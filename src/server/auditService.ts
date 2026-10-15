import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";

export interface AuditLogEntry {
  id?: string;
  admin: string;
  action: string;
  details?: Record<string, any>;
  ip?: string;
  timestamp: string;
  createdAt: number;
}

// In-memory zaxira loglar (agar Firestore vaqtincha mavjud bo'lmasa yoki testlarda)
const inMemoryLogs: AuditLogEntry[] = [];

/**
 * Admin harakatlarini (audit log) Cloud Firestore'ga yozish
 */
export async function recordAuditLog(payload: {
  admin: string;
  action: string;
  details?: Record<string, any>;
  ip?: string;
}): Promise<AuditLogEntry> {
  const now = Date.now();
  const entry: AuditLogEntry = {
    admin: payload.admin || "admin",
    action: payload.action,
    details: payload.details || {},
    ip: payload.ip,
    timestamp: new Date(now).toISOString(),
    createdAt: now,
  };

  // Har doim in-memory logga qo'shamiz (oxirgi 200 tasi saqlanadi)
  inMemoryLogs.unshift(entry);
  if (inMemoryLogs.length > 200) {
    inMemoryLogs.pop();
  }

  const db = getFirestoreDb();
  if (db) {
    try {
      const docRef = await db.collection(FIRESTORE_COLLECTIONS.AUDIT_LOGS).add(entry);
      entry.id = docRef.id;
    } catch (err: any) {
      console.error("[AuditService] Audit logni Firestore'ga yozishda xatolik:", err?.message || err);
    }
  }

  return entry;
}

/**
 * Audit loglari ro'yxatini olish (eng so'nggilari yuqorida)
 */
export async function getAuditLogs(limitCount = 50): Promise<AuditLogEntry[]> {
  const db = getFirestoreDb();
  if (!db) {
    return inMemoryLogs.slice(0, limitCount);
  }

  try {
    const snap = await db
      .collection(FIRESTORE_COLLECTIONS.AUDIT_LOGS)
      .orderBy("createdAt", "desc")
      .limit(limitCount)
      .get();

    if (snap.empty) {
      return inMemoryLogs.slice(0, limitCount);
    }

    return snap.docs.map((doc) => {
      const data = doc.data();
      return {
        id: doc.id,
        admin: data.admin || "admin",
        action: data.action || "UNKNOWN",
        details: data.details || {},
        ip: data.ip,
        timestamp: data.timestamp || new Date().toISOString(),
        createdAt: data.createdAt || 0,
      };
    });
  } catch (err: any) {
    console.warn("[AuditService] Firestore audit loglarni o'qishda xatolik, in-memory qaytarilmoqda:", err?.message || err);
    return inMemoryLogs.slice(0, limitCount);
  }
}
