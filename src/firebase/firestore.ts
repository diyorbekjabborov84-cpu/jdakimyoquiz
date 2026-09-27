import fs from "node:fs";
import { initializeApp, cert, getApps, App, ServiceAccount } from "firebase-admin/app";
import { getFirestore, Firestore } from "firebase-admin/firestore";

let appInstance: App | null = null;
let firestoreDb: Firestore | null = null;
let isInitialized = false;

export const FIRESTORE_COLLECTIONS = {
  SESSIONS: "quiz_sessions",
  RESULTS: "quiz_results",
  GROUPS: "groups",
  USERS: "bot_users",
  QUIZZES: "quizzes",
} as const;

/**
 * Xizmat akkaunti hisob ma'lumotlarini xavfsiz o'qish:
 * 1. Render Secret Files: /etc/secrets/firebase-service-account.json
 * 2. FIREBASE_SERVICE_ACCOUNT_PATH orqali ko'rsatilgan fayl
 * 3. FIREBASE_SERVICE_ACCOUNT_JSON muhit o'zgaruvchisi (JSON matn yoki base64)
 *
 * DIQQAT: Maxfiy kalitlar aslo loglarga yoki xatolik matnlariga chiqarilmaydi!
 */
export function loadFirebaseCredentials(): ServiceAccount | null {
  // 1. Render muhitidagi Secret File
  const renderSecretPath = "/etc/secrets/firebase-service-account.json";
  if (fs.existsSync(renderSecretPath)) {
    try {
      const raw = fs.readFileSync(renderSecretPath, "utf-8");
      return JSON.parse(raw);
    } catch (e) {
      console.error("[Firebase] /etc/secrets/firebase-service-account.json faylini o'qishda xatolik.");
    }
  }

  // 2. Maxsus yo'l ko'rsatilgan bo'lsa
  const customPath = process.env.FIREBASE_SERVICE_ACCOUNT_PATH;
  if (customPath && fs.existsSync(customPath)) {
    try {
      const raw = fs.readFileSync(customPath, "utf-8");
      return JSON.parse(raw);
    } catch (e) {
      console.error("[Firebase] FIREBASE_SERVICE_ACCOUNT_PATH faylini o'qishda xatolik.");
    }
  }

  // 3. FIREBASE_SERVICE_ACCOUNT_JSON muhit o'zgaruvchisi
  const envJson = process.env.FIREBASE_SERVICE_ACCOUNT_JSON;
  if (envJson && envJson.trim()) {
    const trimmed = envJson.trim();
    try {
      // To'g'ridan-to'g'ri JSON parse
      return JSON.parse(trimmed);
    } catch {
      // Agar base64 bilan kodlangan bo'lsa
      try {
        const decoded = Buffer.from(trimmed, "base64").toString("utf-8");
        return JSON.parse(decoded);
      } catch {
        console.error("[Firebase] FIREBASE_SERVICE_ACCOUNT_JSON yaroqli JSON yoki base64 formatda emas.");
      }
    }
  }

  return null;
}

export function getFirestoreDb(): Firestore | null {
  if (firestoreDb) {
    return firestoreDb;
  }

  const apps = getApps();
  if (apps.length > 0) {
    appInstance = apps[0];
    firestoreDb = getFirestore(appInstance);
    firestoreDb.settings({ ignoreUndefinedProperties: true });
    return firestoreDb;
  }

  const creds = loadFirebaseCredentials();
  if (!creds) {
    return null;
  }

  try {
    appInstance = initializeApp({
      credential: cert(creds),
    });
    firestoreDb = getFirestore(appInstance);
    firestoreDb.settings({ ignoreUndefinedProperties: true });
    return firestoreDb;
  } catch (err: any) {
    console.error("[Firebase] Firebase ilovasini initsializatsiya qilishda xatolik:", err?.message || err);
    return null;
  }
}

export async function initFirestore(customDb?: Firestore): Promise<boolean> {
  if (customDb) {
    firestoreDb = customDb;
    isInitialized = true;
    return true;
  }

  if (isInitialized && firestoreDb) {
    return true;
  }

  const db = getFirestoreDb();
  if (!db) {
    console.error("[Firebase] Firestore ma'lumotlar bazasi initsializatsiya qilinmadi (credentials topilmadi).");
    return false;
  }

  try {
    console.log("[Firebase] Cloud Firestore ulanishi tekshirilmoqda...");
    // Yengil va tezkor tekshiruv (hech narsa yozmasdan ulanishni tekshirish)
    await db.collection(FIRESTORE_COLLECTIONS.SESSIONS).limit(1).get();
    isInitialized = true;
    console.log("✅ [Firebase] Cloud Firestore muvaffaqiyatli ulandi.");
    return true;
  } catch (err: any) {
    console.error("❌ [Firebase] Cloud Firestore ulanishida xatolik:", err?.message || err);
    return false;
  }
}

export async function checkFirestoreHealth(): Promise<boolean> {
  const db = getFirestoreDb();
  if (!db) return false;
  try {
    await db.collection(FIRESTORE_COLLECTIONS.SESSIONS).limit(1).get();
    return true;
  } catch {
    return false;
  }
}

export function setCustomFirestoreDb(db: Firestore | null): void {
  firestoreDb = db;
  isInitialized = db !== null;
}

export function resetFirestoreState(): void {
  firestoreDb = null;
  isInitialized = false;
  appInstance = null;
}
