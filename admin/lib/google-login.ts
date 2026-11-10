import { getApps, initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  inMemoryPersistence,
  setPersistence,
  signInWithPopup,
  signOut,
} from "firebase/auth";

export const LOGOUT_SESSION_FLAG = "admin_logged_out";

/**
 * Render free tarifida sovuq uyg'onish (cold start) ~60 soniyagacha cho'zilishi mumkin.
 * 502/503 yoki tarmoq xatosida ketma-ket kutish oraliqlari (jami 61 soniya):
 * 3s -> 6s -> 12s -> 20s -> 20s
 */
export const DEFAULT_SESSION_RETRY_DELAYS_MS = [3000, 6000, 12000, 20000, 20000];

export interface VerifySessionRetryOptions {
  fetchImpl?: typeof fetch;
  onRedirectToLogin?: (path: "/login") => void;
  onWakingChange?: (waking: boolean, attempt: number, maxAttempts: number) => void;
  retryDelaysMs?: number[];
  sleepImpl?: (ms: number) => Promise<void>;
  shouldAbort?: () => boolean;
}

export interface VerifySessionRetryResult {
  status: "authenticated" | "unauthenticated" | "unavailable";
  user?: any;
  attempts: number;
  redirectedToLogin: boolean;
}

export interface LoginSessionCheckOptions {
  onWakingChange?: (waking: boolean, attempt: number, maxAttempts: number) => void;
  retryDelaysMs?: number[];
  sleepImpl?: (ms: number) => Promise<void>;
  shouldAbort?: () => boolean;
  searchStr?: string;
  storage?: Pick<Storage, "getItem">;
}

export interface LoginSessionCheckResult {
  status: "authenticated" | "unauthenticated" | "unavailable";
  redirected: boolean;
  shouldStartOneTap: boolean;
  attempts: number;
}

const defaultSleep = (ms: number) =>
  new Promise<void>((resolve) => setTimeout(resolve, ms));

export async function getGoogleIdToken() {
  const config = await fetch("/api/auth/google/config", { cache: "no-store" }).then((r) =>
    r.json()
  );
  if (!config.apiKey) throw new Error("GOOGLE_NOT_CONFIGURED");
  const app = getApps()[0] || initializeApp(config);
  const auth = getAuth(app);
  await setPersistence(auth, inMemoryPersistence);
  const provider = new GoogleAuthProvider();
  try {
    const result = await signInWithPopup(auth, provider);
    return await result.user.getIdToken();
  } finally {
    await signOut(auth);
  }
}

/**
 * Himoyalangan admin sahifalarida sessiyani tekshirish:
 * - Faqat 401 javobida /login ga yo'naltiradi;
 * - 502, 503 yoki tarmoq xatosida /login ga YO'NALTIRMAYDI, balki "Server uyg'onmoqda..."
 *   holatini bildirib, retryDelaysMs bo'yicha qayta urinadi.
 */
export async function verifyAdminSessionWithRetry(
  options?: VerifySessionRetryOptions
): Promise<VerifySessionRetryResult> {
  const fetchImpl = options?.fetchImpl || fetch;
  const delays = options?.retryDelaysMs ?? DEFAULT_SESSION_RETRY_DELAYS_MS;
  const sleepImpl = options?.sleepImpl || defaultSleep;
  const maxRetries = delays.length;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    if (options?.shouldAbort?.()) {
      return {
        status: "unavailable",
        attempts: attempt,
        redirectedToLogin: false,
      };
    }

    let isTransientFailure = false;
    try {
      const res = await fetchImpl("/api/auth/me", { cache: "no-store" });
      if (options?.shouldAbort?.()) {
        return {
          status: "unavailable",
          attempts: attempt + 1,
          redirectedToLogin: false,
        };
      }

      // Faqat 401 da /login ga yo'naltiriladi!
      if (res.status === 401) {
        options?.onWakingChange?.(false, attempt, maxRetries);
        options?.onRedirectToLogin?.("/login");
        return {
          status: "unauthenticated",
          attempts: attempt + 1,
          redirectedToLogin: true,
        };
      }

      if (res.ok) {
        const data = await res.json().catch(() => ({}));
        if (data && data.ok) {
          options?.onWakingChange?.(false, attempt, maxRetries);
          return {
            status: "authenticated",
            user: data.user,
            attempts: attempt + 1,
            redirectedToLogin: false,
          };
        }
      }

      // 502, 503 yoki boshqa vaqtinchalik server javobi
      isTransientFailure = true;
    } catch {
      // Tarmoq xatosi yoki timeout
      isTransientFailure = true;
    }

    if (isTransientFailure && attempt < maxRetries) {
      options?.onWakingChange?.(true, attempt + 1, maxRetries);
      await sleepImpl(delays[attempt]);
      continue;
    }
  }

  options?.onWakingChange?.(false, maxRetries, maxRetries);
  return {
    status: "unavailable",
    attempts: maxRetries + 1,
    redirectedToLogin: false,
  };
}

/**
 * /login sahifasi uchun sessiya tekshiruvi:
 * - 200 OK bo'lsa: "/" ga yo'naltiradi, One Tap ishga tushmaydi;
 * - 502/503 yoki tarmoq xatosi bo'lsa: qayta urinadi, One Tap ishga tushmaydi;
 * - Faqat 401 (haqiqatan sessiya yo'q) bo'lsa va logout bayrog'i bo'lmasa:
 *   shouldStartOneTap = true qaytaradi.
 */
export async function checkLoginSessionWithRetry(
  fetchImpl: typeof fetch,
  replaceRoute: (path: string) => void,
  options?: LoginSessionCheckOptions
): Promise<LoginSessionCheckResult> {
  const result = await verifyAdminSessionWithRetry({
    fetchImpl,
    onWakingChange: options?.onWakingChange,
    retryDelaysMs: options?.retryDelaysMs,
    sleepImpl: options?.sleepImpl,
    shouldAbort: options?.shouldAbort,
  });

  if (result.status === "authenticated") {
    replaceRoute("/");
    return {
      status: "authenticated",
      redirected: true,
      shouldStartOneTap: false,
      attempts: result.attempts,
    };
  }

  if (result.status === "unauthenticated") {
    const skipAuto = shouldSkipOneTapAutoLogin(options?.searchStr, options?.storage);
    return {
      status: "unauthenticated",
      redirected: false,
      shouldStartOneTap: !skipAuto,
      attempts: result.attempts,
    };
  }

  // status === "unavailable" (502/503 barcha qayta urinishlardan keyin ham javob bermadi)
  return {
    status: "unavailable",
    redirected: false,
    shouldStartOneTap: false,
    attempts: result.attempts,
  };
}

/**
 * /login sahifasi ochilganda mavjud sessiyani /api/auth/me orqali tekshirish (502/503 da qayta urinish bilan).
 * Sessiya yaroqli bo'lsa, "/" ga yo'naltiradi va true qaytaradi.
 */
export async function checkExistingSessionAndRedirect(
  fetchImpl: typeof fetch,
  replaceRoute: (path: string) => void,
  options?: LoginSessionCheckOptions
): Promise<boolean> {
  const res = await checkLoginSessionWithRetry(fetchImpl, replaceRoute, options);
  return res.redirected;
}

/**
 * Chiqish (Logout) bosilganda Google One Tap avtomatik kirishini o'chirish,
 * aks holda /login sahifasiga qaytganda darhol qayta kirib ketadi.
 */
export function disableGoogleAutoSelectOnLogout(
  win: any = typeof window !== "undefined" ? window : undefined,
  storage: Pick<Storage, "setItem"> | undefined = typeof sessionStorage !== "undefined"
    ? sessionStorage
    : undefined
): void {
  try {
    storage?.setItem(LOGOUT_SESSION_FLAG, "1");
  } catch {
    // ignore storage errors
  }
  try {
    if (win?.google?.accounts?.id && typeof win.google.accounts.id.disableAutoSelect === "function") {
      win.google.accounts.id.disableAutoSelect();
    }
  } catch {
    // ignore
  }
}

/**
 * Foydalanuvchi "Chiqish" tugmasini bosib chiqqan bo'lsa, One Tap avtomatik ishga tushmasligi kerak.
 */
export function shouldSkipOneTapAutoLogin(
  searchStr = typeof window !== "undefined" ? window.location.search : "",
  storage: Pick<Storage, "getItem"> | undefined = typeof sessionStorage !== "undefined"
    ? sessionStorage
    : undefined
): boolean {
  if (searchStr && searchStr.includes("logout=1")) {
    return true;
  }
  try {
    if (storage?.getItem(LOGOUT_SESSION_FLAG) === "1") {
      return true;
    }
  } catch {
    // ignore
  }
  return false;
}
