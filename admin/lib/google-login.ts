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
 * /login sahifasi ochilganda mavjud sessiyani /api/auth/me orqali tekshirish.
 * Sessiya yaroqli bo'lsa, darhol "/" ga yo'naltiradi va true qaytaradi.
 */
export async function checkExistingSessionAndRedirect(
  fetchImpl: typeof fetch,
  replaceRoute: (path: string) => void
): Promise<boolean> {
  try {
    const res = await fetchImpl("/api/auth/me", { cache: "no-store" });
    if (!res.ok) return false;
    const data = await res.json();
    if (data && data.ok) {
      replaceRoute("/");
      return true;
    }
    return false;
  } catch {
    return false;
  }
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
