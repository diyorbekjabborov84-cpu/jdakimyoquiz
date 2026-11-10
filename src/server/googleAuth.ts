import crypto from "node:crypto";
import { getAuth } from "firebase-admin/auth";

export const ADMIN_GOOGLE_EMAIL = "diyorbekjabborov84@gmail.com";
const GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs";
const ALLOWED_ISSUERS = new Set(["accounts.google.com", "https://accounts.google.com"]);
const MAX_TOKEN_AGE_SECONDS = 300; // 5 daqiqa
export const JWKS_CACHE_TTL_MS = 60 * 60_000; // 1 soat
export const MIN_JWKS_REFRESH_INTERVAL_MS = 60_000; // Majburiy qayta yuklashlar orasida kamida 60 soniya

export interface GoogleJwk {
  kid: string;
  kty: string;
  alg?: string;
  use?: string;
  n: string;
  e: string;
}

export interface GoogleOneTapVerifyResult {
  valid: boolean;
  error?:
    | "CLIENT_ID_NOT_CONFIGURED"
    | "INVALID_TOKEN_FORMAT"
    | "INVALID_SIGNATURE"
    | "INVALID_ISSUER"
    | "INVALID_AUDIENCE"
    | "TOKEN_EXPIRED"
    | "EMAIL_NOT_VERIFIED"
    | "UNAUTHORIZED_EMAIL";
  message?: string;
  email?: string;
}

let cachedJwks: { keys: GoogleJwk[]; fetchedAt: number; expiresAt: number } | null = null;

export function resetGoogleJwksCache(): void {
  cachedJwks = null;
}

async function fetchGoogleJwksFromNetwork(): Promise<GoogleJwk[]> {
  const res = await fetch(GOOGLE_JWKS_URL, {
    headers: { Accept: "application/json" },
    signal: AbortSignal.timeout(8000),
  });
  if (!res.ok) {
    throw new Error(`Google JWKS fetch failed: ${res.status}`);
  }
  const data = (await res.json()) as { keys?: GoogleJwk[] };
  return Array.isArray(data?.keys) ? data.keys : [];
}

async function getGoogleJwks(
  forceRefresh = false,
  customFetcher?: () => Promise<GoogleJwk[]>,
  nowMs = Date.now()
): Promise<GoogleJwk[]> {
  if (!forceRefresh && cachedJwks && nowMs < cachedJwks.expiresAt) {
    return cachedJwks.keys;
  }

  // Agar kid topilmagani uchun majburiy yangilash so'ralgan bo'lsa,
  // oxirgi yuklashdan beri kamida 60 soniya o'tgan bo'lishi shart (DoS himoyasi).
  if (
    forceRefresh &&
    cachedJwks &&
    nowMs - cachedJwks.fetchedAt < MIN_JWKS_REFRESH_INTERVAL_MS
  ) {
    return cachedJwks.keys;
  }

  const fetcher = customFetcher || fetchGoogleJwksFromNetwork;
  const keys = await fetcher();
  cachedJwks = {
    keys,
    fetchedAt: nowMs,
    expiresAt: nowMs + JWKS_CACHE_TTL_MS,
  };
  return keys;
}

export async function verifyGoogleAdmin(
  idToken: string,
  verify = (token: string) => getAuth().verifyIdToken(token, true)
): Promise<boolean> {
  try {
    const claims = await verify(idToken);
    return (
      claims.email_verified === true &&
      claims.email?.toLowerCase() === ADMIN_GOOGLE_EMAIL &&
      claims.firebase?.sign_in_provider === "google.com" &&
      Number.isFinite(claims.auth_time) &&
      Math.floor(Date.now() / 1000) - claims.auth_time <= 300 &&
      claims.auth_time <= Math.floor(Date.now() / 1000) + 60
    );
  } catch {
    return false;
  }
}

/**
 * Google Identity Services (One Tap / FedCM) ID tokenini Google JWKS orqali tekshirish:
 * - Imzo: Google JWKS (RS256)
 * - iss: "accounts.google.com" yoki "https://accounts.google.com"
 * - aud: GOOGLE_OAUTH_CLIENT_ID
 * - exp va iat: yangi bo'lishi shart
 * - email_verified: true
 * - email: ADMIN_GOOGLE_EMAIL ga aynan teng
 */
export async function verifyGoogleOneTapToken(
  credential: string,
  expectedClientId?: string,
  options?: {
    jwksFetcher?: () => Promise<GoogleJwk[]>;
    nowSeconds?: number;
    nowMs?: number;
  }
): Promise<GoogleOneTapVerifyResult> {
  const clientId = expectedClientId?.trim();
  if (!clientId) {
    return {
      valid: false,
      error: "CLIENT_ID_NOT_CONFIGURED",
      message: "Serverda GOOGLE_OAUTH_CLIENT_ID sozlanmagan.",
    };
  }

  if (!credential || typeof credential !== "string") {
    return {
      valid: false,
      error: "INVALID_TOKEN_FORMAT",
      message: "Google ID token formati yaroqsiz.",
    };
  }

  const parts = credential.split(".");
  if (parts.length !== 3) {
    return {
      valid: false,
      error: "INVALID_TOKEN_FORMAT",
      message: "Google ID token formati yaroqsiz.",
    };
  }

  const [headerB64, payloadB64, signatureB64] = parts;
  let header: any;
  let payload: any;
  try {
    header = JSON.parse(Buffer.from(headerB64, "base64url").toString("utf8"));
    payload = JSON.parse(Buffer.from(payloadB64, "base64url").toString("utf8"));
  } catch {
    return {
      valid: false,
      error: "INVALID_TOKEN_FORMAT",
      message: "Google ID token dekodlanmadi.",
    };
  }

  if (!header || header.alg !== "RS256" || typeof header.kid !== "string" || !header.kid) {
    return {
      valid: false,
      error: "INVALID_SIGNATURE",
      message: "Google ID token imzo algoritmi yaroqsiz.",
    };
  }

  // 1. Imzoni Google JWKS bo'yicha tekshirish (agar kid keshda topilmasa, >=60s sharti bilan bir marta qayta yuklanadi)
  const nowMs =
    options?.nowMs ??
    (options?.nowSeconds !== undefined ? options.nowSeconds * 1000 : Date.now());
  try {
    let keys = await getGoogleJwks(false, options?.jwksFetcher, nowMs);
    let jwk = keys.find((k) => k.kid === header.kid);
    if (!jwk) {
      keys = await getGoogleJwks(true, options?.jwksFetcher, nowMs);
      jwk = keys.find((k) => k.kid === header.kid);
    }
    if (!jwk) {
      return {
        valid: false,
        error: "INVALID_SIGNATURE",
        message: "Google JWKS kaliti topilmadi.",
      };
    }

    const publicKey = crypto.createPublicKey({
      key: jwk as any,
      format: "jwk",
    });

    const signingInput = Buffer.from(`${headerB64}.${payloadB64}`, "utf8");
    const signature = Buffer.from(signatureB64, "base64url");
    const sigOk = crypto.verify("RSA-SHA256", signingInput, publicKey, signature);
    if (!sigOk) {
      return {
        valid: false,
        error: "INVALID_SIGNATURE",
        message: "Google ID token imzosi noto'g'ri.",
      };
    }
  } catch {
    return {
      valid: false,
      error: "INVALID_SIGNATURE",
      message: "Google ID token imzosini tekshirishda xatolik.",
    };
  }

  // 2. iss tekshiruvi
  if (typeof payload.iss !== "string" || !ALLOWED_ISSUERS.has(payload.iss)) {
    return {
      valid: false,
      error: "INVALID_ISSUER",
      message: "Token issuer (iss) noto'g'ri.",
    };
  }

  // 3. aud tekshiruvi
  if (typeof payload.aud !== "string" || payload.aud !== clientId) {
    return {
      valid: false,
      error: "INVALID_AUDIENCE",
      message: "Token audience (aud) mos emas.",
    };
  }

  // 4. exp va iat yangiligi tekshiruvi
  const now = options?.nowSeconds ?? Math.floor(Date.now() / 1000);
  const iat = Number(payload.iat);
  const exp = Number(payload.exp);
  if (
    !Number.isFinite(iat) ||
    !Number.isFinite(exp) ||
    exp <= now ||
    iat > now + 60 ||
    now - iat > MAX_TOKEN_AGE_SECONDS
  ) {
    return {
      valid: false,
      error: "TOKEN_EXPIRED",
      message: "Google ID token muddati o'tgan yoki vaqti yaroqsiz.",
    };
  }

  // 5. email_verified === true
  if (payload.email_verified !== true) {
    return {
      valid: false,
      error: "EMAIL_NOT_VERIFIED",
      message: "Google hisobining email manzili tasdiqlanmagan.",
    };
  }

  // 6. email === ADMIN_GOOGLE_EMAIL
  const email = typeof payload.email === "string" ? payload.email.trim().toLowerCase() : "";
  if (email !== ADMIN_GOOGLE_EMAIL.toLowerCase()) {
    return {
      valid: false,
      error: "UNAUTHORIZED_EMAIL",
      message: "Bu hisobga ruxsat yo'q",
    };
  }

  return {
    valid: true,
    email: ADMIN_GOOGLE_EMAIL,
  };
}
