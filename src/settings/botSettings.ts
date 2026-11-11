import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";

export type DefaultGroupMode = "asosiy" | "ochiq_emas";
export type GroupShellMode = "asosiy" | "kurs" | "ochiq_emas";

export interface BotSettingsData {
  adminContact: string;
  defaultGroupMode: DefaultGroupMode;
  kursQuestionTimeSeconds: number;
  updatedAt?: string;
}

export const DEFAULT_BOT_SETTINGS: BotSettingsData = {
  adminContact: "@diyorbek_jabborov",
  defaultGroupMode: "asosiy",
  kursQuestionTimeSeconds: 25,
};

const SETTINGS_DOC_ID = "global";
const CACHE_TTL_MS = 60_000;

let cachedSettings: BotSettingsData | null = null;
let cacheExpiresAt = 0;
let memoryFallbackSettings: BotSettingsData = { ...DEFAULT_BOT_SETTINGS };

export function normalizeAdminContact(raw: unknown): string | null {
  if (typeof raw !== "string") return null;
  const trimmed = raw.trim();
  if (!trimmed) return null;
  const withoutAt = trimmed.replace(/^@/, "");
  if (!/^[a-zA-Z0-9_]{3,64}$/.test(withoutAt)) {
    return null;
  }
  return `@${withoutAt}`;
}

export function isValidDefaultGroupMode(mode: unknown): mode is DefaultGroupMode {
  return mode === "asosiy" || mode === "ochiq_emas";
}

export function isValidGroupMode(mode: unknown): mode is GroupShellMode {
  return mode === "asosiy" || mode === "kurs" || mode === "ochiq_emas";
}

export function isValidKursQuestionTimeSeconds(val: unknown): val is number {
  return typeof val === "number" && Number.isInteger(val) && val >= 20 && val <= 25;
}

export function getAdminContactUrl(adminContact: string): string {
  const clean = adminContact.replace(/^@/, "").trim() || "diyorbek_jabborov";
  return `https://t.me/${clean}`;
}

export function invalidateBotSettingsCache(): void {
  cachedSettings = null;
  cacheExpiresAt = 0;
}

export function resetBotSettingsState(): void {
  cachedSettings = null;
  cacheExpiresAt = 0;
  memoryFallbackSettings = { ...DEFAULT_BOT_SETTINGS };
}

export async function getBotSettings(): Promise<BotSettingsData> {
  const now = Date.now();
  if (cachedSettings && now < cacheExpiresAt) {
    return { ...cachedSettings };
  }

  const db = getFirestoreDb();
  if (!db) {
    cachedSettings = { ...memoryFallbackSettings };
    cacheExpiresAt = now + CACHE_TTL_MS;
    return { ...cachedSettings };
  }

  try {
    const docSnap = await db.collection(FIRESTORE_COLLECTIONS.SETTINGS).doc(SETTINGS_DOC_ID).get();
    if (!docSnap.exists) {
      cachedSettings = { ...DEFAULT_BOT_SETTINGS };
      cacheExpiresAt = now + CACHE_TTL_MS;
      return { ...cachedSettings };
    }
    const data = docSnap.data() || {};
    const adminContact = normalizeAdminContact(data.adminContact) || DEFAULT_BOT_SETTINGS.adminContact;
    const defaultGroupMode: DefaultGroupMode = isValidDefaultGroupMode(data.defaultGroupMode)
      ? data.defaultGroupMode
      : DEFAULT_BOT_SETTINGS.defaultGroupMode;
    const rawKursTime =
      typeof data.kursQuestionTimeSeconds === "number"
        ? data.kursQuestionTimeSeconds
        : typeof data.kursQuestionTimeSeconds === "string" && data.kursQuestionTimeSeconds.trim() !== ""
        ? Number(data.kursQuestionTimeSeconds)
        : undefined;
    const kursQuestionTimeSeconds = isValidKursQuestionTimeSeconds(rawKursTime)
      ? rawKursTime
      : DEFAULT_BOT_SETTINGS.kursQuestionTimeSeconds;

    cachedSettings = {
      adminContact,
      defaultGroupMode,
      kursQuestionTimeSeconds,
      updatedAt: typeof data.updatedAt === "string" ? data.updatedAt : undefined,
    };
    cacheExpiresAt = now + CACHE_TTL_MS;
    return { ...cachedSettings };
  } catch (err) {
    console.error("[BotSettings] Sozlamalarni o'qishda xatolik:", err);
    return cachedSettings ? { ...cachedSettings } : { ...DEFAULT_BOT_SETTINGS };
  }
}

export async function updateBotSettings(patch: {
  adminContact?: string;
  defaultGroupMode?: DefaultGroupMode;
  kursQuestionTimeSeconds?: number;
}): Promise<BotSettingsData> {
  const current = await getBotSettings();
  const nextAdminContact =
    patch.adminContact !== undefined ? normalizeAdminContact(patch.adminContact) : current.adminContact;
  if (!nextAdminContact) {
    throw new Error("adminContact noto'g'ri formatda (masalan: @diyorbek_jabborov).");
  }

  const nextDefaultGroupMode =
    patch.defaultGroupMode !== undefined ? patch.defaultGroupMode : current.defaultGroupMode;
  if (!isValidDefaultGroupMode(nextDefaultGroupMode)) {
    throw new Error("defaultGroupMode faqat 'asosiy' yoki 'ochiq_emas' bo'lishi mumkin.");
  }

  const nextKursQuestionTimeSeconds =
    patch.kursQuestionTimeSeconds !== undefined
      ? patch.kursQuestionTimeSeconds
      : current.kursQuestionTimeSeconds;
  if (!isValidKursQuestionTimeSeconds(nextKursQuestionTimeSeconds)) {
    throw new Error("kursQuestionTimeSeconds 20 dan 25 gacha butun son bo'lishi kerak.");
  }

  const updated: BotSettingsData = {
    adminContact: nextAdminContact,
    defaultGroupMode: nextDefaultGroupMode,
    kursQuestionTimeSeconds: nextKursQuestionTimeSeconds,
    updatedAt: new Date().toISOString(),
  };

  const db = getFirestoreDb();
  if (db) {
    await db
      .collection(FIRESTORE_COLLECTIONS.SETTINGS)
      .doc(SETTINGS_DOC_ID)
      .set(updated, { merge: true });
  } else {
    memoryFallbackSettings = { ...updated };
  }

  cachedSettings = { ...updated };
  cacheExpiresAt = Date.now() + CACHE_TTL_MS;
  return { ...updated };
}
