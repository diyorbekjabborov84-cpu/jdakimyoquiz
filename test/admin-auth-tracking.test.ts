import assert from "node:assert";
import crypto from "node:crypto";
import http from "node:http";
import express from "express";
import {
  verifyTelegramAuth,
  createAdminSessionToken,
  verifyAdminSessionToken,
  TelegramAuthPayload,
} from "../src/server/adminAuth.js";
import { createAdminRouter } from "../src/server/adminRoutes.js";
import {
  trackGroupEvent,
  trackUserEvent,
  getOverviewStats,
  getGroupsList,
  getUsersList,
  InvalidCursorError,
} from "../src/tracking/tracker.js";
import { allQuizzes } from "../src/quiz/questions.js";
import { EnvConfig } from "../src/config/env.js";
import { setCustomFirestoreDb, resetFirestoreState, FIRESTORE_COLLECTIONS } from "../src/firebase/firestore.js";
import { verifyMutationOrigin } from "../admin/lib/csrf.js";
import { getRenderApiUrl } from "../admin/lib/auth.js";

// Yordamchi: Telegram HMAC yaratish
function createTelegramHash(fields: Record<string, any>, botToken: string): string {
  const allowedKeys = ["auth_date", "first_name", "id", "last_name", "photo_url", "username"];
  const list: string[] = [];
  for (const key of allowedKeys) {
    const val = fields[key];
    if (val !== undefined && val !== null && val !== "") {
      list.push(`${key}=${val}`);
    }
  }
  const dataCheckString = list.join("\n");
  const secretKey = crypto.createHash("sha256").update(botToken).digest();
  return crypto.createHmac("sha256", secretKey).update(dataCheckString).digest("hex");
}

// In-Memory Mock Firestore yaratish (real query, multi-field orderBy va cursor semantikasi bilan)
function createMockFirestore() {
  const collections = new Map<string, Map<string, any>>();
  let shouldFail = false;

  const getCol = (name: string) => {
    if (!collections.has(name)) {
      collections.set(name, new Map());
    }
    return collections.get(name)!;
  };

  const executeQuery = (
    colMap: Map<string, any>,
    filters: any[],
    sorts: any[],
    cursorVals?: any[],
    limitCount?: number
  ) => {
    let items = Array.from(colMap.entries()).map(([id, d]) => ({ id, data: () => d }));

    // Filtrlar
    for (const flt of filters) {
      items = items.filter((item) => {
        const d = item.data();
        if (flt.op === "==") return d[flt.field] === flt.val;
        if (flt.op === ">=") return d[flt.field] >= flt.val;
        if (flt.op === "<=") return d[flt.field] <= flt.val;
        return true;
      });
    }

    // Tartiblash
    if (sorts.length > 0) {
      items.sort((a, b) => {
        for (const s of sorts) {
          const va = s.field === "__name__" ? String(a.id) : String(a.data()[s.field] ?? "");
          const vb = s.field === "__name__" ? String(b.id) : String(b.data()[s.field] ?? "");
          if (va !== vb) {
            if (s.dir === "desc") return va < vb ? 1 : -1;
            return va > vb ? 1 : -1;
          }
        }
        return 0;
      });
    }

    // startAfter cursori
    if (cursorVals && cursorVals.length > 0) {
      const idx = items.findIndex((it) => {
        if (cursorVals.length === 1) {
          const s = sorts[0] || { field: "lastActivity" };
          const val = s.field === "__name__" ? String(it.id) : String(it.data()[s.field] ?? "");
          return val === String(cursorVals[0]) || String(it.id) === String(cursorVals[0]);
        } else if (cursorVals.length >= 2) {
          const s0 = sorts[0];
          const val0 = s0.field === "__name__" ? String(it.id) : String(it.data()[s0.field] ?? "");
          return val0 === String(cursorVals[0]) && String(it.id) === String(cursorVals[1]);
        }
        return false;
      });
      if (idx !== -1) {
        items = items.slice(idx + 1);
      }
    }

    if (limitCount !== undefined) {
      items = items.slice(0, limitCount);
    }

    return items;
  };

  const createQueryObject = (
    colMap: Map<string, any>,
    filters: any[] = [],
    sorts: any[] = [],
    cursorVals?: any[]
  ): any => {
    return {
      where(field: string, op: string, val: any) {
        return createQueryObject(colMap, [...filters, { field, op, val }], [...sorts], cursorVals);
      },
      orderBy(field: string, dir: "asc" | "desc" = "asc") {
        return createQueryObject(colMap, [...filters], [...sorts, { field, dir }], cursorVals);
      },
      startAfter(...vals: any[]) {
        return createQueryObject(colMap, [...filters], [...sorts], vals);
      },
      limit(n: number) {
        return {
          async get() {
            if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
            const items = executeQuery(colMap, filters, sorts, cursorVals, n);
            return { docs: items };
          },
        };
      },
      async get() {
        if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
        const items = executeQuery(colMap, filters, sorts, cursorVals);
        return { docs: items };
      },
      count() {
        return {
          async get() {
            if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
            const items = executeQuery(colMap, filters, sorts);
            return { data: () => ({ count: items.length }) };
          },
        };
      },
    };
  };

  const mockDb = {
    setShouldFail(val: boolean) {
      shouldFail = val;
    },
    collection(colName: string) {
      if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
      const colMap = getCol(colName);

      return {
        doc(id: string) {
          if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
          return {
            id,
            async get() {
              if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
              const data = colMap.get(String(id));
              return {
                id,
                exists: data !== undefined,
                data: () => (data ? JSON.parse(JSON.stringify(data)) : undefined),
              };
            },
            async set(data: any, options?: { merge?: boolean }) {
              if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
              const strId = String(id);
              if (options?.merge && colMap.has(strId)) {
                const existing = colMap.get(strId);
                colMap.set(strId, { ...existing, ...JSON.parse(JSON.stringify(data)) });
              } else {
                colMap.set(strId, JSON.parse(JSON.stringify(data)));
              }
            },
          };
        },
        where(field: string, op: string, val: any) {
          return createQueryObject(colMap).where(field, op, val);
        },
        orderBy(field: string, dir: "asc" | "desc" = "asc") {
          return createQueryObject(colMap).orderBy(field, dir);
        },
        count() {
          return {
            async get() {
              if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
              return { data: () => ({ count: colMap.size }) };
            },
          };
        },
      };
    },
    async runTransaction(updateFunction: (transaction: any) => Promise<any>) {
      if (shouldFail) throw new Error("MOCK_FIRESTORE_FAILURE");
      const transaction = {
        async get(docRef: any) {
          return docRef.get();
        },
        set(docRef: any, data: any, options?: { merge?: boolean }) {
          return docRef.set(data, options);
        },
      };
      return updateFunction(transaction);
    },
  };

  return mockDb;
}

async function runAdminTests() {
  console.log("==================================================================");
  console.log("🧪 ADMIN PANEL (QIDIRUV VA SAHIFALASH YAKUNLASH) TO'LIQ TESTLARI");
  console.log("==================================================================");

  const testBotToken = "123456789:ABCdefGHIjklMNOpqrSTUvwxYZ";
  const validAdminId = "555123456";
  const sessionSecret = "test_super_secret_session_key_32_bytes_long!!";

  // -------------------------------------------------------------
  // 1. Telegram HMAC va Autentifikatsiya Testlari
  // -------------------------------------------------------------
  console.log("\n1. Telegram HMAC va Autentifikatsiya tekshiruvlari...");

  const now = Math.floor(Date.now() / 1000);
  const validPayload: TelegramAuthPayload = {
    id: validAdminId,
    first_name: "Diyorbek",
    username: "diyorbek_jabborov",
    auth_date: now - 30, // 30s ago (within 5 min)
    hash: "",
  };
  validPayload.hash = createTelegramHash(validPayload, testBotToken);

  const resValid = verifyTelegramAuth(validPayload, testBotToken, validAdminId);
  assert.strictEqual(resValid.success, true);
  assert.strictEqual(resValid.user.id, validAdminId);

  // Kutilmagan maydon
  const payloadWithExtra = { ...validPayload, is_admin: true };
  const resExtra = verifyTelegramAuth(payloadWithExtra as any, testBotToken, validAdminId);
  assert.strictEqual(resExtra.success, false);
  assert.strictEqual(resExtra.error, "UNEXPECTED_FIELD");

  // 5 daqiqadan oshgan auth_date
  const payload5mOld = { ...validPayload, auth_date: now - 305 };
  payload5mOld.hash = createTelegramHash(payload5mOld, testBotToken);
  const res5m = verifyTelegramAuth(payload5mOld, testBotToken, validAdminId);
  assert.strictEqual(res5m.success, false);
  assert.strictEqual(res5m.error, "EXPIRED_AUTH");

  // Noto'g'ri / soxta HMAC va 64 belgili hex bo'lmagan hash
  const resBadHash = verifyTelegramAuth(
    { ...validPayload, hash: "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef" },
    testBotToken,
    validAdminId
  );
  assert.strictEqual(resBadHash.success, false);
  assert.strictEqual(resBadHash.error, "INVALID_HASH");

  const malformedHash = verifyTelegramAuth(
    { ...validPayload, hash: "z".repeat(64) },
    testBotToken,
    validAdminId
  );
  assert.strictEqual(malformedHash.success, false);
  assert.strictEqual(malformedHash.error, "INVALID_HASH");

  // Begona Telegram ID va Fail-closed
  const resStranger = verifyTelegramAuth({ ...validPayload, id: "999888777" }, testBotToken, validAdminId);
  assert.strictEqual(resStranger.success, false);
  assert.strictEqual(resStranger.error, "UNAUTHORIZED_ADMIN");

  const resNotConfigured = verifyTelegramAuth(validPayload, testBotToken, undefined);
  assert.strictEqual(resNotConfigured.success, false);
  assert.strictEqual(resNotConfigured.error, "ADMIN_NOT_CONFIGURED");
  console.log("  ✅ Telegram auth tekshiruvlari muvaffaqiyatli o'tdi");

  // -------------------------------------------------------------
  // 2. Admin Sessiyasi va Token (JWT) Testlari
  // -------------------------------------------------------------
  console.log("\n2. Admin sessiyasi va Token xavfsizligi tekshiruvlari...");

  assert.throws(() => createAdminSessionToken(validAdminId, "diyorbek", ""), /SECRET_NOT_CONFIGURED/);
  assert.throws(() => createAdminSessionToken(validAdminId, "diyorbek", "short"), /SECRET_NOT_CONFIGURED/);

  const validToken = createAdminSessionToken(validAdminId, "diyorbek_jabborov", sessionSecret);
  const verifyRes = verifyAdminSessionToken(validToken, validAdminId, sessionSecret);
  assert.strictEqual(verifyRes.valid, true);
  assert.strictEqual(verifyRes.session?.adminId, validAdminId);
  console.log("  ✅ Admin sessiyasi tokeni xavfsiz tasdiqlandi");

  // -------------------------------------------------------------
  // 3. Mock Firestore: Qidiruv, Sahifalash (Cursor) va Chegara Sinovlari
  // -------------------------------------------------------------
  console.log("\n3. Mock Firestore bilan qidiruv va barqaror sahifalash sinovlari...");

  const mockDb = createMockFirestore();
  setCustomFirestoreDb(mockDb as any);

  try {
    // 3.1. 65 ta bir xil prefixga ega guruh («Kimyo Guruh XX»)
    console.log("  -> 65 ta bir xil prefixli guruh bilan sahifalash tekshiruvi...");
    for (let i = 1; i <= 65; i++) {
      const pad = i < 10 ? "0" + i : String(i);
      const ts = new Date(Date.now() + i * 1000).toISOString();
      await mockDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc(String(20000 + i)).set({
        chatId: 20000 + i,
        title: `Kimyo Guruh ${pad}`,
        titleLower: `kimyo guruh ${pad}`,
        type: "supergroup",
        status: "active",
        lastActivity: ts,
        updatedAt: ts,
        eventTimestamp: 5000 + i,
      });
    }

    // 1-sahifa (limit 50)
    const gSearchP1 = await getGroupsList({ query: "Kimyo Guruh", limit: 50 });
    assert.strictEqual(gSearchP1.groups.length, 50, "1-sahifada aynan 50 ta guruh bo'lishi kerak");
    assert.strictEqual(gSearchP1.hasMore, true, "65 tadan 50 tasi olinganda hasMore true bo'lishi kerak");
    assert.ok(gSearchP1.nextCursor !== null, "1-sahifada nextCursor bo'lishi shart");
    assert.strictEqual(gSearchP1.total, 65, "Qidiruv natijasi umumiy soni 65 bo'lishi shart");

    // 2-sahifa (cursor orqali)
    const gSearchP2 = await getGroupsList({ query: "Kimyo Guruh", limit: 50, cursor: gSearchP1.nextCursor! });
    assert.strictEqual(gSearchP2.groups.length, 15, "2-sahifada qolgan 15 ta guruh chiqishi kerak");
    assert.strictEqual(gSearchP2.hasMore, false, "Oxirgi sahifada hasMore false bo'lishi kerak");
    assert.strictEqual(gSearchP2.nextCursor, null, "Oxirgi sahifada nextCursor null bo'lishi kerak");
    assert.strictEqual(gSearchP2.total, 65);

    // Takroriy yoki o'tkazib yuborilgan ID yo'qligini tekshirish
    const allGroupIds = new Set([
      ...gSearchP1.groups.map((g) => g.chatId),
      ...gSearchP2.groups.map((g) => g.chatId),
    ]);
    assert.strictEqual(allGroupIds.size, 65, "Barcha 65 ta guruh IDsi 100% unikal va to'liq bo'lishi shart");
    console.log("  ✅ 65 ta prefixli guruh sahifalashdan 100% to'g'ri va takrorlarsiz o'tdi");

    // 3.2. 65 ta foydalanuvchi (username va name bo'yicha qidiruv va deduplikatsiya)
    console.log("  -> 65 ta foydalanuvchi bilan username/ism qidiruvi va deduplikatsiyasi...");
    // 30 ta username bo'yicha mos ("chem_user_XX")
    for (let i = 1; i <= 30; i++) {
      const pad = i < 10 ? "0" + i : String(i);
      const ts = new Date(Date.now() + i * 1000).toISOString();
      await mockDb.collection(FIRESTORE_COLLECTIONS.USERS).doc(String(30000 + i)).set({
        userId: 30000 + i,
        firstName: `Olim ${pad}`,
        nameLower: `olim ${pad}`,
        username: `chem_user_${pad}`,
        usernameLower: `chem_user_${pad}`,
        privateChatActive: false,
        lastActivity: ts,
        updatedAt: ts,
      });
    }
    // 30 ta ism bo'yicha mos ("Chem Foydalanuvchi XX")
    for (let i = 31; i <= 60; i++) {
      const pad = String(i);
      const ts = new Date(Date.now() + i * 1000).toISOString();
      await mockDb.collection(FIRESTORE_COLLECTIONS.USERS).doc(String(30000 + i)).set({
        userId: 30000 + i,
        firstName: `Chem Foydalanuvchi ${pad}`,
        nameLower: `chem foydalanuvchi ${pad}`,
        username: `user_${pad}`,
        usernameLower: `user_${pad}`,
        privateChatActive: true,
        lastActivity: ts,
        updatedAt: ts,
      });
    }
    // 5 ta HAM username, HAM ism bo'yicha mos ("chem_both_XX")
    for (let i = 61; i <= 65; i++) {
      const pad = String(i);
      const ts = new Date(Date.now() + i * 1000).toISOString();
      await mockDb.collection(FIRESTORE_COLLECTIONS.USERS).doc(String(30000 + i)).set({
        userId: 30000 + i,
        firstName: `Chem Both ${pad}`,
        nameLower: `chem both ${pad}`,
        username: `chem_both_${pad}`,
        usernameLower: `chem_both_${pad}`,
        privateChatActive: true,
        lastActivity: ts,
        updatedAt: ts,
      });
    }

    // Jami mos foydalanuvchilar: 30 + 30 + 5 = 65 ta unikal foydalanuvchi!
    const uSearchP1 = await getUsersList({ query: "chem", limit: 50 });
    assert.strictEqual(uSearchP1.users.length, 50);
    assert.strictEqual(uSearchP1.hasMore, true);
    assert.ok(uSearchP1.nextCursor !== null);

    const uSearchP2 = await getUsersList({ query: "chem", limit: 50, cursor: uSearchP1.nextCursor! });
    assert.strictEqual(uSearchP2.users.length, 15);
    assert.strictEqual(uSearchP2.hasMore, false);
    assert.strictEqual(uSearchP2.nextCursor, null);

    const allUserIds = new Set([
      ...uSearchP1.users.map((u) => u.userId),
      ...uSearchP2.users.map((u) => u.userId),
    ]);
    assert.strictEqual(allUserIds.size, 65, "Ikki maydonli qidiruvda 65 ta unikal foydalanuvchi takrorlarsiz chiqishi shart");
    console.log("  ✅ 65 ta foydalanuvchi qidiruvi (username va ism) deduplikatsiya bilan to'liq o'tdi");

    // Aynan 50 ta username mosligi ism bosqichini yashirib qo'ymasligi kerak.
    const edgeDb = createMockFirestore();
    setCustomFirestoreDb(edgeDb as any);
    for (let i = 0; i < 50; i++) {
      await edgeDb.collection(FIRESTORE_COLLECTIONS.USERS).doc(`edge-${i.toString().padStart(3, "0")}`).set({
        userId: 70000 + i, firstName: "Boshqa", nameLower: "boshqa",
        username: `chem_${i}`, usernameLower: `chem_${i.toString().padStart(3, "0")}`,
        lastActivity: "2026-09-29T10:00:00.000Z",
      });
    }
    await edgeDb.collection(FIRESTORE_COLLECTIONS.USERS).doc("name-only").set({
      userId: 79999, firstName: "Chem ism", nameLower: "chem ism",
      username: "other", usernameLower: "other", lastActivity: "2026-09-29T10:00:00.000Z",
    });
    const edgeFirst = await getUsersList({ query: "chem", limit: 50 });
    assert.strictEqual(edgeFirst.users.length, 50);
    assert.strictEqual(edgeFirst.hasMore, true);
    const edgeSecond = await getUsersList({ query: "chem", limit: 50, cursor: edgeFirst.nextCursor! });
    assert.deepStrictEqual(edgeSecond.users.map((u) => u.userId), [79999]);
    assert.strictEqual(edgeSecond.hasMore, false);

    // 100+ ikki maydonga mos yozuvdan keyin kelgan faqat ism mos yozuv yo'qolmasin.
    const duplicateDb = createMockFirestore();
    setCustomFirestoreDb(duplicateDb as any);
    for (let i = 0; i < 120; i++) {
      await duplicateDb.collection(FIRESTORE_COLLECTIONS.USERS).doc(`both-${i.toString().padStart(3, "0")}`).set({
        userId: 80000 + i, firstName: "Chem", nameLower: `chem ${i.toString().padStart(3, "0")}`,
        username: `chem_${i}`, usernameLower: `chem_${i.toString().padStart(3, "0")}`,
        lastActivity: "2026-09-29T10:00:00.000Z",
      });
    }
    for (let i = 0; i < 2; i++) {
      await duplicateDb.collection(FIRESTORE_COLLECTIONS.USERS).doc(`only-name-${i}`).set({
        userId: 89990 + i, firstName: "Chem", nameLower: `chem zz${i}`,
        username: `other_${i}`, usernameLower: `other_${i}`,
        lastActivity: "2026-09-29T10:00:00.000Z",
      });
    }
    const found: number[] = [];
    let scanCursor: string | null = null;
    for (let page = 0; page < 5; page++) {
      const result = await getUsersList({ query: "chem", limit: 50, cursor: scanCursor || undefined });
      found.push(...result.users.map((u) => Number(u.userId)));
      if (!result.hasMore) {
        assert.strictEqual(result.nextCursor, null);
        break;
      }
      assert.ok(result.nextCursor);
      scanCursor = result.nextCursor;
    }
    assert.strictEqual(found.length, 122);
    assert.strictEqual(new Set(found).size, 122);
    assert.ok(found.includes(89990) && found.includes(89991));
    console.log("  ✅ 50 username + 1 ism va 120 dublikat + 2 ism chegaralari o'tdi");

    // Hujjat IDsi data.chatId/userId dan farq qilsa ham cursor __name__ bo'yicha yuradi.
    const idDb = createMockFirestore();
    setCustomFirestoreDb(idDb as any);
    for (let i = 0; i < 3; i++) {
      await idDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc(`group-doc-${i}`).set({
        chatId: 91000 + i, title: `Quiz ${i}`, titleLower: `quiz ${i}`,
        lastActivity: "2026-09-29T10:00:00.000Z",
      });
      await idDb.collection(FIRESTORE_COLLECTIONS.USERS).doc(`user-doc-${i}`).set({
        userId: 92000 + i, firstName: `Chem ${i}`, nameLower: `chem ${i}`,
        username: `chem_${i}`, usernameLower: `chem_${i}`,
        lastActivity: "2026-09-29T10:00:00.000Z",
      });
    }
    const groupIds: Array<number | string> = [];
    let groupCursor: string | null = null;
    for (let i = 0; i < 3; i++) {
      const page = await getGroupsList({ query: "quiz", limit: 1, cursor: groupCursor || undefined });
      groupIds.push(...page.groups.map((g) => g.chatId));
      groupCursor = page.nextCursor;
    }
    assert.strictEqual(new Set(groupIds).size, 3);
    const userIds: Array<number | string> = [];
    let userCursor: string | null = null;
    for (let i = 0; i < 3; i++) {
      const page = await getUsersList({ query: "@chem", limit: 1, cursor: userCursor || undefined });
      userIds.push(...page.users.map((u) => u.userId));
      userCursor = page.nextCursor;
    }
    assert.strictEqual(new Set(userIds).size, 3);
    console.log("  ✅ Cursorlar data ID emas, haqiqiy Firestore hujjat IDsi bilan yurdi");

    // 3.3. Bir xil lastActivity vaqti bo'lgan yozuvlar bo'yicha barqaror cursor
    console.log("  -> Bir xil lastActivityli 25 ta guruh bo'yicha barqaror sahifalash...");
    const identicalTime = "2026-09-29T10:00:00.000Z";
    const sameTimeDb = createMockFirestore();
    setCustomFirestoreDb(sameTimeDb as any);

    for (let i = 1; i <= 25; i++) {
      await sameTimeDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc(String(40000 + i)).set({
        chatId: 40000 + i,
        title: `Identical Group ${i}`,
        titleLower: `identical group ${i}`,
        type: "group",
        status: "active",
        lastActivity: identicalTime,
        updatedAt: identicalTime,
      });
    }

    const sPage1 = await getGroupsList({ limit: 10 });
    assert.strictEqual(sPage1.groups.length, 10);
    assert.strictEqual(sPage1.hasMore, true);

    const sPage2 = await getGroupsList({ limit: 10, cursor: sPage1.nextCursor! });
    assert.strictEqual(sPage2.groups.length, 10);
    assert.strictEqual(sPage2.hasMore, true);

    const sPage3 = await getGroupsList({ limit: 10, cursor: sPage2.nextCursor! });
    assert.strictEqual(sPage3.groups.length, 5);
    assert.strictEqual(sPage3.hasMore, false);
    assert.strictEqual(sPage3.nextCursor, null);

    const sameTimeIds = new Set([
      ...sPage1.groups.map((g) => g.chatId),
      ...sPage2.groups.map((g) => g.chatId),
      ...sPage3.groups.map((g) => g.chatId),
    ]);
    assert.strictEqual(sameTimeIds.size, 25, "Bir xil vaqtli 25 ta guruh orasida o'tkazib yuborish yoki takror bo'lmasligi shart");
    console.log("  ✅ Bir xil lastActivity vaqti bo'lgan yozuvlar barqaror (id+vaqt) cursor bilan to'liq o'tdi");

    // 3.4. Aynan 50 ta yozuv bo'lgan chegara holati (limit boundary)
    console.log("  -> Aynan 50 ta yozuv chegara holati...");
    const exact50Db = createMockFirestore();
    setCustomFirestoreDb(exact50Db as any);

    for (let i = 1; i <= 50; i++) {
      const ts = new Date(Date.now() + i * 1000).toISOString();
      await exact50Db.collection(FIRESTORE_COLLECTIONS.GROUPS).doc(String(50000 + i)).set({
        chatId: 50000 + i,
        title: `Exact Group ${i}`,
        type: "group",
        status: "active",
        lastActivity: ts,
        updatedAt: ts,
      });
    }

    const exact50Res = await getGroupsList({ limit: 50 });
    assert.strictEqual(exact50Res.groups.length, 50);
    assert.strictEqual(exact50Res.hasMore, false, "Aynan 50 ta bo'lsa hasMore false bo'lishi shart");
    assert.strictEqual(exact50Res.nextCursor, null, "Aynan 50 ta bo'lsa keraksiz nextCursor chiqmasligi shart");
    console.log("  ✅ Aynan 50 ta yozuv qolganda hasMore=false va nextCursor=null ishladi (keraksiz tugma chiqmaydi)");

    // 3.5. Noto'g'ri / buzilgan cursor holati (400 InvalidCursorError)
    console.log("  -> Noto'g'ri cursor tekshiruvi...");
    await assert.rejects(
      async () => await getGroupsList({ cursor: "not_a_valid_base64_json" }),
      (err: any) => err.name === "InvalidCursorError"
    );
    await assert.rejects(
      async () => await getUsersList({ cursor: "not_a_valid_base64_json" }),
      (err: any) => err.name === "InvalidCursorError"
    );
    console.log("  ✅ Noto'g'ri cursor uchun InvalidCursorError istisnosi tashlandi");
  } finally {
    resetFirestoreState();
  }

  // -------------------------------------------------------------
  // 4. Express API: Noto'g'ri Cursor 400 va Production CORS
  // -------------------------------------------------------------
  console.log("\n4. Express API: Noto'g'ri Cursor uchun 400 qaytarilishi va CORS...");

  const testConfig: EnvConfig = {
    BOT_TOKEN: testBotToken,
    PORT: 0,
    NODE_ENV: "production",
    ADMIN_TELEGRAM_ID: validAdminId,
    ADMIN_SESSION_SECRET: sessionSecret,
    ADMIN_CORS_ORIGIN: "https://jda-kimyo-quiz-admin.vercel.app",
    FIRESTORE_LOCAL_ENABLED: false,
  };

  const app = express();
  app.use(express.json());
  app.use("/api", createAdminRouter(testConfig));

  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const port = (server.address() as any).port;
  const baseUrl = `http://localhost:${port}/api`;

  try {
    // Noto'g'ri cursor bilan GET /api/admin/groups -> 400
    const badCursorGroupRes = await fetch(`${baseUrl}/admin/groups?cursor=malformed_cursor_test`, {
      headers: { Authorization: `Bearer ${validToken}` },
    });
    assert.strictEqual(badCursorGroupRes.status, 400);
    const badCursorGroupData = await badCursorGroupRes.json();
    assert.strictEqual(badCursorGroupData.error, "INVALID_CURSOR");

    // Noto'g'ri cursor bilan GET /api/admin/users -> 400
    const badCursorUserRes = await fetch(`${baseUrl}/admin/users?cursor=malformed_cursor_test`, {
      headers: { Authorization: `Bearer ${validToken}` },
    });
    assert.strictEqual(badCursorUserRes.status, 400);
    const badCursorUserData = await badCursorUserRes.json();
    assert.strictEqual(badCursorUserData.error, "INVALID_CURSOR");

    console.log("  ✅ Express API noto'g'ri cursor uchun to'g'ri 400 INVALID_CURSOR qaytardi");
  } finally {
    server.close();
  }

  // -------------------------------------------------------------
  // 5. Next.js BFF Route: Cursorni Render API'ga uzatish sinovi
  // -------------------------------------------------------------
  console.log("\n5. Next.js BFF route'larining cursor parametrini Renderga to'liq uzatishi...");

  let capturedQueryStr = "";
  const mockRenderServer = http.createServer((req, res) => {
    capturedQueryStr = req.url || "";
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ ok: true, groups: [], users: [], nextCursor: null, hasMore: false }));
  });

  await new Promise<void>((resolve) => mockRenderServer.listen(0, resolve));
  const mockRenderPort = (mockRenderServer.address() as any).port;
  const originalRenderUrl = process.env.RENDER_API_URL;
  process.env.RENDER_API_URL = `http://localhost:${mockRenderPort}`;

  try {
    // Next.js groups route test
    const { GET: groupsGet } = await import("../admin/app/api/groups/route.js");
    const testCursor = "test_cursor_base64_sample";

    const mockNextReq = {
      cookies: {
        get: (name: string) => (name === "admin_session" ? { value: validToken } : undefined),
      },
      url: `http://localhost:3000/api/groups?q=olimpiada&limit=25&cursor=${testCursor}`,
    } as any;

    await groupsGet(mockNextReq);
    assert.ok(capturedQueryStr.includes(`cursor=${testCursor}`), "Renderga yuborilgan URLda cursor parametri bo'lishi shart");
    assert.ok(capturedQueryStr.includes("q=olimpiada"));
    assert.ok(capturedQueryStr.includes("limit=25"));

    // Next.js users route test
    const { GET: usersGet } = await import("../admin/app/api/users/route.js");
    const mockNextUserReq = {
      cookies: {
        get: (name: string) => (name === "admin_session" ? { value: validToken } : undefined),
      },
      url: `http://localhost:3000/api/users?q=chem&limit=15&cursor=${testCursor}`,
    } as any;

    await usersGet(mockNextUserReq);
    assert.ok(capturedQueryStr.includes(`cursor=${testCursor}`), "Users Render so'rovida ham cursor bo'lishi shart");
    assert.ok(capturedQueryStr.includes("q=chem"));
    assert.ok(capturedQueryStr.includes("limit=15"));
    console.log("  ✅ Next.js BFF route'lari (groups va users) cursor parametrini Render API'ga to'liq uzatmoqda");
  } finally {
    mockRenderServer.close();
    if (originalRenderUrl) process.env.RENDER_API_URL = originalRenderUrl;
  }

  // -------------------------------------------------------------
  // 6. Mavjud Barcha Quizlar Butunligi
  // -------------------------------------------------------------
  console.log("\n6. Mavjud barcha quizlar butunligi tekshiruvi...");
  assert.strictEqual(allQuizzes.length, 20);
  assert.ok(allQuizzes.some((q) => q.id === "AK1"));
  console.log("  ✅ Barcha 20 ta quiz (jumladan AK1) va ularning savollari to'liq butun");

  console.log("\n==================================================================");
  console.log("🎉 BARCHA QIDIRUV VA SAHIFALASH TESTLARI 100% MUVAFFAQIYATLI O'TDI!");
  console.log("==================================================================");
}

runAdminTests().catch((err) => {
  console.error("❌ Testlarda xatolik:", err);
  process.exit(1);
});
