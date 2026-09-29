import crypto from "node:crypto";

export interface TelegramAuthPayload {
  id: number | string;
  first_name?: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
  auth_date: number | string;
  hash: string;
}

export interface AdminSession {
  adminId: string;
  username?: string;
  iat: number;
  exp: number;
}

/**
 * Telegram Login Widget ma'lumotlarini rasmiy HMAC-SHA256 algoritmi orqali tekshirish
 * va faqat ruxsat berilgan ADMIN_TELEGRAM_ID bilan solishtirish.
 */
export function verifyTelegramAuth(
  payload: TelegramAuthPayload,
  botToken: string,
  adminTelegramId?: string
): { success: boolean; error?: string; user?: any } {
  // 1. Fail-closed: Agar serverda ADMIN_TELEGRAM_ID sozlanmagan bo'lsa, kirish yopiq!
  if (!adminTelegramId || !adminTelegramId.trim()) {
    return { success: false, error: "ADMIN_NOT_CONFIGURED" };
  }

  if (!botToken || !botToken.trim()) {
    return { success: false, error: "BOT_TOKEN_NOT_CONFIGURED" };
  }

  if (!payload || typeof payload !== "object") {
    return { success: false, error: "INVALID_PAYLOAD" };
  }

  // 2. Kutilmagan maydonlar va xavfsizlik tekshiruvi (faqat ruxsat etilgan Telegram maydonlari)
  const allowedKeys = new Set(["auth_date", "first_name", "id", "last_name", "photo_url", "username", "hash"]);
  for (const key of Object.keys(payload)) {
    if (!allowedKeys.has(key)) {
      return { success: false, error: "UNEXPECTED_FIELD" };
    }
    const val = (payload as any)[key];
    if (val !== undefined && val !== null && typeof val !== "string" && typeof val !== "number") {
      return { success: false, error: "INVALID_FIELD_TYPE" };
    }
  }

  // 3. ID tekshiruvi: faqat ADMIN_TELEGRAM_ID ga teng bo'lgan raqamli ID kirishi mumkin!
  const targetId = String(payload.id).trim();
  if (!targetId || targetId !== adminTelegramId.trim()) {
    return { success: false, error: "UNAUTHORIZED_ADMIN" };
  }

  // 4. auth_date yangiligi: yangi login uchun oqilona qisqa muddat (5 daqiqa / 300 soniya)
  const authTime = Number(payload.auth_date);
  const now = Math.floor(Date.now() / 1000);
  const MAX_AUTH_AGE_SECONDS = 300; // 5 daqiqa
  if (isNaN(authTime) || now - authTime > MAX_AUTH_AGE_SECONDS || authTime > now + 60) {
    return { success: false, error: "EXPIRED_AUTH" };
  }

  // 5. Telegram rasmiy data_check_string hosil qilish:
  // "hash" dan tashqari barcha ruxsat etilgan kalitlar alfavit tartibida "key=value\n" ko'rinishida yig'iladi.
  const fields: string[] = [];
  const checkKeys = ["auth_date", "first_name", "id", "last_name", "photo_url", "username"];

  for (const key of checkKeys) {
    const val = (payload as any)[key];
    if (val !== undefined && val !== null && val !== "") {
      fields.push(`${key}=${val}`);
    }
  }

  const dataCheckString = fields.join("\n");

  // 6. Bot API tokenidan SHA256 maxfiy kalit olinadi
  const secretKey = crypto.createHash("sha256").update(botToken).digest();

  // 7. HMAC-SHA256 orqali hisoblangan imzo
  const calculatedHash = crypto
    .createHmac("sha256", secretKey)
    .update(dataCheckString)
    .digest("hex");

  // 8. Doimiy vaqtli (timing-safe) taqqoslash va 64 belgili hex tekshiruvi
  if (typeof payload.hash !== "string" || !/^[a-f0-9]{64}$/i.test(payload.hash)) {
    return { success: false, error: "INVALID_HASH" };
  }

  const isValid = crypto.timingSafeEqual(
    Buffer.from(calculatedHash, "hex"),
    Buffer.from(payload.hash, "hex")
  );

  if (!isValid) {
    return { success: false, error: "INVALID_HASH" };
  }

  return {
    success: true,
    user: {
      id: targetId,
      firstName: payload.first_name || "",
      lastName: payload.last_name || null,
      username: payload.username || null,
      photoUrl: payload.photo_url || null,
    },
  };
}

/**
 * Sessiya kalitini tekshirish.
 * Hech qanday fallback yoki bo'sh kalit qabul qilinmaydi!
 * ADMIN_SESSION_SECRET kamida 32 belgidan iborat kuchli kalit bo'lishi shart.
 */
function getSessionSecret(secret?: string): string {
  if (!secret || typeof secret !== "string" || secret.trim().length < 32) {
    throw new Error("SECRET_NOT_CONFIGURED");
  }
  return secret.trim();
}

/**
 * Admin sessiyasi uchun imzolangan xavfsiz token (HMAC-SHA256 JWT) yaratish.
 * Maksimal sessiya umri 7 kundan oshmaydi.
 */
export function createAdminSessionToken(
  adminId: string | number,
  username?: string,
  secret?: string,
  expiresInSeconds = 7 * 86400
): string {
  const signingKey = getSessionSecret(secret);
  const now = Math.floor(Date.now() / 1000);
  const clampedExp = Math.min(Math.max(expiresInSeconds, 60), 7 * 86400);

  const sessionData: AdminSession = {
    adminId: String(adminId),
    username: username || undefined,
    iat: now,
    exp: now + clampedExp,
  };

  const headerB64 = Buffer.from(JSON.stringify({ alg: "HS256", typ: "JWT" })).toString("base64url");
  const payloadB64 = Buffer.from(JSON.stringify(sessionData)).toString("base64url");
  const signingInput = `${headerB64}.${payloadB64}`;

  const signature = crypto
    .createHmac("sha256", signingKey)
    .update(signingInput)
    .digest("base64url");

  return `${signingInput}.${signature}`;
}

/**
 * Admin sessiyasi tokenini tekshirish.
 * Imzo, muddat, iat/exp chegaralari va admin ID qat'iy tekshiriladi.
 */
export function verifyAdminSessionToken(
  token: string,
  adminTelegramId?: string,
  secret?: string
): { valid: boolean; session?: AdminSession; error?: string } {
  // Fail-closed
  if (!adminTelegramId || !adminTelegramId.trim()) {
    return { valid: false, error: "ADMIN_NOT_CONFIGURED" };
  }

  let signingKey: string;
  try {
    signingKey = getSessionSecret(secret);
  } catch {
    return { valid: false, error: "SECRET_NOT_CONFIGURED" };
  }

  if (!token || typeof token !== "string") {
    return { valid: false, error: "TOKEN_MISSING" };
  }

  const parts = token.split(".");
  if (parts.length !== 3) {
    return { valid: false, error: "TOKEN_MALFORMED" };
  }

  const [headerB64, payloadB64, signature] = parts;
  const signingInput = `${headerB64}.${payloadB64}`;

  let expectedSig: string;
  try {
    expectedSig = crypto
      .createHmac("sha256", signingKey)
      .update(signingInput)
      .digest("base64url");
  } catch {
    return { valid: false, error: "SIGNATURE_INVALID" };
  }

  if (signature.length !== expectedSig.length) {
    return { valid: false, error: "SIGNATURE_INVALID" };
  }

  const isSigValid = crypto.timingSafeEqual(
    Buffer.from(signature, "utf-8"),
    Buffer.from(expectedSig, "utf-8")
  );

  if (!isSigValid) {
    return { valid: false, error: "SIGNATURE_INVALID" };
  }

  let session: AdminSession;
  try {
    session = JSON.parse(Buffer.from(payloadB64, "base64url").toString("utf-8"));
  } catch {
    return { valid: false, error: "PAYLOAD_INVALID" };
  }

  // iat va exp sonli va mantiqan to'g'ri bo'lishi shart
  if (
    typeof session.iat !== "number" ||
    typeof session.exp !== "number" ||
    isNaN(session.iat) ||
    isNaN(session.exp)
  ) {
    return { valid: false, error: "TOKEN_MALFORMED" };
  }

  const now = Math.floor(Date.now() / 1000);

  // iat kelajakda bo'lmasligi kerak (60 soniya clock skew)
  if (session.iat > now + 60) {
    return { valid: false, error: "TOKEN_MALFORMED" };
  }

  // exp muddati o'tgan bo'lmasligi kerak
  if (session.exp <= now) {
    return { valid: false, error: "TOKEN_EXPIRED" };
  }

  // Maksimal umr 7 kundan oshmasligi shart!
  if (session.exp - session.iat > 7 * 86400) {
    return { valid: false, error: "TOKEN_INVALID_EXPIRY" };
  }

  // Raqamli Telegram ID mosligi qat'iy tekshiriladi
  if (String(session.adminId).trim() !== adminTelegramId.trim()) {
    return { valid: false, error: "UNAUTHORIZED_ADMIN" };
  }

  return { valid: true, session };
}
