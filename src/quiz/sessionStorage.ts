import fs from "node:fs";
import path from "node:path";
import { Firestore } from "firebase-admin/firestore";
import { Quiz, QuizSession, ParticipantScore } from "./types.js";
import { getDatabasePool, initDatabase } from "../database/db.js";
import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";

export interface SerializedSession {
  sessionId?: string;
  chatId: number;
  quiz: Quiz;
  status: "running" | "paused" | "finishing";
  currentQuestionIndex: number;
  consecutiveUnansweredCount: number;
  participants: [number, ParticipantScore][];
  answeredUsers: string[];
  savedAt: number;
  version?: number;
  finalMessageSent?: boolean;
  sentChunksCount?: number;
}

export interface ISessionStorage {
  saveSession(session: QuizSession): Promise<void>;
  deleteSession(chatId: number): Promise<void>;
  loadAllSessions(): Promise<SerializedSession[]>;
  clearAll?(): Promise<void>;
  isUsingDatabase?(): boolean;
}

/**
 * Mahalliy JSON fayl saqlovchisi (Faqat lokal development va testlar uchun).
 * DIQQAT: Production muhitida ishlatilmaydi; Render Free diskida fayllar
 * restart, spin-down yoki yangi versiya deploy paytida o'chib ketadi.
 */
export class JsonFileSessionStorage implements ISessionStorage {
  private filePath: string;
  private chatQueues = new Map<number, Promise<any>>();

  constructor(customPath?: string) {
    this.filePath = customPath || path.resolve(process.cwd(), "data", "sessions.json");
    this.ensureDir();
  }

  public getFilePath(): string {
    return this.filePath;
  }

  private ensureDir(): void {
    try {
      const dir = path.dirname(this.filePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    } catch (e) {
      console.error("[JsonFileSessionStorage] Papka yaratishda xatolik:", e);
    }
  }

  private enqueueChatOp<T>(chatId: number, op: () => Promise<T>): Promise<T> {
    const previous = this.chatQueues.get(chatId) || Promise.resolve();
    const next = previous
      .catch(() => {})
      .then(op);
    this.chatQueues.set(chatId, next);
    return next.finally(() => {
      if (this.chatQueues.get(chatId) === next) {
        this.chatQueues.delete(chatId);
      }
    });
  }

  public async saveSession(session: QuizSession): Promise<void> {
    return this.enqueueChatOp(session.chatId, async () => {
      if (
        session.status !== "running" &&
        session.status !== "paused" &&
        session.status !== "finishing"
      ) {
        await this.deleteSessionDirect(session.chatId);
        return;
      }

      this.ensureDir();
      const all = this.loadAllInternal();
      const existing = all[session.chatId.toString()];

      // Versiyali shartli yangilash: eski versiyadagi yozuv yangirog'ini bosib ketmasin
      if (existing && existing.version && session.version < existing.version) {
        return;
      }

      const serialized: SerializedSession = {
        sessionId: session.sessionId,
        chatId: session.chatId,
        quiz: session.quiz,
        status: session.status,
        currentQuestionIndex: session.currentQuestionIndex,
        consecutiveUnansweredCount: session.consecutiveUnansweredCount || 0,
        participants: Array.from(session.participants.entries()),
        answeredUsers: Array.from(session.answeredUsers),
        savedAt: Date.now(),
        version: session.version,
        finalMessageSent: Boolean(session.finalMessageSent),
        sentChunksCount: Number(session.sentChunksCount || 0),
      };

      all[session.chatId.toString()] = serialized;
      this.writeAtomic(all);
    });
  }

  public async deleteSession(chatId: number): Promise<void> {
    return this.enqueueChatOp(chatId, async () => {
      await this.deleteSessionDirect(chatId);
    });
  }

  private async deleteSessionDirect(chatId: number): Promise<void> {
    this.ensureDir();
    const all = this.loadAllInternal();
    const key = chatId.toString();
    if (all[key]) {
      delete all[key];
      this.writeAtomic(all);
    }
  }

  public async loadAllSessions(): Promise<SerializedSession[]> {
    const all = this.loadAllInternal();
    return Object.values(all);
  }

  public loadAllSessionsSync(): SerializedSession[] {
    const all = this.loadAllInternal();
    return Object.values(all);
  }

  private loadAllInternal(): Record<string, SerializedSession> {
    if (!fs.existsSync(this.filePath)) {
      return {};
    }
    try {
      const content = fs.readFileSync(this.filePath, "utf-8");
      if (!content.trim()) return {};
      return JSON.parse(content);
    } catch (e) {
      console.error("[JsonFileSessionStorage] JSON faylni o'qishda xatolik:", e);
      return {};
    }
  }

  private writeAtomic(data: Record<string, SerializedSession>): void {
    const tmpPath = `${this.filePath}.tmp.${Date.now()}.${Math.random().toString(36).substring(2, 7)}`;
    const content = JSON.stringify(data, null, 2);
    fs.writeFileSync(tmpPath, content, "utf-8");
    try {
      if (process.platform === "win32" && fs.existsSync(this.filePath)) {
        fs.copyFileSync(tmpPath, this.filePath);
        try {
          fs.unlinkSync(tmpPath);
        } catch {
          // ignore
        }
      } else {
        fs.renameSync(tmpPath, this.filePath);
      }
    } catch {
      fs.writeFileSync(this.filePath, content, "utf-8");
      try {
        if (fs.existsSync(tmpPath)) fs.unlinkSync(tmpPath);
      } catch {
        // ignore
      }
    }
  }

  public async clearAll(): Promise<void> {
    if (fs.existsSync(this.filePath)) {
      fs.unlinkSync(this.filePath);
    }
  }
}

/**
 * PostgreSQL asosidagi doimiy saqlovchi sinf.
 * Render Free / Supabase / Neon qayta ishga tushganda, spin-down yoki
 * yangi versiya deploy qilinganda sessiyalar to'liq saqlanib qoladi.
 */
export class PostgresSessionStorage implements ISessionStorage {
  private chatQueues = new Map<number, Promise<any>>();

  public enqueueChatOp<T>(chatId: number, op: () => Promise<T>): Promise<T> {
    const previous = this.chatQueues.get(chatId) || Promise.resolve();
    const next = previous
      .catch(() => {})
      .then(op);
    this.chatQueues.set(chatId, next);
    return next.finally(() => {
      if (this.chatQueues.get(chatId) === next) {
        this.chatQueues.delete(chatId);
      }
    });
  }

  public async saveSession(session: QuizSession): Promise<void> {
    return this.enqueueChatOp(session.chatId, async () => {
      const pool = getDatabasePool();
      if (!pool) {
        throw new Error("[PostgresSessionStorage] Database pool mavjud emas yoki DATABASE_URL sozlanmagan!");
      }

      if (
        session.status !== "running" &&
        session.status !== "paused" &&
        session.status !== "finishing"
      ) {
        await this.deleteSessionDirect(session.chatId);
        return;
      }

      const query = `
        INSERT INTO quiz_sessions (
          session_id, chat_id, quiz_id, quiz_data, status,
          current_question_index, consecutive_unanswered_count,
          participants, answered_users, saved_at, version, final_message_sent, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, NOW())
        ON CONFLICT (chat_id) DO UPDATE SET
          session_id = EXCLUDED.session_id,
          quiz_id = EXCLUDED.quiz_id,
          quiz_data = EXCLUDED.quiz_data,
          status = EXCLUDED.status,
          current_question_index = EXCLUDED.current_question_index,
          consecutive_unanswered_count = EXCLUDED.consecutive_unanswered_count,
          participants = EXCLUDED.participants,
          answered_users = EXCLUDED.answered_users,
          saved_at = EXCLUDED.saved_at,
          version = EXCLUDED.version,
          final_message_sent = EXCLUDED.final_message_sent,
          updated_at = NOW()
        WHERE quiz_sessions.version <= EXCLUDED.version;
      `;

      const values = [
        session.sessionId,
        session.chatId,
        session.quiz.id,
        JSON.stringify(session.quiz),
        session.status,
        session.currentQuestionIndex,
        session.consecutiveUnansweredCount || 0,
        JSON.stringify(Array.from(session.participants.entries())),
        JSON.stringify(Array.from(session.answeredUsers)),
        Date.now(),
        session.version || 1,
        Boolean(session.finalMessageSent),
      ];

      await pool.query(query, values);
    });
  }

  public async deleteSession(chatId: number): Promise<void> {
    return this.enqueueChatOp(chatId, async () => {
      await this.deleteSessionDirect(chatId);
    });
  }

  private async deleteSessionDirect(chatId: number): Promise<void> {
    const pool = getDatabasePool();
    if (!pool) return;
    await pool.query("DELETE FROM quiz_sessions WHERE chat_id = $1", [chatId]);
  }

  public async loadAllSessions(): Promise<SerializedSession[]> {
    const pool = getDatabasePool();
    if (!pool) {
      throw new Error("[PostgresSessionStorage] Database pool mavjud emas!");
    }

    await initDatabase();
    const res = await pool.query(
      "SELECT * FROM quiz_sessions WHERE status IN ('running', 'paused', 'finishing') ORDER BY updated_at DESC"
    );

    return res.rows.map((row) => ({
      sessionId: row.session_id,
      chatId: Number(row.chat_id),
      quiz: typeof row.quiz_data === "string" ? JSON.parse(row.quiz_data) : row.quiz_data,
      status: row.status as "running" | "paused" | "finishing",
      currentQuestionIndex: row.current_question_index,
      consecutiveUnansweredCount: row.consecutive_unanswered_count,
      participants: typeof row.participants === "string" ? JSON.parse(row.participants) : row.participants,
      answeredUsers: typeof row.answered_users === "string" ? JSON.parse(row.answered_users) : row.answered_users,
      savedAt: Number(row.saved_at),
      version: row.version ? Number(row.version) : 1,
      finalMessageSent: Boolean(row.final_message_sent),
    }));
  }

  public async clearAll(): Promise<void> {
    const pool = getDatabasePool();
    if (!pool) return;
    await pool.query("DELETE FROM quiz_sessions");
  }
}

/**
 * Cloud Firestore asosidagi doimiy saqlovchi sinf.
 * Render Free qayta ishga tushganda, spin-down yoki yangi versiya deploy qilinganda
 * sessiyalar Firebase Cloud Firestore'da to'liq va xavfsiz saqlanib qoladi.
 */
export class FirestoreSessionStorage implements ISessionStorage {
  private customDb?: Firestore;
  private collectionName: string;
  private chatQueues = new Map<number, Promise<any>>();

  constructor(customDb?: Firestore, customCollection?: string) {
    this.customDb = customDb;
    this.collectionName = customCollection || FIRESTORE_COLLECTIONS.SESSIONS;
  }

  public isUsingFirestore(): boolean {
    return true;
  }

  public getCustomDb(): Firestore | undefined {
    return this.customDb;
  }

  private getDb(): Firestore {
    const db = this.customDb || getFirestoreDb();
    if (!db) {
      throw new Error("[FirestoreSessionStorage] Firestore ma'lumotlar bazasi topilmadi yoki ulanmagan!");
    }
    return db;
  }

  public enqueueChatOp<T>(chatId: number, op: () => Promise<T>): Promise<T> {
    const previous = this.chatQueues.get(chatId) || Promise.resolve();
    const next = previous
      .catch(() => {})
      .then(op);
    this.chatQueues.set(chatId, next);
    return next.finally(() => {
      if (this.chatQueues.get(chatId) === next) {
        this.chatQueues.delete(chatId);
      }
    });
  }

  public async saveSession(session: QuizSession): Promise<void> {
    return this.enqueueChatOp(session.chatId, async () => {
      const db = this.getDb();

      if (
        session.status !== "running" &&
        session.status !== "paused" &&
        session.status !== "finishing"
      ) {
        await this.deleteSessionDirect(session.chatId);
        return;
      }

      const docRef = db.collection(this.collectionName).doc(session.chatId.toString());

      // Concurrency: tranzaksiya yordamida versiya tekshiruvi (eski versiya yangisini bosib ketmasligi uchun)
      await db.runTransaction(async (transaction) => {
        const docSnap = await transaction.get(docRef);
        if (docSnap.exists) {
          const existing = docSnap.data();
          if (existing && typeof existing.version === "number" && session.version < existing.version) {
            return;
          }
        }

        // Firestore ichma-ich massivlarni qabul qilmaydi (Nested arrays are not allowed),
        // shuning uchun Map entries emas, ParticipantScore[] array of objects saqlanadi.
        const participantsList = Array.from(session.participants.values());
        const answeredList = Array.from(session.answeredUsers);

        transaction.set(docRef, {
          sessionId: session.sessionId,
          chatId: session.chatId,
          quizId: session.quiz.id,
          quizData: session.quiz,
          status: session.status,
          currentQuestionIndex: session.currentQuestionIndex,
          consecutiveUnansweredCount: session.consecutiveUnansweredCount || 0,
          participants: participantsList,
          answeredUsers: answeredList,
          savedAt: Date.now(),
          version: session.version || 1,
          finalMessageSent: Boolean(session.finalMessageSent),
          sentChunksCount: Number(session.sentChunksCount || 0),
          updatedAt: new Date().toISOString(),
        });
      });
    });
  }

  public async deleteSession(chatId: number): Promise<void> {
    return this.enqueueChatOp(chatId, async () => {
      await this.deleteSessionDirect(chatId);
    });
  }

  private async deleteSessionDirect(chatId: number): Promise<void> {
    const db = this.getDb();
    const docRef = db.collection(this.collectionName).doc(chatId.toString());
    await docRef.delete();
  }

  public async loadAllSessions(): Promise<SerializedSession[]> {
    const db = this.getDb();
    const snapshot = await db
      .collection(this.collectionName)
      .where("status", "in", ["running", "paused", "finishing"])
      .get();

    const results: SerializedSession[] = [];
    for (const doc of snapshot.docs) {
      const data = doc.data();
      let participants: [number, ParticipantScore][] = [];
      if (Array.isArray(data.participants)) {
        participants = data.participants.map((p: any) => {
          if (Array.isArray(p)) return p as [number, ParticipantScore];
          return [p.userId, p as ParticipantScore];
        });
      } else if (typeof data.participants === "string") {
        try {
          participants = JSON.parse(data.participants);
        } catch {
          participants = [];
        }
      } else if (data.participants && typeof data.participants === "object") {
        participants = Object.values(data.participants).map((p: any) => [p.userId, p as ParticipantScore]);
      }

      let quiz = data.quizData;
      if (typeof quiz === "string") {
        try {
          quiz = JSON.parse(quiz);
        } catch {
          // ignore
        }
      }

      results.push({
        sessionId: data.sessionId,
        chatId: Number(data.chatId),
        quiz,
        status: data.status as "running" | "paused" | "finishing",
        currentQuestionIndex: Number(data.currentQuestionIndex),
        consecutiveUnansweredCount: Number(data.consecutiveUnansweredCount || 0),
        participants,
        answeredUsers: Array.isArray(data.answeredUsers) ? data.answeredUsers : [],
        savedAt: Number(data.savedAt || Date.now()),
        version: Number(data.version || 1),
        finalMessageSent: Boolean(data.finalMessageSent),
        sentChunksCount: Number(data.sentChunksCount || 0),
      });
    }

    return results;
  }

  public async clearAll(): Promise<void> {
    const db = this.getDb();
    const snapshot = await db.collection(this.collectionName).get();
    if (snapshot.empty) return;
    const batch = db.batch();
    snapshot.docs.forEach((doc) => batch.delete(doc.ref));
    await batch.commit();
  }
}

/**
 * Gibrid / Muhitga asoslangan Sessiya Saqlovchisi (SessionStorage)
 *
 * QOIDALAR:
 * 1. NODE_ENV === 'production' bo'lsa:
 *    - Faqat Firestore (FirestoreSessionStorage) ishlatiladi.
 *    - Lokal faylga hech qanday yashirin fallback yo'q!
 *    - DB xatoliklari yutilmaydi, yuqoriga uzatiladi.
 *    - Restartda faqat Firestore'dan o'qiladi, fayldan o'lik sessiyalar qayta tiklanmaydi.
 * 2. NODE_ENV !== 'production' bo'lsa:
 *    - Firebase mavjud bo'lsa Firestore, DATABASE_URL bo'lsa PostgreSQL, bo'lmasa JsonFileSessionStorage ishlatiladi.
 */
export class SessionStorage implements ISessionStorage {
  private fileStore: JsonFileSessionStorage | null = null;
  private firestoreStore: FirestoreSessionStorage | null = null;
  private postgresStore: PostgresSessionStorage | null = null;
  private isProduction: boolean;

  constructor(customFilePath?: string, customFirestoreStore?: FirestoreSessionStorage) {
    this.isProduction = process.env.NODE_ENV === "production";

    if (this.isProduction) {
      this.firestoreStore = customFirestoreStore || new FirestoreSessionStorage();
      this.fileStore = null;
    } else {
      if (customFirestoreStore) {
        this.firestoreStore = customFirestoreStore;
      } else if (process.env.NODE_ENV === "test") {
        // Test processes must never select live storage from developer .env flags.
        this.fileStore = new JsonFileSessionStorage(customFilePath);
      } else if (customFilePath) {
        // Explicit local storage paths are used by isolated tests. Never route
        // them to the live Firestore database merely because .env has credentials.
        this.fileStore = new JsonFileSessionStorage(customFilePath);
      } else if (process.env.FIRESTORE_LOCAL_ENABLED === "true" && getFirestoreDb()) {
        this.firestoreStore = new FirestoreSessionStorage();
      } else if (process.env.DATABASE_URL) {
        this.postgresStore = new PostgresSessionStorage();
      }
      if (!this.fileStore) {
        this.fileStore = new JsonFileSessionStorage();
      }
    }
  }

  public isUsingDatabase(): boolean {
    if (this.isProduction) return true;
    return !!(this.firestoreStore || this.postgresStore);
  }

  public isUsingFirestore(): boolean {
    return this.firestoreStore !== null;
  }

  public getCustomDb(): Firestore | undefined {
    return this.firestoreStore?.getCustomDb();
  }

  public async saveSession(session: QuizSession): Promise<void> {
    if (this.isProduction) {
      if (!this.firestoreStore) {
        throw new Error("[SessionStorage] Productionda faqat Firestore ishlatilishi shart!");
      }
      await this.firestoreStore.saveSession(session);
      return;
    }

    if (this.firestoreStore) {
      await this.firestoreStore.saveSession(session);
    } else if (this.postgresStore) {
      await this.postgresStore.saveSession(session);
    } else if (this.fileStore) {
      await this.fileStore.saveSession(session);
    }
  }

  public async deleteSession(chatId: number): Promise<void> {
    if (this.isProduction) {
      if (!this.firestoreStore) {
        throw new Error("[SessionStorage] Productionda faqat Firestore ishlatilishi shart!");
      }
      await this.firestoreStore.deleteSession(chatId);
      return;
    }

    if (this.firestoreStore) {
      await this.firestoreStore.deleteSession(chatId);
    } else if (this.postgresStore) {
      await this.postgresStore.deleteSession(chatId);
    } else if (this.fileStore) {
      await this.fileStore.deleteSession(chatId);
    }
  }

  public async loadAllSessions(): Promise<SerializedSession[]> {
    if (this.isProduction) {
      if (!this.firestoreStore) {
        throw new Error("[SessionStorage] Productionda faqat Firestore ishlatilishi shart!");
      }
      // Productionda FAQAT Firestore'dan o'qiladi. Agar bazada 0 ta sessiya bo'lsa, [] qaytadi.
      return await this.firestoreStore.loadAllSessions();
    }

    if (this.firestoreStore) {
      return await this.firestoreStore.loadAllSessions();
    }

    if (this.postgresStore) {
      return await this.postgresStore.loadAllSessions();
    }

    if (this.fileStore) {
      return await this.fileStore.loadAllSessions();
    }

    return [];
  }

  public async clearAll(): Promise<void> {
    if (this.firestoreStore) {
      await this.firestoreStore.clearAll();
    }
    if (this.postgresStore) {
      await this.postgresStore.clearAll();
    }
    if (this.fileStore) {
      await this.fileStore.clearAll();
    }
  }
}

export const defaultSessionStorage = new SessionStorage();
