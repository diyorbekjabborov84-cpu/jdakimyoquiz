import assert from "node:assert/strict";
import http from "node:http";
import express from "express";
import { createAdminRouter } from "../src/server/adminRoutes.js";
import {
  createAdminSessionToken,
  verifyAdminSessionToken,
} from "../src/server/adminAuth.js";
import { ADMIN_GOOGLE_EMAIL } from "../src/server/googleAuth.js";
import { recordAuditLog, getAuditLogs } from "../src/server/auditService.js";
import {
  executeBroadcast,
  getBroadcastHistory,
  resolveBroadcastTargets,
} from "../src/server/broadcastService.js";
import {
  getQuizResultsList,
  getSessionLeaderboard,
} from "../src/server/resultsService.js";
import {
  setCustomFirestoreDb,
  resetFirestoreState,
  FIRESTORE_COLLECTIONS,
} from "../src/firebase/firestore.js";
import { EnvConfig } from "../src/config/env.js";

// Mock Firestore yaratish
function createMockFirestore() {
  const collections = new Map<string, Map<string, any>>();

  const getCol = (name: string) => {
    if (!collections.has(name)) {
      collections.set(name, new Map());
    }
    return collections.get(name)!;
  };

  const mockDb = {
    collection(colName: string) {
      const colMap = getCol(colName);
      return {
        doc(id: string) {
          return {
            id,
            async get() {
              const data = colMap.get(String(id));
              return {
                id,
                exists: data !== undefined,
                data: () => (data ? JSON.parse(JSON.stringify(data)) : undefined),
              };
            },
            async set(data: any, options?: { merge?: boolean }) {
              const existing = colMap.get(String(id)) || {};
              const toSave = options?.merge ? { ...existing, ...data } : data;
              colMap.set(String(id), JSON.parse(JSON.stringify(toSave)));
            },
          };
        },
        async add(data: any) {
          const id = `doc_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`;
          colMap.set(id, JSON.parse(JSON.stringify(data)));
          return { id };
        },
        where(field: string, op: string, val: any) {
          return {
            where(f2: string, op2: string, v2: any) {
              return this;
            },
            orderBy() {
              return this;
            },
            limit(n: number) {
              return {
                async get() {
                  const filtered = Array.from(colMap.entries())
                    .filter(([_, d]) => {
                      if (op === "==") return d[field] === val;
                      return true;
                    })
                    .slice(0, n);
                  return {
                    empty: filtered.length === 0,
                    docs: filtered.map(([id, d]) => ({
                      id,
                      data: () => JSON.parse(JSON.stringify(d)),
                    })),
                  };
                },
              };
            },
            count() {
              return {
                async get() {
                  const count = Array.from(colMap.values()).filter((d) => d[field] === val).length;
                  return { data: () => ({ count }) };
                },
              };
            },
            async get() {
              const filtered = Array.from(colMap.entries()).filter(([_, d]) => {
                if (op === "==") return d[field] === val;
                return true;
              });
              return {
                empty: filtered.length === 0,
                docs: filtered.map(([id, d]) => ({
                  id,
                  data: () => JSON.parse(JSON.stringify(d)),
                })),
              };
            },
          };
        },
        orderBy() {
          return {
            limit(n: number) {
              return {
                async get() {
                  const docs = Array.from(colMap.entries())
                    .slice(0, n)
                    .map(([id, d]) => ({
                      id,
                      data: () => JSON.parse(JSON.stringify(d)),
                    }));
                  return { empty: docs.length === 0, docs };
                },
              };
            },
            async get() {
              const docs = Array.from(colMap.entries()).map(([id, d]) => ({
                id,
                data: () => JSON.parse(JSON.stringify(d)),
              }));
              return { empty: docs.length === 0, docs };
            },
          };
        },
        select() {
          return {
            limit(n: number) {
              return {
                async get() {
                  const docs = Array.from(colMap.entries())
                    .slice(0, n)
                    .map(([id, d]) => ({
                      id,
                      data: () => JSON.parse(JSON.stringify(d)),
                    }));
                  return { empty: docs.length === 0, docs };
                },
              };
            },
          };
        },
        limit(n: number) {
          return {
            async get() {
              const docs = Array.from(colMap.entries())
                .slice(0, n)
                .map(([id, d]) => ({
                  id,
                  data: () => JSON.parse(JSON.stringify(d)),
                }));
              return { empty: docs.length === 0, docs };
            },
          };
        },
        async get() {
          const docs = Array.from(colMap.entries()).map(([id, d]) => ({
            id,
            data: () => JSON.parse(JSON.stringify(d)),
          }));
          return { empty: docs.length === 0, docs };
        },
      };
    },
  };

  return { mockDb, collections };
}

async function runTests() {
  console.log("=== Admin Modules (Broadcast, Results, Settings & Google Auth) Testlari ===\n");

  const secret = "a_super_secure_random_admin_session_secret_123456789";

  // 1. Google Direct Login & Session Verification
  console.log("1. Google Direct Login sinovlari...");
  const googleToken = createAdminSessionToken(ADMIN_GOOGLE_EMAIL, ADMIN_GOOGLE_EMAIL, secret);
  assert.ok(googleToken && googleToken.split(".").length === 3);

  // 1.1 ADMIN_TELEGRAM_ID yo'q holatda ham Google admin tasdiqlanishi kerak
  const resNoTg = verifyAdminSessionToken(googleToken, undefined, secret);
  assert.equal(resNoTg.valid, true);
  assert.equal(resNoTg.session?.adminId, ADMIN_GOOGLE_EMAIL);

  // 1.2 ADMIN_TELEGRAM_ID berilgan holatda ham Google admin tasdiqlanishi kerak
  const resWithTg = verifyAdminSessionToken(googleToken, "123456789", secret);
  assert.equal(resWithTg.valid, true);
  console.log("  ✅ Google admin email sessiya tekshiruvidan muvaffaqiyatli o'tdi");

  // 2. Audit Service
  console.log("\n2. Audit Service sinovlari...");
  const logEntry = await recordAuditLog({
    admin: ADMIN_GOOGLE_EMAIL,
    action: "TEST_ACTION",
    details: { foo: "bar" },
  });
  assert.equal(logEntry.admin, ADMIN_GOOGLE_EMAIL);
  assert.equal(logEntry.action, "TEST_ACTION");

  const logs = await getAuditLogs(10);
  assert.ok(logs.length > 0);
  assert.equal(logs[0].action, "TEST_ACTION");
  console.log("  ✅ Audit log yozish va o'qish muvaffaqiyatli ishladi");

  // 3. Broadcast Service & Mock Telegram API
  console.log("\n3. Broadcast Service sinovlari...");
  const { mockDb } = createMockFirestore();
  setCustomFirestoreDb(mockDb as any);

  // Mock guruhlar va userlar kiritamiz
  await mockDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc("-1001").set({
    chatId: -1001,
    title: "Kimyo Guruh 1",
    status: "active",
  });
  await mockDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc("-1002").set({
    chatId: -1002,
    title: "Kimyo Guruh 2",
    status: "active",
  });
  await mockDb.collection(FIRESTORE_COLLECTIONS.USERS).doc("999").set({
    userId: 999,
    firstName: "Ali",
    privateChatActive: true,
  });

  const targets = await resolveBroadcastTargets("all_groups");
  assert.equal(targets.length, 2);

  const userTargets = await resolveBroadcastTargets("private_users");
  assert.equal(userTargets.length, 1);

  const selectedTargets = await resolveBroadcastTargets("selected_groups", [-1001, -1001, -1002]);
  assert.deepEqual(selectedTargets, [-1001, -1002]); // Dublikatlar tozalanadi

  // Mock Telegram API
  const sentMessages: any[] = [];
  const mockApi = {
    async sendMessage(chatId: number, text: string, options: any) {
      // Agar HTML parse mode bo'lsa va xato simulyatsiyasi qilinsa
      if (options?.parse_mode === "HTML" && text.includes("<unclosed_tag>")) {
        const err: any = new Error("Bad Request: can't parse entities");
        err.description = "can't parse entities: Unsupported start tag";
        throw err;
      }
      sentMessages.push({ chatId, text, options });
      return { message_id: 1 };
    },
    async sendPhoto(chatId: number, photo: string, options: any) {
      sentMessages.push({ chatId, photo, options });
      return { message_id: 2 };
    },
  };

  // 3.1 Tugma URL prefiksi va oddiy yuborish
  const bcResult = await executeBroadcast(
    {
      target: "selected_groups",
      selectedChatIds: [-1001, -1002],
      message: "<b>E'lon:</b> Yangi test!",
      buttons: [{ text: "Boshlash", url: "t.me/jdakimyoquizbot" }], // https:// siz kiritilgan URL
      adminUser: ADMIN_GOOGLE_EMAIL,
    },
    mockApi
  );

  assert.equal(bcResult.successful, 2);
  assert.equal(bcResult.failed, 0);
  assert.equal(sentMessages.length, 2);
  assert.equal(sentMessages[0].options.parse_mode, "HTML");
  assert.equal(sentMessages[0].options.reply_markup?.inline_keyboard?.length, 1);
  assert.equal(sentMessages[0].options.reply_markup?.inline_keyboard[0][0].url, "https://t.me/jdakimyoquizbot");

  // 3.2 HTML parsing xatosida plain text fallback sinovi
  const bcFallbackResult = await executeBroadcast(
    {
      target: "selected_groups",
      selectedChatIds: [-1001],
      message: "Xato <unclosed_tag> matn",
      adminUser: ADMIN_GOOGLE_EMAIL,
    },
    mockApi
  );
  assert.equal(bcFallbackResult.successful, 1);
  assert.equal(bcFallbackResult.failed, 0);
  // Oxirgi yuborilgan xabarda parse_mode bo'lmasligi kerak (plain text)
  assert.equal(sentMessages[sentMessages.length - 1].options.parse_mode, undefined);

  const bcHistory = await getBroadcastHistory(10);
  assert.ok(bcHistory.length > 0);
  console.log("  ✅ Broadcast yuborish, deduplikatsiya, URL sanitization va HTML fallback 100% sinovdan o'tdi");

  // 4. Results Service
  console.log("\n4. Results & Leaderboard Service sinovlari...");
  const testSessionId = "sess_test_123";

  await mockDb.collection(FIRESTORE_COLLECTIONS.SESSIONS).doc(testSessionId).set({
    sessionId: testSessionId,
    chatId: -1001,
    quiz: { id: "KK1_1", title: "Kimyoning asosiy tushunchalari 1", questions: new Array(20) },
    status: "finished",
    savedAt: new Date().toISOString(),
    participants: { "1": {}, "2": {} },
  });

  await mockDb.collection(FIRESTORE_COLLECTIONS.RESULTS).doc(`${testSessionId}_1`).set({
    sessionId: testSessionId,
    quizId: "KK1_1",
    chatId: -1001,
    userId: 1,
    firstName: "Zafar",
    username: "zafar_chem",
    score: 18,
    totalQuestions: 20,
    totalTimeMs: 25000,
  });

  await mockDb.collection(FIRESTORE_COLLECTIONS.RESULTS).doc(`${testSessionId}_2`).set({
    sessionId: testSessionId,
    quizId: "KK1_1",
    chatId: -1001,
    userId: 2,
    firstName: "Nodira",
    username: null,
    score: 19,
    totalQuestions: 20,
    totalTimeMs: 30000,
  });

  const resultsList = await getQuizResultsList({ quizId: "KK1_1" });
  assert.ok(resultsList.sessions.length > 0);
  assert.equal(resultsList.sessions[0].quizId, "KK1_1");

  const leaderboardRes = await getSessionLeaderboard(testSessionId);
  assert.equal(leaderboardRes.leaderboard.length, 2);
  // 19 ball olgan Nodira 1-o'rinda bo'lishi kerak
  assert.equal(leaderboardRes.leaderboard[0].rank, 1);
  assert.equal(leaderboardRes.leaderboard[0].name, "Nodira");
  assert.equal(leaderboardRes.leaderboard[0].score, 19);
  assert.equal(leaderboardRes.leaderboard[0].accuracy, 95);

  // 18 ball olgan Zafar 2-o'rinda bo'lishi kerak
  assert.equal(leaderboardRes.leaderboard[1].rank, 2);
  assert.equal(leaderboardRes.leaderboard[1].name, "Zafar");
  assert.equal(leaderboardRes.leaderboard[1].score, 18);
  assert.equal(leaderboardRes.leaderboard[1].accuracy, 90);
  console.log("  ✅ Results ro'yxati va saralangan Leaderboard to'g'ri hisoblandi");

  // 5. Express Router HTTP Endpoints
  console.log("\n5. Express API Routeri HTTP sinovlari...");
  const config: EnvConfig = {
    BOT_TOKEN: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    PORT: 0,
    NODE_ENV: "test",
    ADMIN_SESSION_SECRET: secret,
    ADMIN_TELEGRAM_ID: "123456789",
  };

  const app = express();
  app.use(express.json());
  app.use("/api", createAdminRouter(config, mockApi));

  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const port = (server.address() as any).port;

  const authHeader = { Authorization: `Bearer ${googleToken}` };

  // Helper fetch
  const getJson = async (path: string, headers = authHeader) => {
    const res = await fetch(`http://127.0.0.1:${port}${path}`, { headers });
    return { status: res.status, data: await res.json() };
  };

  const postJson = async (path: string, body: any, headers = authHeader) => {
    const res = await fetch(`http://127.0.0.1:${port}${path}`, {
      method: "POST",
      headers: { ...headers, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return { status: res.status, data: await res.json() };
  };

  // 5.1 Settings endpoint
  const settingsRes = await getJson("/api/admin/settings");
  assert.equal(settingsRes.status, 200);
  assert.equal(settingsRes.data.ok, true);
  assert.equal(settingsRes.data.settings.adminGoogleEmail, ADMIN_GOOGLE_EMAIL);

  // 5.2 Audit logs endpoint
  const logsRes = await getJson("/api/admin/audit-logs");
  assert.equal(logsRes.status, 200);
  assert.equal(logsRes.data.ok, true);
  assert.ok(Array.isArray(logsRes.data.logs));

  // 5.3 Broadcast endpoint
  const bcPost = await postJson("/api/admin/broadcast", {
    target: "selected_groups",
    selectedChatIds: [-1001],
    message: "HTTP broadcast test",
  });
  assert.equal(bcPost.status, 200);
  assert.equal(bcPost.data.ok, true);
  assert.equal(bcPost.data.result.successful, 1);

  // 5.4 Broadcast history endpoint
  const bcHistRes = await getJson("/api/admin/broadcast/history");
  assert.equal(bcHistRes.status, 200);
  assert.equal(bcHistRes.data.ok, true);

  // 5.5 Results list endpoint
  const resList = await getJson("/api/admin/results");
  assert.equal(resList.status, 200);
  assert.equal(resList.data.ok, true);

  // 5.6 Session Leaderboard endpoint
  const lbHttp = await getJson(`/api/admin/results/${testSessionId}`);
  assert.equal(lbHttp.status, 200);
  assert.equal(lbHttp.data.ok, true);
  assert.equal(lbHttp.data.leaderboard.length, 2);

  // 5.7 Auth failure test (yaroqsiz token)
  const unauthRes = await getJson("/api/admin/settings", { Authorization: "Bearer bad_token" });
  assert.equal(unauthRes.status, 401);

  await new Promise<void>((resolve) => server.close(() => resolve()));
  resetFirestoreState();

  console.log("  ✅ Barcha HTTP endpointlari (Settings, Audit, Broadcast, Results) 100% muvaffaqiyatli o'tdi!");
  console.log("\n🎉 Barcha testlar muvaffaqiyatli yakunlandi!");
}

runTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
