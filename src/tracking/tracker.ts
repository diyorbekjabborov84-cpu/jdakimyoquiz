import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";
import { allQuizzes } from "../quiz/questions.js";

export interface TrackGroupPayload {
  title?: string;
  type?: string;
  status?: "active" | "left" | "kicked";
  memberCount?: number | null;
  eventTimestamp?: number;
}

export interface TrackUserPayload {
  firstName?: string;
  lastName?: string | null;
  username?: string | null;
  privateChatActive?: boolean;
  eventTimestamp?: number;
}

export interface GroupRecord {
  chatId: number | string;
  title: string;
  type: string;
  status: "active" | "left" | "kicked" | "unknown";
  memberCount: number | null;
  lastActivity: string;
  updatedAt: string;
  statusUpdatedAt?: string;
  createdAt?: string;
  eventTimestamp?: number;
}

export interface BotUserRecord {
  userId: number | string;
  firstName: string;
  lastName: string | null;
  username: string | null;
  privateChatActive: boolean;
  lastActivity: string;
  updatedAt: string;
  createdAt?: string;
  eventTimestamp?: number;
}

export interface GetGroupsOptions {
  query?: string;
  limit?: number;
  cursor?: string;
}

export interface GroupsResult {
  groups: GroupRecord[];
  nextCursor: string | null;
  hasMore: boolean;
  total: number;
}

export interface GetUsersOptions {
  query?: string;
  limit?: number;
  cursor?: string;
}

export interface UsersResult {
  users: BotUserRecord[];
  nextCursor: string | null;
  hasMore: boolean;
  total?: number | null;
}

export class InvalidCursorError extends Error {
  constructor(message = "Cursor parametri yaroqsiz yoki noto'g'ri formatda") {
    super(message);
    this.name = "InvalidCursorError";
  }
}

// In-memory cache for overview stats (30s TTL)
let cachedStats: { data: any; expiresAt: number } | null = null;

// Cursor encode/decode yordamchilari
export function encodeCursor(payload: Record<string, any>): string {
  return Buffer.from(JSON.stringify(payload)).toString("base64url");
}

export function decodeCursor(cursorStr: string): Record<string, any> {
  if (!cursorStr || typeof cursorStr !== "string") {
    throw new InvalidCursorError();
  }
  try {
    const jsonStr = Buffer.from(cursorStr, "base64url").toString("utf-8");
    const data = JSON.parse(jsonStr);
    if (!data || typeof data !== "object") {
      throw new InvalidCursorError();
    }
    return data;
  } catch {
    throw new InvalidCursorError();
  }
}

/**
 * Guruh ma'lumotlarini Firestore'ga ehtiyotkor va asinxron tarzda upsert qilish.
 * Race condition va tartibsiz yetib kelgan hodisalardan transaction orqali himoyalangan.
 */
export async function trackGroupEvent(chatId: number | string, payload: TrackGroupPayload = {}): Promise<void> {
  const db = getFirestoreDb();
  if (!db) return;

  const now = new Date().toISOString();
  const eventTimestamp = payload.eventTimestamp || Date.now();
  const docRef = db.collection(FIRESTORE_COLLECTIONS.GROUPS).doc(String(chatId));

  try {
    await db.runTransaction(async (transaction) => {
      const doc = await transaction.get(docRef);
      const existing = doc.exists ? (doc.data() as Record<string, any>) : null;

      if (existing) {
        const existingEventTime = existing.eventTimestamp || 0;
        // 1. Agar kelgan hodisa bazadagi eng so'nggi hodisadan eskiroq bo'lsa (out-of-order arrival):
        if (eventTimestamp < existingEventTime) {
          return;
        }

        // 2. Agar guruh holati allaqachon left yoki kicked bo'lsa va bu hodisa kechikkan active bo'lsa:
        if (
          (existing.status === "left" || existing.status === "kicked") &&
          payload.status === "active" &&
          eventTimestamp <= existingEventTime
        ) {
          return;
        }
      }

      const updateData: Record<string, any> = {
        chatId: Number(chatId),
        lastActivity: now,
        updatedAt: now,
        eventTimestamp,
      };

      if (payload.title !== undefined) {
        updateData.title = payload.title || "Guruh";
        updateData.titleLower = (payload.title || "Guruh").toLowerCase().trim();
      }
      if (payload.type !== undefined) updateData.type = payload.type;
      if (payload.status !== undefined) {
        updateData.status = payload.status;
        updateData.statusUpdatedAt = now;
      }
      if (payload.memberCount !== undefined) updateData.memberCount = payload.memberCount;

      if (!existing) {
        updateData.createdAt = now;
        if (!updateData.title) {
          updateData.title = "Guruh";
          updateData.titleLower = "guruh";
        }
        if (!updateData.status) updateData.status = "active";
        if (updateData.memberCount === undefined) updateData.memberCount = null;
        transaction.set(docRef, updateData);
      } else {
        transaction.set(docRef, updateData, { merge: true });
      }
    });
  } catch (err: any) {
    console.error(`[Tracker] Guruh ma'lumotini saqlashda xatolik (chatId: ${chatId}):`, err?.message || err);
  }
}

/**
 * Bot foydalanuvchisi ma'lumotlarini Firestore'ga ehtiyotkor va asinxron tarzda upsert qilish.
 */
export async function trackUserEvent(userId: number | string, payload: TrackUserPayload = {}): Promise<void> {
  const db = getFirestoreDb();
  if (!db) return;

  const now = new Date().toISOString();
  const eventTimestamp = payload.eventTimestamp || Date.now();
  const docRef = db.collection(FIRESTORE_COLLECTIONS.USERS).doc(String(userId));

  try {
    await db.runTransaction(async (transaction) => {
      const doc = await transaction.get(docRef);
      const existing = doc.exists ? (doc.data() as Record<string, any>) : null;

      if (existing) {
        const existingEventTime = existing.eventTimestamp || 0;
        if (eventTimestamp < existingEventTime) {
          return;
        }
      }

      const updateData: Record<string, any> = {
        userId: Number(userId),
        lastActivity: now,
        updatedAt: now,
        eventTimestamp,
      };

      if (payload.firstName !== undefined) {
        updateData.firstName = payload.firstName;
        updateData.nameLower = (payload.firstName || "").toLowerCase().trim();
      }
      if (payload.lastName !== undefined) updateData.lastName = payload.lastName;
      if (payload.username !== undefined) {
        updateData.username = payload.username;
        updateData.usernameLower = (payload.username || "").toLowerCase().trim();
      }
      if (payload.privateChatActive !== undefined) updateData.privateChatActive = payload.privateChatActive;

      if (!existing) {
        updateData.createdAt = now;
        if (!updateData.firstName) {
          updateData.firstName = "Foydalanuvchi";
          updateData.nameLower = "foydalanuvchi";
        }
        if (updateData.privateChatActive === undefined) updateData.privateChatActive = false;
        transaction.set(docRef, updateData);
      } else {
        transaction.set(docRef, updateData, { merge: true });
      }
    });
  } catch (err: any) {
    console.error(`[Tracker] Foydalanuvchi ma'lumotini saqlashda xatolik (userId: ${userId}):`, err?.message || err);
  }
}

/**
 * Admin bosh sahifasi uchun qisqacha ko'rsatkichlar (kpi / overview).
 * Xatolar keshlanmaydi; xatolik yuz bersa istisno tashlanadi.
 */
export async function getOverviewStats(forceRefresh = false): Promise<{
  groupsCount: number;
  activeGroupsCount: number;
  totalGroupsCount: number;
  usersCount: number;
  quizzesCount: number;
  resultsCount: number;
  cached: boolean;
}> {
  const now = Date.now();
  if (!forceRefresh && cachedStats && cachedStats.expiresAt > now) {
    return { ...cachedStats.data, cached: true };
  }

  const db = getFirestoreDb();
  if (!db) {
    throw new Error("DATABASE_NOT_INITIALIZED");
  }

  // Firestore count() aggregatsiyalari
  const [activeGroupsSnap, totalGroupsSnap, usersSnap, resultsSnap] = await Promise.all([
    db.collection(FIRESTORE_COLLECTIONS.GROUPS).where("status", "==", "active").count().get(),
    db.collection(FIRESTORE_COLLECTIONS.GROUPS).count().get(),
    db.collection(FIRESTORE_COLLECTIONS.USERS).count().get(),
    db.collection(FIRESTORE_COLLECTIONS.RESULTS).count().get(),
  ]);

  const activeGroupsCount = activeGroupsSnap.data().count;
  const totalGroupsCount = totalGroupsSnap.data().count;
  const usersCount = usersSnap.data().count;
  const resultsCount = resultsSnap.data().count;

  const data = {
    groupsCount: activeGroupsCount, // Faol guruhlar
    activeGroupsCount,
    totalGroupsCount, // Barcha tarixiy guruhlar
    usersCount,
    quizzesCount: allQuizzes.length,
    resultsCount,
  };

  // Faqat barcha so'rovlar muvaffaqiyatli bo'lsagina 30 soniyalik keshga qo'yiladi
  cachedStats = {
    data,
    expiresAt: now + 30_000,
  };

  return { ...data, cached: false };
}

/**
 * Guruhlarning ro'yxatini olish (server qidiruvi, barqaror cursor va limit+1 sahifalash)
 */
export async function getGroupsList(options: GetGroupsOptions = {}): Promise<GroupsResult> {
  const parsedCursor = options.cursor ? decodeCursor(options.cursor) : null;

  const db = getFirestoreDb();
  if (!db) {
    throw new Error("DATABASE_NOT_INITIALIZED");
  }

  const limit = Math.min(Math.max(options.limit || 50, 1), 100);
  const groupsCol = db.collection(FIRESTORE_COLLECTIONS.GROUPS);

  const q = options.query?.trim();

  // 1. Aniq sonli Chat ID bo'yicha qidiruv (masalan: -10012345678 yoki 123456)
  if (q && /^-?\d+$/.test(q)) {
    const idDoc = await groupsCol.doc(q).get();
    if (idDoc.exists) {
      const data = idDoc.data()!;
      return {
        groups: [
          {
            chatId: data.chatId ?? idDoc.id,
            title: data.title || "Nomsiz guruh",
            type: data.type || "group",
            status: data.status || "active",
            memberCount: data.memberCount ?? null,
            lastActivity: data.lastActivity || data.updatedAt || "",
            updatedAt: data.updatedAt || "",
            statusUpdatedAt: data.statusUpdatedAt,
            createdAt: data.createdAt,
          },
        ],
        nextCursor: null,
        hasMore: false,
        total: 1,
      };
    }
    return {
      groups: [],
      nextCursor: null,
      hasMore: false,
      total: 0,
    };
  }

  // 2. Matnli qidiruv (guruh sarlavhasi prefixi)
  if (q) {
    const qLower = q.toLowerCase();
    const queryBase = groupsCol
      .where("titleLower", ">=", qLower)
      .where("titleLower", "<=", qLower + "\uf8ff");

    // Aniq qidiruv natijalarining umumiy soni
    const countSnap = await queryBase.count().get();
    const totalMatching = countSnap.data().count;

    let queryRef = queryBase
      .orderBy("titleLower", "asc")
      .orderBy("__name__", "asc");

    if (parsedCursor) {
      if (parsedCursor.type !== "group_search" || parsedCursor.q !== qLower || !parsedCursor.titleLower || !parsedCursor.id) {
        throw new InvalidCursorError();
      }
      queryRef = queryRef.startAfter(parsedCursor.titleLower, parsedCursor.id);
    }

    // Sahifa mavjudligini limit + 1 yozuv orqali aniqlash
    const snapshot = await queryRef.limit(limit + 1).get();
    const hasMore = snapshot.docs.length > limit;
    const docs = hasMore ? snapshot.docs.slice(0, limit) : snapshot.docs;

    const items: GroupRecord[] = docs.map((doc: any) => {
      const data = doc.data();
      return {
        chatId: data.chatId ?? doc.id,
        title: data.title || "Nomsiz guruh",
        type: data.type || "group",
        status: data.status || "active",
        memberCount: data.memberCount ?? null,
        lastActivity: data.lastActivity || data.updatedAt || "",
        updatedAt: data.updatedAt || "",
        statusUpdatedAt: data.statusUpdatedAt,
        createdAt: data.createdAt,
      };
    });

    const lastDoc = docs[docs.length - 1];
    const nextCursor =
      hasMore && lastDoc
        ? encodeCursor({
            type: "group_search",
            q: qLower,
            titleLower: lastDoc.data().titleLower,
            id: lastDoc.id,
          })
        : null;

    return {
      groups: items,
      nextCursor,
      hasMore,
      total: totalMatching,
    };
  }

  // 3. Standart tartiblangan ro'yxat (lastActivity desc + __name__ desc barqaror tartib)
  const totalSnap = await groupsCol.count().get();
  const totalCount = totalSnap.data().count;

  let queryRef = groupsCol
    .orderBy("lastActivity", "desc")
    .orderBy("__name__", "desc");

  if (parsedCursor) {
    if (parsedCursor.type !== "group_list" || !parsedCursor.lastActivity || !parsedCursor.id) {
      throw new InvalidCursorError();
    }
    queryRef = queryRef.startAfter(parsedCursor.lastActivity, parsedCursor.id);
  }

  // limit + 1 orqali aniq hasMore aniqlash
  const snapshot = await queryRef.limit(limit + 1).get();
  const hasMore = snapshot.docs.length > limit;
  const docs = hasMore ? snapshot.docs.slice(0, limit) : snapshot.docs;

  const items: GroupRecord[] = docs.map((doc: any) => {
    const data = doc.data();
    return {
      chatId: data.chatId ?? doc.id,
      title: data.title || "Nomsiz guruh",
      type: data.type || "group",
      status: data.status || "active",
      memberCount: data.memberCount ?? null,
      lastActivity: data.lastActivity || data.updatedAt || "",
      updatedAt: data.updatedAt || "",
      statusUpdatedAt: data.statusUpdatedAt,
      createdAt: data.createdAt,
    };
  });

  const lastDoc = docs[docs.length - 1];
  const nextCursor =
    hasMore && lastDoc
      ? encodeCursor({
          type: "group_list",
          lastActivity: lastDoc.data().lastActivity,
          id: lastDoc.id,
        })
      : null;

  return {
    groups: items,
    nextCursor,
    hasMore,
    total: totalCount,
  };
}

/**
 * Ma'lum foydalanuvchilar ro'yxatini olish (server qidiruvi, barqaror cursor va limit+1 sahifalash)
 */
export async function getUsersList(options: GetUsersOptions = {}): Promise<UsersResult> {
  const parsedCursor = options.cursor ? decodeCursor(options.cursor) : null;

  const db = getFirestoreDb();
  if (!db) {
    throw new Error("DATABASE_NOT_INITIALIZED");
  }

  const limit = Math.min(Math.max(options.limit || 50, 1), 100);
  const usersCol = db.collection(FIRESTORE_COLLECTIONS.USERS);

  const q = options.query?.trim();

  // 1. Aniq Telegram raqamli ID bo'yicha qidiruv
  if (q && /^\d+$/.test(q)) {
    const idDoc = await usersCol.doc(q).get();
    if (idDoc.exists) {
      const data = idDoc.data()!;
      return {
        users: [
          {
            userId: data.userId ?? idDoc.id,
            firstName: data.firstName || "Foydalanuvchi",
            lastName: data.lastName ?? null,
            username: data.username ?? null,
            privateChatActive: Boolean(data.privateChatActive),
            lastActivity: data.lastActivity || data.updatedAt || "",
            updatedAt: data.updatedAt || "",
            createdAt: data.createdAt,
          },
        ],
        nextCursor: null,
        hasMore: false,
        total: 1,
      };
    }
    return {
      users: [],
      nextCursor: null,
      hasMore: false,
      total: 0,
    };
  }

  // 2. Username yoki ism prefixi bo'yicha qidiruv
  if (q) {
    let cleanQ = q.toLowerCase();
    const isExplicitUsername = cleanQ.startsWith("@");
    if (isExplicitUsername) cleanQ = cleanQ.substring(1);

    if (isExplicitUsername) {
      // Faqat username bo'yicha qidiruv
      const queryBase = usersCol
        .where("usernameLower", ">=", cleanQ)
        .where("usernameLower", "<=", cleanQ + "\uf8ff");

      const countSnap = await queryBase.count().get();
      const totalMatching = countSnap.data().count;

      let queryRef = queryBase
        .orderBy("usernameLower", "asc")
        .orderBy("__name__", "asc");

      if (parsedCursor) {
        if (parsedCursor.type !== "user_search_username" || parsedCursor.q !== cleanQ || !parsedCursor.usernameLower || !parsedCursor.id) {
          throw new InvalidCursorError();
        }
        queryRef = queryRef.startAfter(parsedCursor.usernameLower, parsedCursor.id);
      }

      const snapshot = await queryRef.limit(limit + 1).get();
      const hasMore = snapshot.docs.length > limit;
      const docs = hasMore ? snapshot.docs.slice(0, limit) : snapshot.docs;

      const items: BotUserRecord[] = docs.map((doc: any) => {
        const data = doc.data();
        return {
          userId: data.userId ?? doc.id,
          firstName: data.firstName || "Foydalanuvchi",
          lastName: data.lastName ?? null,
          username: data.username ?? null,
          privateChatActive: Boolean(data.privateChatActive),
          lastActivity: data.lastActivity || data.updatedAt || "",
          updatedAt: data.updatedAt || "",
          createdAt: data.createdAt,
        };
      });

      const lastDoc = docs[docs.length - 1];
      const nextCursor =
        hasMore && lastDoc
          ? encodeCursor({
              type: "user_search_username",
              q: cleanQ,
              usernameLower: lastDoc.data().usernameLower,
              id: lastDoc.id,
            })
          : null;

      return {
        users: items,
        nextCursor,
        hasMore,
        total: totalMatching,
      };
    }

    // Username mosliklari avval, faqat ismga moslar keyin. Har ikkala oqimni
    // limit+1 ta UNIKAL yozuv topilguncha o'qiymiz; dublikatlar sahifani yemaydi.
    if (parsedCursor && (
      parsedCursor.type !== "user_search_multi" || parsedCursor.q !== cleanQ ||
      !["username", "name"].includes(parsedCursor.stage) ||
      typeof parsedCursor.val !== "string" || !parsedCursor.val ||
      typeof parsedCursor.id !== "string" || !parsedCursor.id
    )) {
      throw new InvalidCursorError();
    }

    type SearchHit = { doc: any; stage: "username" | "name"; val: string };
    const hits: SearchHit[] = [];
    const batchSize = Math.max(limit + 1, 100);

    for (const stage of ["username", "name"] as const) {
      if (parsedCursor?.stage === "name" && stage === "username") continue;

      const field = stage === "username" ? "usernameLower" : "nameLower";
      let afterVal = parsedCursor?.stage === stage ? parsedCursor.val : undefined;
      let afterId = parsedCursor?.stage === stage ? parsedCursor.id : undefined;

      while (hits.length <= limit) {
        let queryRef = usersCol
          .where(field, ">=", cleanQ)
          .where(field, "<=", cleanQ + "\uf8ff")
          .orderBy(field, "asc")
          .orderBy("__name__", "asc");
        if (afterVal && afterId) queryRef = queryRef.startAfter(afterVal, afterId);

        const snap = await queryRef.limit(batchSize).get();
        if (snap.docs.length === 0) break;

        for (const doc of snap.docs) {
          const data = doc.data();
          afterVal = data[field];
          afterId = doc.id;
          if (stage === "name") {
            const username = data.usernameLower || "";
            if (username >= cleanQ && username <= cleanQ + "\uf8ff") continue;
          }
          hits.push({ doc, stage, val: data[field] });
          if (hits.length > limit) break;
        }

        if (hits.length > limit || snap.docs.length < batchSize) break;
      }
      if (hits.length > limit) break;
    }

    const hasMore = hits.length > limit;
    const pageHits = hits.slice(0, limit);
    const users: BotUserRecord[] = pageHits.map(({ doc }) => {
      const data = doc.data();
      return {
        userId: data.userId ?? doc.id,
        firstName: data.firstName || "Foydalanuvchi",
        lastName: data.lastName ?? null,
        username: data.username ?? null,
        privateChatActive: Boolean(data.privateChatActive),
        lastActivity: data.lastActivity || data.updatedAt || "",
        updatedAt: data.updatedAt || "",
        createdAt: data.createdAt,
      };
    });
    const lastHit = pageHits[pageHits.length - 1];
    const nextCursor = hasMore && lastHit ? encodeCursor({
      type: "user_search_multi",
      q: cleanQ,
      stage: lastHit.stage,
      val: lastHit.val,
      id: lastHit.doc.id,
    }) : null;

    return { users, nextCursor, hasMore, total: null };
  }

  // 3. Standart tartiblangan ro'yxat (lastActivity desc + __name__ desc)
  const totalSnap = await usersCol.count().get();
  const totalCount = totalSnap.data().count;

  let queryRef = usersCol
    .orderBy("lastActivity", "desc")
    .orderBy("__name__", "desc");

  if (parsedCursor) {
    if (parsedCursor.type !== "user_list" || !parsedCursor.lastActivity || !parsedCursor.id) {
      throw new InvalidCursorError();
    }
    queryRef = queryRef.startAfter(parsedCursor.lastActivity, parsedCursor.id);
  }

  const snapshot = await queryRef.limit(limit + 1).get();
  const hasMore = snapshot.docs.length > limit;
  const docs = hasMore ? snapshot.docs.slice(0, limit) : snapshot.docs;

  const items: BotUserRecord[] = docs.map((doc: any) => {
    const data = doc.data();
    return {
      userId: data.userId ?? doc.id,
      firstName: data.firstName || "Foydalanuvchi",
      lastName: data.lastName ?? null,
      username: data.username ?? null,
      privateChatActive: Boolean(data.privateChatActive),
      lastActivity: data.lastActivity || data.updatedAt || "",
      updatedAt: data.updatedAt || "",
      createdAt: data.createdAt,
    };
  });

  const lastDoc = docs[docs.length - 1];
  const nextCursor =
    hasMore && lastDoc
      ? encodeCursor({
          type: "user_list",
          lastActivity: lastDoc.data().lastActivity,
          id: lastDoc.id,
        })
      : null;

  return {
    users: items,
    nextCursor,
    hasMore,
    total: totalCount,
  };
}
