import assert from "node:assert/strict";
import http from "node:http";
import express from "express";
import { createAdminRouter } from "../src/server/adminRoutes.js";
import { createAdminSessionToken } from "../src/server/adminAuth.js";
import { ADMIN_GOOGLE_EMAIL } from "../src/server/googleAuth.js";
import { getAuditLogs } from "../src/server/auditService.js";
import {
  setCustomFirestoreDb,
  resetFirestoreState,
  FIRESTORE_COLLECTIONS,
} from "../src/firebase/firestore.js";
import { EnvConfig } from "../src/config/env.js";
import {
  resolveShell,
  setGroupShellMode,
  addKursParticipant,
  updateKursParticipantBlockStatus,
  resetShellStateForTest,
} from "../src/shell/shell.js";
import {
  resetBotSettingsState,
  getBotSettings,
} from "../src/settings/botSettings.js";
import {
  validateKursDarslarPayload,
  populateKursMemory,
  clearKursDarslarForTest,
  getKursQuizById,
} from "../src/kurs/kursRepository.js";
import { uploadKursBankToFirestore } from "../src/kurs/yuklaScript.js";
import { handleStart } from "../src/bot/handlers/start.js";
import {
  handleQuizCommand,
  handleStopQuizCommand,
  startQuizById,
} from "../src/bot/handlers/quiz.js";
import { handleMenuCallback } from "../src/bot/handlers/menu.js";
import { quizManager, TelegramApiSender } from "../src/quiz/quizManager.js";

// ============================================================================
// Fake Fixture Data (hech qachon haqiqiy test_bank.json ishlatilmaydi!)
// ============================================================================
function createFakeKursBank() {
  const makeQuestions = (dars: number, count = 12) =>
    Array.from({ length: count }, (_, idx) => ({
      id: `FAKE_D0${dars}_T${String(idx + 1).padStart(2, "0")}`,
      savol: `Sinov darsi #${dars}, savol #${idx + 1}?`,
      variantlar: {
        A: `Variant A (${dars}.${idx + 1})`,
        B: `Variant B (${dars}.${idx + 1})`,
        C: `Variant C (${dars}.${idx + 1})`,
        D: `Variant D (${dars}.${idx + 1})`,
      },
      javob: (["A", "B", "C", "D"] as const)[idx % 4],
      qiyinlik: "oson",
    }));

  return {
    kurs: "Kimyo 0 dan (Fixture)",
    yangilangan: "2026-04-12",
    darslar: [
      {
        dars: 1,
        mavzu: "1-mavzu (Sinov fixture)",
        papka: "01-dars_sinov",
        testlar: makeQuestions(1, 12),
        mashqlar: [{ id: "FAKE_D01_M01", savol: "Mashq 1", yechim: "Yechim 1" }],
      },
      {
        dars: 2,
        mavzu: "2-mavzu (Sinov fixture)",
        papka: "02-dars_sinov",
        testlar: makeQuestions(2, 12),
        mashqlar: [],
      },
    ],
  };
}

function createMockFirestore() {
  const collections = new Map<string, Map<string, any>>();
  let shouldThrowError = false;

  const getCol = (name: string) => {
    if (!collections.has(name)) {
      collections.set(name, new Map());
    }
    return collections.get(name)!;
  };

  const mockDb = {
    setShouldThrow(flag: boolean) {
      shouldThrowError = flag;
    },
    async runTransaction(fn: (tx: any) => Promise<any>) {
      const tx = {
        async get(docRef: any) {
          return docRef.get();
        },
        set(docRef: any, data: any, options?: { merge?: boolean }) {
          return docRef.set(data, options);
        },
      };
      return fn(tx);
    },
    collection(colName: string) {
      const colMap = getCol(colName);
      return {
        doc(id: string) {
          return {
            id,
            async get() {
              if (shouldThrowError) throw new Error("Simulated Firestore Error");
              const data = colMap.get(String(id));
              return {
                id,
                exists: data !== undefined,
                data: () => (data ? JSON.parse(JSON.stringify(data)) : undefined),
              };
            },
            async set(data: any, options?: { merge?: boolean }) {
              if (shouldThrowError) throw new Error("Simulated Firestore Error");
              const existing = colMap.get(String(id)) || {};
              const toSave = options?.merge ? { ...existing, ...data } : data;
              colMap.set(String(id), JSON.parse(JSON.stringify(toSave)));
            },
            async delete() {
              if (shouldThrowError) throw new Error("Simulated Firestore Error");
              colMap.delete(String(id));
            },
          };
        },
        where(field: string, op: string, val: any) {
          return {
            async get() {
              if (shouldThrowError) throw new Error("Simulated Firestore Error");
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
            count() {
              return {
                async get() {
                  const count = Array.from(colMap.values()).filter((d) => d[field] === val).length;
                  return { data: () => ({ count }) };
                },
              };
            },
          };
        },
        orderBy() {
          return {
            orderBy() {
              return this;
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
          };
        },
        count() {
          return {
            async get() {
              return { data: () => ({ count: colMap.size }) };
            },
          };
        },
        async add(data: any) {
          const id = `doc_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
          colMap.set(id, JSON.parse(JSON.stringify(data)));
          return { id };
        },
        async get() {
          if (shouldThrowError) throw new Error("Simulated Firestore Error");
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

class KursTestApi implements TelegramApiSender {
  public memberCount = 15;
  public groupMemberships = new Map<string, string>(); // "${chatId}:${userId}" -> status
  public shouldFailGetChatMember = false;
  public sentMessages: Array<{ chatId: number | string; text: string; other?: any }> = [];
  public sentPolls: Array<{
    chatId: number | string;
    question: string;
    options: string[];
    other?: Record<string, any>;
    messageId: number;
    pollId: string;
  }> = [];

  private nextMsgId = 100;
  private nextPollId = 1;

  async getChatMemberCount(_chatId: number | string) {
    return this.memberCount;
  }

  async getChatMember(chatId: number | string, userId: number) {
    if (this.shouldFailGetChatMember) {
      throw new Error("Simulated Telegram API network timeout");
    }
    const status = this.groupMemberships.get(`${chatId}:${userId}`) || "left";
    return { status, user: { id: userId } };
  }

  async sendPoll(
    chatId: number | string,
    question: string,
    options: string[],
    other?: Record<string, any>
  ) {
    const messageId = this.nextMsgId++;
    const pollId = `kurs_poll_${this.nextPollId++}`;
    this.sentPolls.push({ chatId, question, options, other, messageId, pollId });
    return { message_id: messageId, poll: { id: pollId } };
  }

  async stopPoll(_chatId: number | string, _messageId: number) {
    return { is_closed: true };
  }

  async sendMessage(chatId: number | string, text: string, other?: Record<string, any>) {
    this.sentMessages.push({ chatId, text, other });
    return { message_id: this.nextMsgId++, text };
  }
}

function makeCtx(params: {
  chatId: number;
  chatType: "private" | "group" | "supergroup";
  userId: number;
  firstName?: string;
  isAdmin?: boolean;
  text?: string;
  match?: string;
  callbackData?: string;
  api: KursTestApi;
}) {
  const replies: Array<{ text: string; other?: any }> = [];
  const edits: Array<{ text: string; other?: any }> = [];
  const alerts: Array<{ text?: string; show_alert?: boolean }> = [];

  return {
    chat: { id: params.chatId, type: params.chatType, title: "Test Chat" },
    from: { id: params.userId, first_name: params.firstName || "Talaba" },
    me: { id: 999999, username: "jdakimyoquizbot" },
    match: params.match ?? "",
    message: { text: params.text ?? "" },
    callbackQuery: params.callbackData ? { data: params.callbackData } : undefined,
    api: params.api,
    replies,
    edits,
    alerts,
    reply: async (text: string, other?: any) => {
      replies.push({ text, other });
      return { message_id: 500, text };
    },
    editMessageText: async (text: string, other?: any) => {
      edits.push({ text, other });
      return { message_id: 500, text };
    },
    answerCallbackQuery: async (p?: { text?: string; show_alert?: boolean }) => {
      alerts.push(p || {});
      return true;
    },
    getChatMember: async (userId: number) => ({
      status: params.isAdmin ? "administrator" : "member",
      user: { id: userId },
    }),
  };
}

async function runKursQobiqTests() {
  console.log("=== Kurs Qobig'i («Kimyo 0 dan») va Ikki Qobiqli Arxitektura Testlari ===\n");

  const { mockDb } = createMockFirestore();
  setCustomFirestoreDb(mockDb as any);
  resetShellStateForTest();
  resetBotSettingsState();
  clearKursDarslarForTest();

  const api = new KursTestApi();

  // 1. Validatsiya va Firestore yuklash sinovi
  console.log("1. Yuklash skripti va test banki validatsiyasi...");
  const badValidation = validateKursDarslarPayload([
    {
      dars: 1,
      mavzu: "Xato dars",
      testlar: [
        {
          id: "DUP_1",
          savol: "Savol 1",
          variantlar: { A: "1", B: "2", C: "3", D: "" }, // D bo'sh
          javob: "E" as any, // noto'g'ri javob
        },
      ],
    },
  ]);
  assert.equal(badValidation.valid, false);
  assert.ok(badValidation.errors.length > 0);

  const fakeBank = createFakeKursBank();
  const uploadRes = await uploadKursBankToFirestore(fakeBank);
  assert.equal(uploadRes.uploadedLessons, 2);
  assert.equal(uploadRes.totalQuestions, 24);

  populateKursMemory(uploadRes.validated);
  const d1Quiz = getKursQuizById("KURS_D01");
  assert.ok(d1Quiz);
  assert.equal(d1Quiz.questions.length, 12);
  assert.equal(d1Quiz.questions[0].timeLimitSeconds, 30);
  assert.ok(d1Quiz.questions[0].explanation?.includes("📺 1-dars:"));
  assert.ok((d1Quiz.questions[0].explanation?.length || 0) <= 200);
  console.log("  ✅ Yuklash skripti va 30s/izoh formatlash to'g'ri ishladi");

  // 2. Guruh rejimlari: asosiy, kurs, ochiq_emas va qobiq izolatsiyasi
  console.log("\n2. Guruh rejimlari (asosiy, kurs, ochiq_emas) va qobiq izolatsiyasi...");
  const asosiyGroupId = -1001001;
  const kursGroupId = -1002002;
  const disabledGroupId = -1003003;

  await setGroupShellMode(asosiyGroupId, "asosiy");
  await setGroupShellMode(kursGroupId, "kurs");
  await setGroupShellMode(disabledGroupId, "ochiq_emas");

  // 2.1 Asosiy guruhda kurs testi rad etilishi
  const ctxAsosiyTryKurs = makeCtx({
    chatId: asosiyGroupId,
    chatType: "supergroup",
    userId: 101,
    api,
  });
  await startQuizById(ctxAsosiyTryKurs as any, "KURS_D01");
  assert.equal(quizManager.isQuizActive(asosiyGroupId), false);
  assert.ok(ctxAsosiyTryKurs.replies[0].text.includes("faqat «Kimyo 0 dan» kursi"));

  // 2.2 Kurs guruhida asosiy test rad etilishi
  const ctxKursTryAsosiy = makeCtx({
    chatId: kursGroupId,
    chatType: "supergroup",
    userId: 102,
    api,
  });
  await startQuizById(ctxKursTryAsosiy as any, "KK1_1");
  assert.equal(quizManager.isQuizActive(kursGroupId), false);
  assert.ok(ctxKursTryAsosiy.replies[0].text.includes("faqat «Kimyo 0 dan» kursi testlari ishlaydi"));

  // 2.3 Kurs guruhida guruh a'zolari < 12 bo'lsa ham kurs testi boshlanishi (Q5)
  api.memberCount = 3; // 3 kishi (< 12)
  const ctxKursStartQuiz = makeCtx({
    chatId: kursGroupId,
    chatType: "supergroup",
    userId: 102,
    isAdmin: true,
    api,
  });
  await startQuizById(ctxKursStartQuiz as any, "KURS_D01");
  assert.equal(quizManager.isQuizActive(kursGroupId), true, "Kurs guruhida 3 kishi bilan ham test boshlanishi shart");
  await handleStopQuizCommand(ctxKursStartQuiz as any);
  api.memberCount = 15;

  // 2.4 ochiq_emas guruhda bir marta ogohlantirish va spam qilmaslik
  const ctxDisabled1 = makeCtx({
    chatId: disabledGroupId,
    chatType: "supergroup",
    userId: 103,
    api,
  });
  await handleStart(ctxDisabled1 as any);
  assert.equal(ctxDisabled1.replies.length, 1);
  assert.ok(ctxDisabled1.replies[0].text.includes("Bu guruhda bot faol emas"));

  const ctxDisabled2 = makeCtx({
    chatId: disabledGroupId,
    chatType: "supergroup",
    userId: 103,
    api,
  });
  await handleQuizCommand(ctxDisabled2 as any);
  assert.equal(ctxDisabled2.replies.length, 0, "Ikkinchi marta spam xabar yuborilmasligi kerak");
  console.log("  ✅ Guruh rejimlari va qobiq izolatsiyasi 100% ishladi");

  // 3. Shaxsiy chat ruxsatlari: guruh a'zosi, qo'lda qo'shilgan, bloklangan, fail-closed
  console.log("\n3. Shaxsiy chat ruxsatlari, bloklash ustunligi va fail-closed xavfsizlik...");
  const groupMemberUserId = 5001;
  const manualUserId = 5002;
  const outsiderUserId = 5003;

  // 3.1 Kurs guruhi a'zosi shaxsiy chatda ruxsat oladi
  api.groupMemberships.set(`${kursGroupId}:${groupMemberUserId}`, "member");
  const ctxMemberPrivate = makeCtx({
    chatId: groupMemberUserId,
    chatType: "private",
    userId: groupMemberUserId,
    api,
  });
  const memberShell = await resolveShell(ctxMemberPrivate as any);
  assert.deepEqual(memberShell, { shell: "kurs", context: "private" });

  // 3.2 Guruh a'zosi kurs_ishtirokchilari da bloklangan bo'lsa, rad etiladi!
  await addKursParticipant({ userId: groupMemberUserId, ism: "Bloklanuvchi" });
  await updateKursParticipantBlockStatus(groupMemberUserId, true);
  const blockedShell = await resolveShell(ctxMemberPrivate as any);
  assert.deepEqual(blockedShell, { shell: "yopiq", reason: "blocked" });

  // 3.3 Qo'lda qo'shilgan ishtirokchi (bloklangan: false) ruxsat oladi
  await addKursParticipant({ userId: manualUserId, ism: "Qo'lda qo'shilgan" });
  const ctxManualPrivate = makeCtx({
    chatId: manualUserId,
    chatType: "private",
    userId: manualUserId,
    api,
  });
  const manualShell = await resolveShell(ctxManualPrivate as any);
  assert.deepEqual(manualShell, { shell: "kurs", context: "private" });

  // 3.4 Fail-closed: Telegram API getChatMember xato berganda reason: "check_error"
  api.shouldFailGetChatMember = true;
  const ctxErrorPrivate = makeCtx({
    chatId: outsiderUserId,
    chatType: "private",
    userId: outsiderUserId,
    api,
  });
  await handleStart(ctxErrorPrivate as any);
  assert.equal(ctxErrorPrivate.replies.length, 1);
  assert.ok(ctxErrorPrivate.replies[0].text.includes("Hozir tekshirib bo‘lmadi"));
  api.shouldFailGetChatMember = false;

  // 3.5 Fail-closed: Firestore xato berganda reason: "check_error"
  mockDb.setShouldThrow(true);
  const ctxDbErrPrivate = makeCtx({
    chatId: 5004,
    chatType: "private",
    userId: 5004,
    api,
  });
  await handleStart(ctxDbErrPrivate as any);
  assert.ok(ctxDbErrPrivate.replies[0].text.includes("Hozir tekshirib bo‘lmadi"));
  mockDb.setShouldThrow(false);
  console.log("  ✅ Shaxsiy chat ruxsatlari, bloklash ustunligi va fail-closed tasdiqlandi");

  // 4. Inline menyular, <= 64 bayt callback_data, poyga himoyasi va shaxsiy chatda < 9/12 tavsiyasi
  console.log("\n4. Inline menyu oqimi, callback <= 64 bayt va shaxsiy chat yakuniy tavsiyasi...");
  // Dars tanlash: m:k:d:1
  const ctxSelectLesson = makeCtx({
    chatId: manualUserId,
    chatType: "private",
    userId: manualUserId,
    callbackData: "m:k:d:1",
    api,
  });
  await handleMenuCallback(ctxSelectLesson as any);
  assert.equal(ctxSelectLesson.edits.length, 1);
  assert.ok(ctxSelectLesson.edits[0].text.includes("1-dars bo‘yicha test: 12 savol, har biriga 30 soniya"));
  const confirmBtns = ctxSelectLesson.edits[0].other?.reply_markup?.inline_keyboard?.[0];
  assert.equal(confirmBtns?.[0]?.callback_data, "m:k:go:1");
  assert.equal(confirmBtns?.[1]?.callback_data, "m:k:list");
  for (const btn of confirmBtns) {
    assert.ok(Buffer.byteLength(btn.callback_data, "utf8") <= 64);
  }

  // Testni boshlash: m:k:go:1
  const ctxGoLesson = makeCtx({
    chatId: manualUserId,
    chatType: "private",
    userId: manualUserId,
    callbackData: "m:k:go:1",
    api,
  });
  await handleMenuCallback(ctxGoLesson as any);
  assert.equal(quizManager.isQuizActive(manualUserId), true);

  // Faol quiz paytida ikkinchi marta m:k:go:1 bosilganda alert chiqishi va yangi sessiya ochilmasligi
  const ctxDoubleClick = makeCtx({
    chatId: manualUserId,
    chatType: "private",
    userId: manualUserId,
    callbackData: "m:k:go:1",
    api,
  });
  await handleMenuCallback(ctxDoubleClick as any);
  assert.equal(ctxDoubleClick.alerts[0]?.show_alert, true);

  // Shaxsiy chatda 5/12 ball bilan yakunlanganda "<N>-dars videosini qayta ko'rishni tavsiya qilamiz." chiqishi (Q4)
  const privSession = quizManager.getSession(manualUserId)!;
  privSession.participants.set(manualUserId, {
    userId: manualUserId,
    firstName: "Talaba",
    score: 5,
    totalTimeMs: 40000,
    answersCount: 12,
  });
  const formattedMsgs = quizManager.formatLeaderboardMessages(
    privSession,
    quizManager.getLeaderboard(manualUserId)
  );
  assert.ok(
    formattedMsgs[0].includes("1-dars videosini qayta ko‘rishni tavsiya qilamiz."),
    "9/12 dan kam ball olganda video tavsiyasi chiqishi shart"
  );

  // Shaxsiy chatda /stop admin tekshiruvisiz ishlashi (Q6)
  const ctxPrivateStop = makeCtx({
    chatId: manualUserId,
    chatType: "private",
    userId: manualUserId,
    isAdmin: false,
    api,
  });
  await handleStopQuizCommand(ctxPrivateStop as any);
  assert.equal(quizManager.isQuizActive(manualUserId), false);
  console.log("  ✅ Inline menyu, poyga himoyasi, < 9/12 tavsiyasi va shaxsiy /stop ishladi");

  // 5. Admin API yangi endpointlari va xavfsizlik (javob maydoni yo'qligi)
  console.log("\n5. Admin API endpointlari va javob kaliti xavfsizligi...");
  const secret = "test_admin_secret_key_for_kurs_qobiq_12345";
  const token = createAdminSessionToken(ADMIN_GOOGLE_EMAIL, ADMIN_GOOGLE_EMAIL, secret);
  const config: EnvConfig = {
    BOT_TOKEN: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    PORT: 0,
    NODE_ENV: "test",
    ADMIN_SESSION_SECRET: secret,
  };

  const app = express();
  app.use(express.json());
  app.use("/api", createAdminRouter(config, api as any));
  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const port = (server.address() as any).port;
  const headers = {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };

  const reqApi = async (method: string, path: string, body?: any) => {
    const res = await fetch(`http://127.0.0.1:${port}${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    return { status: res.status, data: await res.json() };
  };

  // 5.1 PATCH /api/admin/groups/:chatId/mode
  const modePatch = await reqApi("PATCH", `/api/admin/groups/${asosiyGroupId}/mode`, {
    mode: "kurs",
  });
  assert.equal(modePatch.status, 200);
  assert.equal(modePatch.data.mode, "kurs");

  const badModePatch = await reqApi("PATCH", `/api/admin/groups/${asosiyGroupId}/mode`, {
    mode: "notogri_rejim",
  });
  assert.equal(badModePatch.status, 400);

  // 5.2 CRUD /api/admin/kurs/ishtirokchilar
  const postPart = await reqApi("POST", "/api/admin/kurs/ishtirokchilar", {
    userId: 7001,
    ism: "Yangi O'quvchi",
  });
  assert.equal(postPart.status, 200);
  assert.equal(postPart.data.participant.userId, 7001);

  const getPart = await reqApi("GET", "/api/admin/kurs/ishtirokchilar?q=7001");
  assert.equal(getPart.status, 200);
  assert.equal(getPart.data.items.length, 1);

  const patchPart = await reqApi("PATCH", "/api/admin/kurs/ishtirokchilar/7001", {
    bloklangan: true,
  });
  assert.equal(patchPart.status, 200);
  assert.equal(patchPart.data.participant.bloklangan, true);

  const delPart = await reqApi("DELETE", "/api/admin/kurs/ishtirokchilar/7001");
  assert.equal(delPart.status, 200);

  // 5.3 GET /api/admin/kurs/darslar (javob maydoni ASLO bo'lmasligi shart!)
  const darslarRes = await reqApi("GET", "/api/admin/kurs/darslar");
  assert.equal(darslarRes.status, 200);
  assert.equal(darslarRes.data.darslar.length, 2);
  const serializedDarslar = JSON.stringify(darslarRes.data);
  assert.equal(serializedDarslar.includes("javob"), false, "API javobida 'javob' maydoni bo'lmasligi shart!");
  assert.equal(serializedDarslar.includes("variantlar"), false, "API javobida savol variantlari bo'lmasligi shart!");

  // 5.4 POST /api/admin/kurs/qayta-yuklash
  const reloadRes = await reqApi("POST", "/api/admin/kurs/qayta-yuklash");
  assert.equal(reloadRes.status, 200);
  assert.equal(reloadRes.data.lessonsCount, 2);

  // 5.5 GET & PATCH /api/admin/settings (subscriptionChannels olib tashlangan!)
  const getSettings = await reqApi("GET", "/api/admin/settings");
  assert.equal(getSettings.status, 200);
  assert.equal(getSettings.data.settings.subscriptionChannels, undefined);
  assert.equal(getSettings.data.settings.adminContact, "@diyorbek_jabborov");
  assert.equal(getSettings.data.settings.defaultGroupMode, "asosiy");

  const patchSettings = await reqApi("PATCH", "/api/admin/settings", {
    adminContact: "@yangi_admin",
    defaultGroupMode: "ochiq_emas",
  });
  assert.equal(patchSettings.status, 200);
  assert.equal(patchSettings.data.settings.adminContact, "@yangi_admin");
  assert.equal(patchSettings.data.settings.defaultGroupMode, "ochiq_emas");
  const currentSettings = await getBotSettings();
  assert.equal(currentSettings.adminContact, "@yangi_admin");

  // Audit loglar yozilganini tekshirish
  const logs = await getAuditLogs(20);
  assert.ok(logs.some((l) => l.action === "GROUP_MODE_CHANGE"));
  assert.ok(logs.some((l) => l.action === "KURS_PARTICIPANT_ADD"));
  assert.ok(logs.some((l) => l.action === "KURS_LESSONS_RELOAD"));
  assert.ok(logs.some((l) => l.action === "BOT_SETTINGS_UPDATE"));

  await new Promise<void>((resolve) => server.close(() => resolve()));
  clearKursDarslarForTest();
  resetShellStateForTest();
  resetBotSettingsState();
  resetFirestoreState();

  console.log("  ✅ Barcha Admin API endpointlari, kesh invalidatsiyasi va audit loglar 100% o'tdi!");
  console.log("\n🎉 BARCHA KURS QOBIG'I TESTLARI MUVAFFAQIYATLI YAKUNLANDI!");
}

runKursQobiqTests().catch((err) => {
  console.error("❌ Kurs qobig'i testida xatolik:", err);
  process.exit(1);
});
