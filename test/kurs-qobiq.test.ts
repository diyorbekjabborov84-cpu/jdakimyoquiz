import assert from "node:assert/strict";
import crypto from "node:crypto";
import http from "node:http";
import express from "express";
import {
  createAdminRouter,
  extractClientIpForRateLimit,
} from "../src/server/adminRoutes.js";
import {
  createAdminSessionToken,
  verifyAdminSessionToken,
  shouldRenewAdminSession,
  MAX_ADMIN_SESSION_SECONDS,
} from "../src/server/adminAuth.js";
import {
  ADMIN_GOOGLE_EMAIL,
  verifyGoogleOneTapToken,
  resetGoogleJwksCache,
} from "../src/server/googleAuth.js";
import { getAuditLogs } from "../src/server/auditService.js";
import { GET as meGet } from "../admin/app/api/auth/me/route.js";
import { POST as oneTapPost } from "../admin/app/api/auth/google-onetap/route.js";
import { PATCH as bffGroupModePatch } from "../admin/app/api/groups/[chatId]/mode/route.js";
import {
  GET as bffKursPartGet,
  POST as bffKursPartPost,
} from "../admin/app/api/kurs/ishtirokchilar/route.js";
import {
  PATCH as bffKursPartPatch,
  DELETE as bffKursPartDelete,
} from "../admin/app/api/kurs/ishtirokchilar/[userId]/route.js";
import { GET as bffKursDarslarGet } from "../admin/app/api/kurs/darslar/route.js";
import { POST as bffKursReloadPost } from "../admin/app/api/kurs/qayta-yuklash/route.js";
import { PATCH as bffSettingsPatch } from "../admin/app/api/settings/route.js";
import { middleware as adminMiddleware } from "../admin/middleware.js";
import {
  checkExistingSessionAndRedirect,
  checkLoginSessionWithRetry,
  verifyAdminSessionWithRetry,
  disableGoogleAutoSelectOnLogout,
  shouldSkipOneTapAutoLogin,
} from "../admin/lib/google-login.js";
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
  normalizeKursMashqlar,
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
import {
  handleInlineQuery,
  isValidQuizStartPayload,
} from "../src/bot/handlers/inlineQuery.js";
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

  const executeQuery = (
    colMap: Map<string, any>,
    filters: Array<{ field: string; op: string; val: any }>,
    sorts: Array<{ field: string; dir: "asc" | "desc" }>,
    cursorVals?: any[],
    limitCount?: number
  ) => {
    let items = Array.from(colMap.entries()).map(([id, d]) => ({
      id,
      data: () => JSON.parse(JSON.stringify(d)),
    }));

    for (const flt of filters) {
      items = items.filter((item) => {
        const d = item.data();
        if (flt.op === "==") return d[flt.field] === flt.val;
        if (flt.op === ">=") return d[flt.field] >= flt.val;
        if (flt.op === "<=") return d[flt.field] <= flt.val;
        return true;
      });
    }

    if (sorts.length > 0) {
      items.sort((a, b) => {
        for (const s of sorts) {
          const va = s.field === "__name__" ? String(a.id) : String(a.data()[s.field] ?? "");
          const vb = s.field === "__name__" ? String(b.id) : String(b.data()[s.field] ?? "");
          if (va !== vb) {
            return s.dir === "desc" ? (va < vb ? 1 : -1) : va > vb ? 1 : -1;
          }
        }
        return 0;
      });
    }

    if (cursorVals && cursorVals.length > 0) {
      const idx = items.findIndex((it) => {
        if (cursorVals.length === 1) {
          const s = sorts[0] || { field: "__name__" };
          const val = s.field === "__name__" ? String(it.id) : String(it.data()[s.field] ?? "");
          return val === String(cursorVals[0]) || String(it.id) === String(cursorVals[0]);
        }
        if (cursorVals.length >= 2) {
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
    filters: Array<{ field: string; op: string; val: any }> = [],
    sorts: Array<{ field: string; dir: "asc" | "desc" }> = [],
    cursorVals?: any[]
  ): any => ({
    where(field: string, op: string, val: any) {
      return createQueryObject(colMap, [...filters, { field, op, val }], [...sorts], cursorVals);
    },
    orderBy(field: string = "__name__", dir: "asc" | "desc" = "asc") {
      return createQueryObject(colMap, [...filters], [...sorts, { field, dir }], cursorVals);
    },
    startAfter(...vals: any[]) {
      return createQueryObject(colMap, [...filters], [...sorts], vals);
    },
    limit(n: number) {
      return {
        async get() {
          if (shouldThrowError) throw new Error("Simulated Firestore Error");
          const docs = executeQuery(colMap, filters, sorts, cursorVals, n);
          return { empty: docs.length === 0, docs };
        },
      };
    },
    count() {
      return {
        async get() {
          if (shouldThrowError) throw new Error("Simulated Firestore Error");
          const docs = executeQuery(colMap, filters, sorts);
          return { data: () => ({ count: docs.length }) };
        },
      };
    },
    async get() {
      if (shouldThrowError) throw new Error("Simulated Firestore Error");
      const docs = executeQuery(colMap, filters, sorts, cursorVals);
      return { empty: docs.length === 0, docs };
    },
  });

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
        ...createQueryObject(colMap),
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
        async add(data: any) {
          const id = `doc_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
          colMap.set(id, JSON.parse(JSON.stringify(data)));
          return { id };
        },
      };
    },
  };

  return { mockDb, collections };
}

class KursTestApi implements TelegramApiSender {
  public memberCount = 15;
  public groupMemberships = new Map<string, string>(); // "${chatId}:${userId}" -> status
  public groupErrors = new Map<number, string>(); // chatId -> error message
  public getChatMemberCalls = 0;
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
    this.getChatMemberCalls++;
    const numChatId = Number(chatId);
    if (this.groupErrors.has(numChatId)) {
      throw new Error(this.groupErrors.get(numChatId)!);
    }
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
  assert.equal(d1Quiz.questions[0].timeLimitSeconds, 25);
  assert.ok(d1Quiz.questions[0].explanation?.includes("📺 1-dars:"));
  assert.ok((d1Quiz.questions[0].explanation?.length || 0) <= 200);
  console.log("  ✅ Yuklash skripti va 25s/izoh formatlash to'g'ri ishladi");

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

  // 3.4 Fail-closed: Telegram API 429 (vaqtinchalik) xato berganda reason: "check_error" va 30s keshlanishi (T1)
  api.shouldFailGetChatMember = true;
  const callsBefore429 = api.getChatMemberCalls;
  const ctxErrorPrivate = makeCtx({
    chatId: outsiderUserId,
    chatType: "private",
    userId: outsiderUserId,
    api,
  });
  await handleStart(ctxErrorPrivate as any);
  assert.equal(ctxErrorPrivate.replies.length, 1);
  assert.ok(ctxErrorPrivate.replies[0].text.includes("Hozir tekshirib bo‘lmadi"));
  const callsAfterFirst429 = api.getChatMemberCalls;
  assert.ok(callsAfterFirst429 > callsBefore429, "1-chaqiruv Telegram API ga murojaat qilishi kerak");

  // Ikkinchi chaqiruv 30s keshdan qaytishi va Telegram API ga bormasligi shart!
  await handleStart(ctxErrorPrivate as any);
  assert.equal(api.getChatMemberCalls, callsAfterFirst429, "2-chaqiruvda check_error keshdan olinishi va Telegramga bormasligi shart");
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

  // 3.6 T1: Bitta guruh o'lik bo'lsa ("chat not found"), oddiy foydalanuvchi admin xabarini oladi va status yangilanadi
  const deadGroup1 = -1002901;
  await setGroupShellMode(deadGroup1, "kurs");
  api.groupErrors.set(deadGroup1, "Bad Request: chat not found");

  const normalUserWithDeadGroup = 5005;
  const ctxNormalDead = makeCtx({
    chatId: normalUserWithDeadGroup,
    chatType: "private",
    userId: normalUserWithDeadGroup,
    api,
  });
  await handleStart(ctxNormalDead as any);
  assert.equal(ctxNormalDead.replies.length, 1);
  assert.ok(
    ctxNormalDead.replies[0].text.includes("faqat «Kimyo 0 dan» kursi ishtirokchilari uchun ishlaydi"),
    "O'lik guruh oddiy foydalanuvchini check_error da qoldirmasligi, admin xabarini berishi kerak"
  );
  const deadDoc1 = await mockDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc(String(deadGroup1)).get();
  assert.equal(deadDoc1.data()?.status, "unknown", "chat not found bo'lganda guruh statusi unknown ga yangilanishi kerak");

  // 3.7 T1: Bitta guruh o'lik bo'lsa ham ("bot was kicked"), ikkinchi guruh a'zosi ruxsat oladi
  const deadGroup2 = -1002902;
  await setGroupShellMode(deadGroup2, "kurs");
  api.groupErrors.set(deadGroup2, "Forbidden: bot was kicked from the supergroup chat");

  const secondGroupMember = 5006;
  api.groupMemberships.set(`${kursGroupId}:${secondGroupMember}`, "member");
  const ctxSecondGroupMember = makeCtx({
    chatId: secondGroupMember,
    chatType: "private",
    userId: secondGroupMember,
    api,
  });
  const secondGroupShell = await resolveShell(ctxSecondGroupMember as any);
  assert.deepEqual(
    secondGroupShell,
    { shell: "kurs", context: "private" },
    "Bitta kurs guruhi o'lik bo'lsa ham, ikkinchi faol kurs guruhi a'zosi ruxsat olishi shart"
  );
  api.groupErrors.clear();
  console.log("  ✅ Shaxsiy chat ruxsatlari, o'lik guruh himoyasi (T1), bloklash ustunligi va fail-closed tasdiqlandi");

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
  assert.ok(ctxSelectLesson.edits[0].text.includes("1-dars bo‘yicha test: 12 savol, har biriga 25 soniya"));
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

  // 5.1b T2: mode maydoni yo'q eski guruhlar migratsiyasi va Firestore mode filtri + sahifalash + modeCounts
  await mockDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc("-1009901").set({
    chatId: -1009901,
    title: "Eski Guruh 1 (modesiz)",
    titleLower: "eski guruh 1 (modesiz)",
    type: "supergroup",
    status: "active",
    lastActivity: "2026-04-12T10:01:00.000Z",
    updatedAt: "2026-04-12T10:01:00.000Z",
  });
  await mockDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc("-1009902").set({
    chatId: -1009902,
    title: "Kurs Guruh A",
    titleLower: "kurs guruh a",
    type: "supergroup",
    status: "active",
    mode: "kurs",
    lastActivity: "2026-04-12T10:02:00.000Z",
    updatedAt: "2026-04-12T10:02:00.000Z",
  });
  await mockDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc("-1009903").set({
    chatId: -1009903,
    title: "Kurs Guruh B",
    titleLower: "kurs guruh b",
    type: "supergroup",
    status: "active",
    mode: "kurs",
    lastActivity: "2026-04-12T10:03:00.000Z",
    updatedAt: "2026-04-12T10:03:00.000Z",
  });
  await mockDb.collection("admin_migrations").doc("group_modes_v1").delete();

  // limit=2 bilan mode=kurs so'ralganda: 1-sahifada aynan 2 ta kurs guruhi chiqishi va hasMore=true bo'lishi shart!
  const kursGroupsPage1 = await reqApi("GET", "/api/admin/groups?mode=kurs&limit=2");
  assert.equal(kursGroupsPage1.status, 200);
  assert.equal(kursGroupsPage1.data.groups.length, 2, "mode=kurs limit=2 da 1-sahifa to'liq 2 ta kurs guruhini qaytarishi kerak");
  assert.equal(kursGroupsPage1.data.hasMore, true, "2 tadan ko'p kurs guruhi bo'lganda hasMore=true bo'lishi kerak");
  assert.ok(kursGroupsPage1.data.nextCursor, "nextCursor bo'lishi shart");
  assert.ok(kursGroupsPage1.data.groups.every((g: any) => g.mode === "kurs"));
  assert.ok(kursGroupsPage1.data.modeCounts.kurs >= 3);
  assert.ok(kursGroupsPage1.data.modeCounts.asosiy >= 1, "Eski modesiz guruh asosiy ga migratsiya qilingan bo'lishi kerak");

  // 2-sahifa cursor orqali
  const kursGroupsPage2 = await reqApi(
    "GET",
    `/api/admin/groups?mode=kurs&limit=2&cursor=${encodeURIComponent(kursGroupsPage1.data.nextCursor)}`
  );
  assert.equal(kursGroupsPage2.status, 200);
  assert.ok(kursGroupsPage2.data.groups.length >= 1);
  assert.ok(kursGroupsPage2.data.groups.every((g: any) => g.mode === "kurs"));

  // Migratsiya markeri yozilgani va modesiz guruhga mode: "asosiy" qo'yilgani tekshiruvi
  const migratedOldGroup = await mockDb.collection(FIRESTORE_COLLECTIONS.GROUPS).doc("-1009901").get();
  assert.equal(migratedOldGroup.data()?.mode, "asosiy");
  const migMarker = await mockDb.collection("admin_migrations").doc("group_modes_v1").get();
  assert.equal(migMarker.data()?.completed, true);

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

  // ============================================================================
  // 6. Admin kirish yaxshilanishlari (4.1) + Next.js BFF Route testlari (2-bosqich)
  // ============================================================================
  console.log("\n▶ 6. Admin kirish (Google One Tap, 30 kunlik sirpanuvchi sessiya) va BFF testlari...");

  // 6.1 RS256 JWK kalit juftligini yaratish va Google One Tap JWT imzolash yordamchisi
  const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
    modulusLength: 2048,
  });
  const publicJwk = publicKey.export({ format: "jwk" }) as JsonWebKey;
  const testKid = "test-google-kid-1";
  const clientId = "1234567890-testclient.apps.googleusercontent.com";

  const mockJwkFetcher = async () => [
    {
      ...(publicJwk as any),
      kid: testKid,
      alg: "RS256",
      use: "sig",
    },
  ];

  const signTestGoogleJwt = (
    payload: Record<string, any>,
    headerOverrides?: Record<string, any>
  ): string => {
    const header = {
      alg: "RS256",
      typ: "JWT",
      kid: testKid,
      ...headerOverrides,
    };
    const hB64 = Buffer.from(JSON.stringify(header)).toString("base64url");
    const pB64 = Buffer.from(JSON.stringify(payload)).toString("base64url");
    const signingInput = `${hB64}.${pB64}`;
    const sig = crypto
      .createSign("RSA-SHA256")
      .update(signingInput)
      .sign(privateKey)
      .toString("base64url");
    return `${signingInput}.${sig}`;
  };

  resetGoogleJwksCache();
  const nowSec = Math.floor(Date.now() / 1000);
  const validClaims = {
    iss: "https://accounts.google.com",
    aud: clientId,
    email: ADMIN_GOOGLE_EMAIL,
    email_verified: true,
    iat: nowSec - 10,
    exp: nowSec + 3600,
    sub: "google-uid-123",
  };

  // (1) One Tap token to'g'ri
  const validOneTapJwt = signTestGoogleJwt(validClaims);
  const resValid = await verifyGoogleOneTapToken(validOneTapJwt, clientId, {
    nowSeconds: nowSec,
    jwksFetcher: mockJwkFetcher,
  });
  assert.equal(resValid.valid, true, "To'g'ri One Tap JWT valid=true bo'lishi kerak");
  assert.equal(resValid.email, ADMIN_GOOGLE_EMAIL);

  // (2) Noto'g'ri aud / iss / begona email ("Bu hisobga ruxsat yo'q")
  const wrongAudRes = await verifyGoogleOneTapToken(
    signTestGoogleJwt({ ...validClaims, aud: "wrong-client-id.apps.googleusercontent.com" }),
    clientId,
    { nowSeconds: nowSec, jwksFetcher: mockJwkFetcher }
  );
  assert.equal(wrongAudRes.valid, false);
  assert.equal(wrongAudRes.error, "INVALID_AUDIENCE");

  const wrongIssRes = await verifyGoogleOneTapToken(
    signTestGoogleJwt({ ...validClaims, iss: "https://evil.example.com" }),
    clientId,
    { nowSeconds: nowSec, jwksFetcher: mockJwkFetcher }
  );
  assert.equal(wrongIssRes.valid, false);
  assert.equal(wrongIssRes.error, "INVALID_ISSUER");

  const wrongEmailRes = await verifyGoogleOneTapToken(
    signTestGoogleJwt({ ...validClaims, email: "begona@gmail.com" }),
    clientId,
    { nowSeconds: nowSec, jwksFetcher: mockJwkFetcher }
  );
  assert.equal(wrongEmailRes.valid, false);
  assert.equal(wrongEmailRes.error, "UNAUTHORIZED_EMAIL");
  assert.equal(wrongEmailRes.message, "Bu hisobga ruxsat yo'q");

  // (3) Muddati o'tgan token (exp <= now yoki eski iat)
  const expiredRes = await verifyGoogleOneTapToken(
    signTestGoogleJwt({ ...validClaims, exp: nowSec - 5 }),
    clientId,
    { nowSeconds: nowSec, jwksFetcher: mockJwkFetcher }
  );
  assert.equal(expiredRes.valid, false);
  assert.equal(expiredRes.error, "TOKEN_EXPIRED");

  const staleIatRes = await verifyGoogleOneTapToken(
    signTestGoogleJwt({ ...validClaims, iat: nowSec - 600 }),
    clientId,
    { nowSeconds: nowSec, jwksFetcher: mockJwkFetcher }
  );
  assert.equal(staleIatRes.valid, false);
  assert.equal(staleIatRes.error, "TOKEN_EXPIRED");

  // (4) email_verified: false
  const unverifiedRes = await verifyGoogleOneTapToken(
    signTestGoogleJwt({ ...validClaims, email_verified: false }),
    clientId,
    { nowSeconds: nowSec, jwksFetcher: mockJwkFetcher }
  );
  assert.equal(unverifiedRes.valid, false);
  assert.equal(unverifiedRes.error, "EMAIL_NOT_VERIFIED");

  // (5) & (6) 30 kunlik maksimal chegara va sirpanuvchi sessiya yangilanishi (< 7 kun qolganda)
  assert.equal(MAX_ADMIN_SESSION_SECONDS, 30 * 86400);
  const thirtyDayToken = createAdminSessionToken(
    ADMIN_GOOGLE_EMAIL,
    "admin",
    secret,
    MAX_ADMIN_SESSION_SECONDS
  );
  const thirtyDayVerified = verifyAdminSessionToken(thirtyDayToken, undefined, secret);
  assert.equal(thirtyDayVerified.valid, true);
  assert.equal(
    shouldRenewAdminSession(thirtyDayVerified.session!),
    false,
    "Yangi 30 kunlik sessiya darhol yangilanmasligi kerak"
  );

  // 30 kundan ortiq (> 30 kun) token rad etilishi
  const overMaxPayloadB64 = Buffer.from(
    JSON.stringify({
      adminId: ADMIN_GOOGLE_EMAIL,
      username: "admin",
      iat: nowSec,
      exp: nowSec + 31 * 86400,
    })
  ).toString("base64url");
  const overMaxHeaderB64 = Buffer.from(JSON.stringify({ alg: "HS256", typ: "JWT" })).toString("base64url");
  const overMaxSig = crypto
    .createHmac("sha256", secret)
    .update(`${overMaxHeaderB64}.${overMaxPayloadB64}`)
    .digest("base64url");
  const overMaxToken = `${overMaxHeaderB64}.${overMaxPayloadB64}.${overMaxSig}`;
  const overMaxVerified = verifyAdminSessionToken(overMaxToken, undefined, secret);
  assert.equal(overMaxVerified.valid, false);
  assert.equal(overMaxVerified.error, "TOKEN_INVALID_EXPIRY");

  // < 7 kun (masalan, 5 kun) qolgan token sirpanuvchi yangilanishi kerak
  const fiveDaysLeftToken = createAdminSessionToken(
    ADMIN_GOOGLE_EMAIL,
    "admin",
    secret,
    5 * 86400
  );
  const fiveDaysVerified = verifyAdminSessionToken(fiveDaysLeftToken, undefined, secret);
  assert.equal(fiveDaysVerified.valid, true);
  assert.equal(
    shouldRenewAdminSession(fiveDaysVerified.session!),
    true,
    "5 kun qolgan sessiya yangilanishi kerak"
  );

  // Express server va Next.js BFF orqali One Tap, /api/admin/me sirpanuvchi yangilanish va BFF route testlari
  const { mockDb: mockDb6 } = createMockFirestore();
  setCustomFirestoreDb(mockDb6 as any);
  await mockDb6.collection(FIRESTORE_COLLECTIONS.GROUPS).doc("-100501").set({
    chatId: -100501,
    title: "BFF Test Guruh",
    titleLower: "bff test guruh",
    type: "supergroup",
    status: "active",
    mode: "asosiy",
    lastActivity: "2026-04-12T10:00:00.000Z",
    updatedAt: "2026-04-12T10:00:00.000Z",
  });
  populateKursMemory(createFakeKursBank().darslar);

  const app6 = express();
  app6.use(express.json());
  app6.use(
    "/api",
    createAdminRouter(
      { ...config, GOOGLE_OAUTH_CLIENT_ID: clientId },
      api as any,
      { nowSeconds: nowSec, jwksFetcher: mockJwkFetcher }
    )
  );
  const server6 = http.createServer(app6);
  await new Promise<void>((resolve) => server6.listen(0, resolve));
  const port6 = (server6.address() as any).port;
  process.env.RENDER_API_URL = `http://127.0.0.1:${port6}`;

  const makeBffReq = (url: string, method = "GET", body?: any, tokenOverride?: string | null) => {
    const cookieToken = tokenOverride === undefined ? thirtyDayToken : tokenOverride;
    const h = new Headers({
      origin: "http://localhost:3000",
      host: "localhost:3000",
      ...(body ? { "Content-Type": "application/json" } : {}),
    });
    return {
      url,
      method,
      headers: h,
      nextUrl: new URL(url),
      cookies: {
        get: (name: string) =>
          name === "admin_session" && cookieToken ? { value: cookieToken } : undefined,
      },
      json: async () => body,
    } as any;
  };

  // BFF POST /api/auth/google-onetap -> 200 va 30 kunlik cookie
  const oneTapReq = makeBffReq(
    "http://localhost:3000/api/auth/google-onetap",
    "POST",
    { credential: validOneTapJwt },
    null
  );
  const oneTapResp = await oneTapPost(oneTapReq);
  assert.equal(oneTapResp.status, 200);
  const oneTapSetCookie = oneTapResp.headers.get("set-cookie") || "";
  assert.ok(oneTapSetCookie.includes("admin_session="));
  assert.ok(oneTapSetCookie.includes(`Max-Age=${30 * 86400}`), "Cookie Max-Age 30 kun bo'lishi shart");

  // BFF POST /api/auth/google-onetap -> begona email ("Bu hisobga ruxsat yo'q", 403)
  const badOneTapReq = makeBffReq(
    "http://localhost:3000/api/auth/google-onetap",
    "POST",
    { credential: signTestGoogleJwt({ ...validClaims, email: "other@gmail.com" }) },
    null
  );
  const badOneTapResp = await oneTapPost(badOneTapReq);
  assert.equal(badOneTapResp.status, 403);
  const badOneTapData = await badOneTapResp.json();
  assert.equal(badOneTapData.message, "Bu hisobga ruxsat yo'q");

  // BFF GET /api/auth/me -> 5 kun qolgan sessiyani 30 kunga yangilab Set-Cookie beradi
  const meSlidingReq = makeBffReq(
    "http://localhost:3000/api/auth/me",
    "GET",
    undefined,
    fiveDaysLeftToken
  );
  const meSlidingResp = await meGet(meSlidingReq);
  assert.equal(meSlidingResp.status, 200);
  const meSlidingBody = await meSlidingResp.json();
  assert.equal(meSlidingBody.ok, true);
  assert.equal(meSlidingBody.renewed, true);
  const renewedCookie = meSlidingResp.headers.get("set-cookie") || "";
  assert.ok(renewedCookie.includes("admin_session="), "Yangilangan sessiya cookie'si o'rnatilishi kerak");
  assert.ok(renewedCookie.includes(`Max-Age=${30 * 86400}`));

  // (7) /login sahifasiga haqiqiy sessiya bilan kirilganda `/` ga yo'naltirish
  let redirectedTo: string | null = null;
  const didRedirect = await checkExistingSessionAndRedirect(
    (async () => new Response(JSON.stringify({ ok: true }), { status: 200 })) as any,
    (path: string) => {
      redirectedTo = path;
    }
  );
  assert.equal(didRedirect, true);
  assert.equal(redirectedTo, "/");

  // (8) Chiqish (logout) qilganda disableAutoSelect chaqirilishi va auto-login skip bayrog'i
  let disableAutoSelectCalled = false;
  const fakeStorageMap = new Map<string, string>();
  const mockStorage = {
    setItem: (k: string, v: string) => fakeStorageMap.set(k, v),
    getItem: (k: string) => fakeStorageMap.get(k) ?? null,
  };
  const mockWin = {
    google: {
      accounts: {
        id: {
          disableAutoSelect: () => {
            disableAutoSelectCalled = true;
          },
          cancel: () => {},
        },
      },
    },
  };
  disableGoogleAutoSelectOnLogout(mockWin, mockStorage);
  assert.equal(disableAutoSelectCalled, true, "Logout vaqtida google.accounts.id.disableAutoSelect() chaqirilishi shart");
  assert.equal(shouldSkipOneTapAutoLogin("", mockStorage), true, "Logout'dan keyin One Tap avto-kirish to'xtatilishi shart");
  assert.equal(shouldSkipOneTapAutoLogin("?logout=1"), true, "logout=1 query bo'lganda ham One Tap avto-kirish to'xtatilishi shart");

  // Middleware tekshiruvi: sessiyasiz himoyalangan sahifa /login ga yo'naltiriladi
  const unauthMwReq = makeBffReq("http://localhost:3000/kurs-testlari", "GET", undefined, null);
  const unauthMwRes = adminMiddleware(unauthMwReq);
  assert.equal(unauthMwRes.status, 307);
  assert.ok(unauthMwRes.headers.get("location")?.includes("/login"));

  const bffModeRes = await bffGroupModePatch(
    makeBffReq("http://localhost:3000/api/groups/-100501/mode", "PATCH", { mode: "kurs" }),
    { params: Promise.resolve({ chatId: "-100501" }) }
  );
  assert.equal(bffModeRes.status, 200);

  const bffAddPartRes = await bffKursPartPost(
    makeBffReq("http://localhost:3000/api/kurs/ishtirokchilar", "POST", {
      userId: 8801,
      ism: "BFF Ishtirokchi",
    })
  );
  assert.equal(bffAddPartRes.status, 200);

  const bffGetPartRes = await bffKursPartGet(
    makeBffReq("http://localhost:3000/api/kurs/ishtirokchilar?q=8801")
  );
  assert.equal(bffGetPartRes.status, 200);
  const bffGetPartData = await bffGetPartRes.json();
  assert.equal(bffGetPartData.items.length, 1);

  const bffPatchPartRes = await bffKursPartPatch(
    makeBffReq("http://localhost:3000/api/kurs/ishtirokchilar/8801", "PATCH", {
      bloklangan: true,
    }),
    { params: Promise.resolve({ userId: "8801" }) }
  );
  assert.equal(bffPatchPartRes.status, 200);

  const bffDelPartRes = await bffKursPartDelete(
    makeBffReq("http://localhost:3000/api/kurs/ishtirokchilar/8801", "DELETE"),
    { params: Promise.resolve({ userId: "8801" }) }
  );
  assert.equal(bffDelPartRes.status, 200);

  const bffDarslarRes = await bffKursDarslarGet(
    makeBffReq("http://localhost:3000/api/kurs/darslar")
  );
  assert.equal(bffDarslarRes.status, 200);
  const bffDarslarData = await bffDarslarRes.json();
  assert.equal(bffDarslarData.darslar.length, 2);

  const bffReloadRes = await bffKursReloadPost(
    makeBffReq("http://localhost:3000/api/kurs/qayta-yuklash", "POST")
  );
  assert.equal(bffReloadRes.status, 200);

  const bffSettingsRes = await bffSettingsPatch(
    makeBffReq("http://localhost:3000/api/settings", "PATCH", {
      adminContact: "@Diyorbek_Jabborov",
      defaultGroupMode: "asosiy",
    })
  );
  assert.equal(bffSettingsRes.status, 200);

  // ============================================================================
  // 7. Tuzatishlar 2 (T4, T5, T6) testlari
  // ============================================================================
  console.log("\n▶ 7. Tuzatishlar 2 (T4: 503 qayta urinish, T5: JWKS kalit almashishi, T6: X-Forwarded-For rate-limit)...");

  // 7.1 (T4-1) 401 bo'lsa, darhol /login ga yo'naltiriladi (qayta urinmasdan)
  let t4RedirectPath: string | null = null;
  let t4WakingCalled = false;
  const t4Res401 = await verifyAdminSessionWithRetry({
    fetchImpl: (async () =>
      new Response(JSON.stringify({ ok: false, error: "UNAUTHORIZED" }), {
        status: 401,
      })) as any,
    onRedirectToLogin: (p) => {
      t4RedirectPath = p;
    },
    onWakingChange: (waking) => {
      if (waking) t4WakingCalled = true;
    },
    retryDelaysMs: [10, 20, 30],
    sleepImpl: async () => {},
  });
  assert.equal(t4Res401.status, "unauthenticated");
  assert.equal(t4Res401.redirectedToLogin, true);
  assert.equal(t4RedirectPath, "/login", "401 da /login ga yo'naltirilishi shart");
  assert.equal(t4Res401.attempts, 1, "401 da qayta urinmasligi kerak");
  assert.equal(t4WakingCalled, false);

  // 7.2 (T4-2 va T4-3) 503 bo'lsa, /login ga yo'naltirilmaydi, qayta urinish boshlanadi va 200 kelganda sahifa ochiladi
  let t4RetryRedirect: string | null = null;
  const wakingEvents: Array<{ waking: boolean; attempt: number }> = [];
  let seqAttempt = 0;
  const t4Res503Then200 = await verifyAdminSessionWithRetry({
    fetchImpl: (async () => {
      seqAttempt++;
      if (seqAttempt <= 2) {
        return new Response(JSON.stringify({ ok: false, error: "RENDER_UNAVAILABLE" }), {
          status: 503,
        });
      }
      return new Response(
        JSON.stringify({ ok: true, user: { id: ADMIN_GOOGLE_EMAIL, username: "admin" } }),
        { status: 200 }
      );
    }) as any,
    onRedirectToLogin: (p) => {
      t4RetryRedirect = p;
    },
    onWakingChange: (waking, attempt) => {
      wakingEvents.push({ waking, attempt });
    },
    retryDelaysMs: [5, 5, 5],
    sleepImpl: async () => {},
  });
  assert.equal(t4Res503Then200.status, "authenticated", "Qayta urinishdan so'ng sahifa ochilishi kerak");
  assert.equal(t4Res503Then200.redirectedToLogin, false, "503 da /login ga yo'naltirilmasligi shart");
  assert.equal(t4RetryRedirect, null);
  assert.equal(t4Res503Then200.attempts, 3);
  assert.ok(
    wakingEvents.some((e) => e.waking === true && e.attempt === 1),
    "503 da 'Server uyg'onmoqda' (waking=true) holati yoqilishi kerak"
  );

  // Barcha urinishlarda 503 bo'lsa ham /login ga yo'naltirilmaydi, status="unavailable" qaytadi ("Qayta urinish" tugmasi uchun)
  let t4All503Redirect: string | null = null;
  const t4All503 = await verifyAdminSessionWithRetry({
    fetchImpl: (async () =>
      new Response(JSON.stringify({ ok: false, error: "RENDER_UNAVAILABLE" }), {
        status: 503,
      })) as any,
    onRedirectToLogin: (p) => {
      t4All503Redirect = p;
    },
    retryDelaysMs: [5, 5],
    sleepImpl: async () => {},
  });
  assert.equal(t4All503.status, "unavailable");
  assert.equal(t4All503.redirectedToLogin, false);
  assert.equal(t4All503Redirect, null, "Barcha urinishlar 503 bo'lsa ham /login ga tashlab yubormasligi shart");

  // 7.3 (T4-4) /login sahifasida 503 bo'lsa, One Tap ishga tushmaydi; faqat 401 da ishga tushadi
  let login503Redirect: string | null = null;
  const loginOn503 = await checkLoginSessionWithRetry(
    (async () =>
      new Response(JSON.stringify({ ok: false, error: "RENDER_UNAVAILABLE" }), {
        status: 503,
      })) as any,
    (p) => {
      login503Redirect = p;
    },
    {
      retryDelaysMs: [5, 5],
      sleepImpl: async () => {},
      searchStr: "",
    }
  );
  assert.equal(loginOn503.status, "unavailable");
  assert.equal(loginOn503.redirected, false);
  assert.equal(loginOn503.shouldStartOneTap, false, "/login da 503 bo'lganda One Tap ishga tushmasligi shart!");
  assert.equal(login503Redirect, null);

  // /login da 503 -> 200 bo'lsa, "/" ga yo'naltiriladi va One Tap ishga tushmaydi
  let loginWakeRedirect: string | null = null;
  let loginWakeCount = 0;
  const loginWakeRes = await checkLoginSessionWithRetry(
    (async () => {
      loginWakeCount++;
      if (loginWakeCount === 1) {
        return new Response(JSON.stringify({ ok: false }), { status: 503 });
      }
      return new Response(JSON.stringify({ ok: true, user: { id: "admin" } }), { status: 200 });
    }) as any,
    (p) => {
      loginWakeRedirect = p;
    },
    {
      retryDelaysMs: [5, 5],
      sleepImpl: async () => {},
      searchStr: "",
    }
  );
  assert.equal(loginWakeRes.status, "authenticated");
  assert.equal(loginWakeRes.redirected, true);
  assert.equal(loginWakeRedirect, "/");
  assert.equal(loginWakeRes.shouldStartOneTap, false);

  // /login da 401 bo'lsa (va logout bayrog'i bo'lmasa), One Tap ishga tushishi mumkin (shouldStartOneTap=true)
  const emptyStorage = { getItem: () => null };
  const loginOn401 = await checkLoginSessionWithRetry(
    (async () => new Response(JSON.stringify({ ok: false }), { status: 401 })) as any,
    () => {},
    {
      retryDelaysMs: [5],
      sleepImpl: async () => {},
      searchStr: "",
      storage: emptyStorage,
    }
  );
  assert.equal(loginOn401.status, "unauthenticated");
  assert.equal(loginOn401.shouldStartOneTap, true, "/login da aniq 401 bo'lganda One Tap ruxsat oladi");

  // 7.4 (T5) Google JWKS kalitlari almashganda (yangi kid) >=60s oraliq bilan bir marta qayta yuklanishi
  resetGoogleJwksCache();
  const rotatedKeyPair = crypto.generateKeyPairSync("rsa", { modulusLength: 2048 });
  const rotatedPublicJwk = rotatedKeyPair.publicKey.export({ format: "jwk" }) as JsonWebKey;
  const rotatedKid = "test-google-kid-rotated-2";

  let jwksFetchCount = 0;
  let currentJwksList: any[] = [
    {
      ...(publicJwk as any),
      kid: testKid,
      alg: "RS256",
      use: "sig",
    },
  ];
  const statefulJwksFetcher = async () => {
    jwksFetchCount++;
    return currentJwksList;
  };

  const baseNowMs = nowSec * 1000;
  // 1-so'rov: eski kalit keshga tushadi (jwksFetchCount = 1)
  const firstVerify = await verifyGoogleOneTapToken(validOneTapJwt, clientId, {
    nowSeconds: nowSec,
    nowMs: baseNowMs,
    jwksFetcher: statefulJwksFetcher,
  });
  assert.equal(firstVerify.valid, true);
  assert.equal(jwksFetchCount, 1);

  // Google kalitni almashtirdi: serverda yangi rotatedKid paydo bo'ldi
  currentJwksList = [
    {
      ...(rotatedPublicJwk as any),
      kid: rotatedKid,
      alg: "RS256",
      use: "sig",
    },
  ];
  const signRotatedJwt = (kidToUse: string) => {
    const hB64 = Buffer.from(
      JSON.stringify({ alg: "RS256", typ: "JWT", kid: kidToUse })
    ).toString("base64url");
    const pB64 = Buffer.from(JSON.stringify(validClaims)).toString("base64url");
    const sig = crypto
      .createSign("RSA-SHA256")
      .update(`${hB64}.${pB64}`)
      .sign(rotatedKeyPair.privateKey)
      .toString("base64url");
    return `${hB64}.${pB64}.${sig}`;
  };

  // 65 soniyadan so'ng yangi kid bilan token kelganda: kesh chetlab o'tilib 1 marta qayta yuklanadi (jwksFetchCount = 2) va valid=true bo'ladi!
  const rotatedJwt = signRotatedJwt(rotatedKid);
  const rotatedVerify = await verifyGoogleOneTapToken(rotatedJwt, clientId, {
    nowSeconds: nowSec,
    nowMs: baseNowMs + 65_000,
    jwksFetcher: statefulJwksFetcher,
  });
  assert.equal(rotatedVerify.valid, true, "Yangi kid uchun JWKS qayta yuklanib, token tasdiqlanishi shart");
  assert.equal(jwksFetchCount, 2, "JWKS aynan 1 marta qayta yuklanishi kerak");

  // Oradan atigi 10 soniya (< 60s) o'tganda yana noma'lum kid kelsa: JWKS qayta yuklanmasligi kerak (DoS himoyasi)
  const unknownKidJwt = signRotatedJwt("unknown-kid-999");
  const cooldownVerify = await verifyGoogleOneTapToken(unknownKidJwt, clientId, {
    nowSeconds: nowSec,
    nowMs: baseNowMs + 75_000,
    jwksFetcher: statefulJwksFetcher,
  });
  assert.equal(cooldownVerify.valid, false);
  assert.equal(
    jwksFetchCount,
    2,
    "60 soniyalik cooldown ichida JWKS qayta yuklanmasligi shart"
  );

  // 7.5 (T6) X-Forwarded-For boshiga soxta IP qo'shish orqali login rate-limitni aylanib o'tib bo'lmasligi
  const spoofReq = {
    headers: { "x-forwarded-for": "1.1.1.1, 2.2.2.2, 198.51.100.77" },
    ip: "127.0.0.1",
  } as any;
  assert.equal(
    extractClientIpForRateLimit(spoofReq),
    "198.51.100.77",
    "Oxirgi (ishonchli proxy qo'shgan) IP olinishi shart"
  );

  let rateLimitedStatus = 200;
  for (let i = 1; i <= 26; i++) {
    const res = await fetch(`http://127.0.0.1:${port6}/api/auth/google-onetap`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Har safar birinchi IP ni o'zgartirib yuboramiz, lekin Render proxy qo'shgan oxirgi IP bir xil:
        "X-Forwarded-For": `10.99.0.${i}, 198.51.100.88`,
      },
      body: JSON.stringify({ credential: "invalid.jwt.token" }),
    });
    rateLimitedStatus = res.status;
  }
  assert.equal(
    rateLimitedStatus,
    429,
    "X-Forwarded-For boshidagi IP o'zgartirilsa ham 26-urinishda 429 TOO_MANY_ATTEMPTS qaytishi shart"
  );

  console.log("  ✅ Tuzatishlar 2 (T4, T5, T6) testlari 100% o'tdi!");

  // ============================================================================
  // 8. 3-bosqich (B1, B2, B3, B5): Inline query, deep-link payload, 20-25s taymer, mashqlar
  // ============================================================================
  console.log("\n8. 3-bosqich (B1, B2, B3, B5) testlari...");

  // 8.1 (B5) String massiv va obyekt ko'rinishidagi mashqlar validatsiyasi va normallashtirilishi
  const dars3WithStrings = {
    dars: 3,
    mavzu: "Sinov 3-mavzu (Atom tuzilishi fixture)",
    papka: "03-dars_sinov",
    testlar: Array.from({ length: 12 }, (_, idx) => ({
      id: `FAKE_D03_T${String(idx + 1).padStart(2, "0")}`,
      savol: `Sinov 3-dars, savol #${idx + 1}?`,
      variantlar: {
        A: `A-${idx + 1}`,
        B: `B-${idx + 1}`,
        C: `C-${idx + 1}`,
        D: `D-${idx + 1}`,
      },
      javob: (["A", "B", "C", "D"] as const)[idx % 4],
    })),
    mashqlar: [
      "1-sinov ochiq savoli?",
      "2-sinov ochiq savoli?",
      { id: "custom_m03", savol: "3-sinov obyekt savoli?", yechim: "Javob" },
    ],
  };

  const b5Val = validateKursDarslarPayload([...fakeBank.darslar, dars3WithStrings]);
  assert.equal(b5Val.valid, true, "String massiv mashqlar bilan validatsiya o'tishi shart");
  const validatedD3 = b5Val.validated.find((d) => d.dars === 3);
  assert.ok(validatedD3);
  assert.equal(validatedD3.mashqlar?.length, 3);
  assert.deepEqual(validatedD3.mashqlar?.[0], {
    id: "d03_m01",
    savol: "1-sinov ochiq savoli?",
  });
  assert.deepEqual(validatedD3.mashqlar?.[1], {
    id: "d03_m02",
    savol: "2-sinov ochiq savoli?",
  });
  assert.deepEqual(validatedD3.mashqlar?.[2], {
    id: "custom_m03",
    savol: "3-sinov obyekt savoli?",
    yechim: "Javob",
  });
  assert.equal(normalizeKursMashqlar(["  Savol A  "], 5)[0].id, "d05_m01");

  populateKursMemory(b5Val.validated);
  await addKursParticipant({ userId: manualUserId, ism: "Bosqich 3 Talaba" });
  await setGroupShellMode(kursGroupId, "kurs");

  // 8.2 (B1 & B2) Inline query: ishtirokchi, admin, begona, xatolik (fail-closed) va qidiruv
  const makeInlineCtx = (params: {
    userId: number;
    query?: string;
    botUsername?: string;
    apiInstance?: KursTestApi;
  }) => {
    let answeredResults: any[] = [];
    let answeredOptions: any = null;
    return {
      from: { id: params.userId, first_name: "InlineUser" },
      inlineQuery: {
        id: "iq_1",
        from: { id: params.userId, first_name: "InlineUser" },
        query: params.query ?? "",
        offset: "",
      },
      me: { id: 999999, username: params.botUsername || "jdakimyoquizbot" },
      api: params.apiInstance || api,
      getResults: () => answeredResults,
      getOptions: () => answeredOptions,
      answerInlineQuery: async (results: any[], options?: any) => {
        answeredResults = results;
        answeredOptions = options;
        return true;
      },
    };
  };

  // Kurs ishtirokchisi bo'sh so'rov yuborganda: oxirgi dars (KURS_D03) birinchi chiqadi
  const iqParticipantEmpty = makeInlineCtx({ userId: manualUserId, query: "" });
  await handleInlineQuery(iqParticipantEmpty as any);
  const partResults = iqParticipantEmpty.getResults();
  const partOpts = iqParticipantEmpty.getOptions();
  assert.equal(partOpts?.is_personal, true, "is_personal: true bo'lishi shart");
  assert.ok(
    typeof partOpts?.cache_time === "number" && partOpts.cache_time <= 10,
    "cache_time <= 10 bo'lishi shart"
  );
  assert.ok(partResults.length >= 3);
  assert.equal(partResults[0].id, "KURS_D03", "Bo'sh so'rovda oxirgi dars (KURS_D03) yuqorida turishi shart");
  assert.equal(partResults[1].id, "KURS_D02");
  assert.equal(partResults[2].id, "KURS_D01");

  // B2: Kartochka matni va 3 ta tugma formati tekshiruvi
  const cardD3 = partResults[0];
  assert.equal(
    cardD3.input_message_content.message_text,
    `🎲 «3-dars: Sinov 3-mavzu (Atom tuzilishi fixture)» testi\n\n🖊 12 ta savol · ⏱ 25 soniya`
  );
  const cardKeyboard = cardD3.reply_markup.inline_keyboard;
  assert.equal(cardKeyboard.length, 3, "3 ta tugma qatori bo'lishi shart");
  assert.deepEqual(cardKeyboard[0][0], {
    text: "Bu testni boshlash",
    url: "https://t.me/jdakimyoquizbot?start=quiz_KURS_D03",
  });
  assert.deepEqual(cardKeyboard[1][0], {
    text: "Guruhda testni boshlash",
    url: "https://t.me/jdakimyoquizbot?startgroup=quiz_KURS_D03",
  });
  assert.deepEqual(cardKeyboard[2][0], {
    text: "Testni ulashish",
    switch_inline_query: "KURS_D03",
  });
  // callback_data ishlatilmaganligini tekshirish
  for (const row of cardKeyboard) {
    for (const btn of row) {
      assert.equal("callback_data" in btn, false, "Inline kartochka tugmalarida callback_data bo'lmasligi shart");
    }
  }
  assert.equal(isValidQuizStartPayload("quiz_KURS_D03"), true);
  assert.equal(isValidQuizStartPayload("quiz_bad-char!"), false);
  assert.equal(isValidQuizStartPayload("quiz_" + "A".repeat(65)), false);

  // Qidiruv: "3" va "atom" -> KURS_D03, "KK1" -> asosiy quiz (KK1_1 va h.k.)
  const iqSearch3 = makeInlineCtx({ userId: manualUserId, query: "3" });
  await handleInlineQuery(iqSearch3 as any);
  assert.equal(iqSearch3.getResults().length, 1);
  assert.equal(iqSearch3.getResults()[0].id, "KURS_D03");

  const iqSearchAtom = makeInlineCtx({ userId: manualUserId, query: "atom" });
  await handleInlineQuery(iqSearchAtom as any);
  assert.equal(iqSearchAtom.getResults().length, 1);
  assert.equal(iqSearchAtom.getResults()[0].id, "KURS_D03");

  const iqSearchKk1 = makeInlineCtx({ userId: manualUserId, query: "KK1" });
  await handleInlineQuery(iqSearchKk1 as any);
  assert.ok(iqSearchKk1.getResults().length >= 1);
  assert.ok(iqSearchKk1.getResults().every((r: any) => r.id.startsWith("KK1")));

  // Begona foydalanuvchi kurs kartochkasini ASLO ko'rmaydi (faqat asosiy quizlarni ko'radi)
  const strangerUserId = 8801;
  const iqStranger = makeInlineCtx({ userId: strangerUserId, query: "" });
  await handleInlineQuery(iqStranger as any);
  assert.ok(iqStranger.getResults().length > 0);
  assert.equal(
    iqStranger.getResults().some((r: any) => r.id.startsWith("KURS_")),
    false,
    "Begona foydalanuvchiga kurs kartochkalari ko'rinmasligi shart"
  );

  const iqStrangerTryKurs = makeInlineCtx({ userId: strangerUserId, query: "atom" });
  await handleInlineQuery(iqStrangerTryKurs as any);
  assert.equal(iqStrangerTryKurs.getResults().length, 0);

  // Tekshiruv xatosida (fail-closed) kurs kartochkalari chiqmasligi shart
  const errorUserId = 8802;
  mockDb.setShouldThrow(true);
  const iqCheckError = makeInlineCtx({ userId: errorUserId, query: "" });
  await handleInlineQuery(iqCheckError as any);
  assert.equal(
    iqCheckError.getResults().some((r: any) => r.id.startsWith("KURS_")),
    false,
    "Tekshiruv xatosida (fail-closed) kurs kartochkalari chiqmasligi shart"
  );
  mockDb.setShouldThrow(false);

  // Admin (ADMIN_TELEGRAM_ID) ishtirokchi ro'yxatida bo'lmasa ham kurs kartochkasini ko'radi
  const prevAdminId = process.env.ADMIN_TELEGRAM_ID;
  process.env.ADMIN_TELEGRAM_ID = "990099";
  const iqAdmin = makeInlineCtx({ userId: 990099, query: "3" });
  await handleInlineQuery(iqAdmin as any);
  assert.equal(iqAdmin.getResults()[0]?.id, "KURS_D03");
  if (prevAdminId === undefined) {
    delete process.env.ADMIN_TELEGRAM_ID;
  } else {
    process.env.ADMIN_TELEGRAM_ID = prevAdminId;
  }

  // 8.3 (B2) Payload: start=quiz_KURS_D03 shaxsiy chatda ishtirokchi uchun boshlanadi, begona uchun rad etiladi;
  // startgroup asosiy guruhda kurs testini rad etadi
  const ctxStartPayloadParticipant = makeCtx({
    chatId: manualUserId,
    chatType: "private",
    userId: manualUserId,
    text: "/start quiz_KURS_D03",
    match: "quiz_KURS_D03",
    api,
  });
  await handleStart(ctxStartPayloadParticipant as any);
  assert.equal(
    quizManager.isQuizActive(manualUserId),
    true,
    "start=quiz_KURS_D03 shaxsiy chatda kurs ishtirokchisi uchun boshlanishi shart"
  );
  assert.equal(quizManager.getSession(manualUserId)?.quiz.id, "KURS_D03");

  // Begona foydalanuvchi shaxsiy chatda /start quiz_KURS_D03 bossa rad etiladi
  const ctxStartPayloadStranger = makeCtx({
    chatId: strangerUserId,
    chatType: "private",
    userId: strangerUserId,
    text: "/start quiz_KURS_D03",
    match: "quiz_KURS_D03",
    api,
  });
  await handleStart(ctxStartPayloadStranger as any);
  assert.equal(
    quizManager.isQuizActive(strangerUserId),
    false,
    "Begona foydalanuvchi uchun shaxsiy chatda kurs testi boshlanmasligi shart"
  );
  assert.ok(
    ctxStartPayloadStranger.replies[0]?.text.includes(
      "faqat «Kimyo 0 dan» kursi ishtirokchilari uchun ishlaydi"
    )
  );

  // Asosiy guruhda startgroup=quiz_KURS_D03 (/start@jdakimyoquizbot quiz_KURS_D03) rad etiladi
  const realAsosiyGroupId = -1007701;
  await setGroupShellMode(realAsosiyGroupId, "asosiy");
  const ctxStartGroupAsosiy = makeCtx({
    chatId: realAsosiyGroupId,
    chatType: "supergroup",
    userId: manualUserId,
    text: "/start@jdakimyoquizbot quiz_KURS_D03",
    match: "quiz_KURS_D03",
    api,
  });
  await handleStart(ctxStartGroupAsosiy as any);
  assert.equal(
    quizManager.isQuizActive(realAsosiyGroupId),
    false,
    "Asosiy guruhda startgroup=quiz_KURS_D03 rad etilishi shart"
  );
  assert.ok(
    ctxStartGroupAsosiy.replies[0]?.text.includes(
      "faqat «Kimyo 0 dan» kursi guruhlari va ishtirokchilari uchun"
    )
  );

  // 8.4 (B3) Vaqt sozlamasi (kursQuestionTimeSeconds): 19 va 26 rad etiladi, 20 va 25 qabul qilinadi;
  // yangi sessiya yangi vaqtni oladi, ishlayotgan sessiya eski vaqtni saqlaydi!
  const runningSessionBeforePatch = quizManager.getSession(manualUserId);
  assert.ok(runningSessionBeforePatch);
  assert.equal(
    runningSessionBeforePatch.quiz.questions[0].timeLimitSeconds,
    25,
    "Boshlangan sessiya dastlabki 25 soniya vaqtga ega bo'lishi kerak"
  );

  const reqApi6 = async (method: string, path: string, body?: any) => {
    const res = await fetch(`http://127.0.0.1:${port6}${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    return { status: res.status, data: await res.json() };
  };

  // 19 va 26 rad etilishi
  const badTime19 = await reqApi6("PATCH", "/api/admin/settings", {
    kursQuestionTimeSeconds: 19,
  });
  assert.equal(badTime19.status, 400);
  assert.equal(badTime19.data.error, "INVALID_KURS_QUESTION_TIME");

  const badTime26 = await reqApi6("PATCH", "/api/admin/settings", {
    kursQuestionTimeSeconds: 26,
  });
  assert.equal(badTime26.status, 400);
  assert.equal(badTime26.data.error, "INVALID_KURS_QUESTION_TIME");

  // 20 qabul qilinishi
  const okTime20 = await reqApi6("PATCH", "/api/admin/settings", {
    kursQuestionTimeSeconds: 20,
  });
  assert.equal(okTime20.status, 200);
  assert.equal(okTime20.data.settings.kursQuestionTimeSeconds, 20);

  // Ishlayotgan sessiya eski (25s) vaqtini saqlab qolganligini tekshirish
  assert.equal(
    quizManager.getSession(manualUserId)?.quiz.questions[0].timeLimitSeconds,
    25,
    "Allaqachon ishlayotgan sessiya o'zining eski 25s vaqtini saqlashi shart"
  );

  // Yangi boshlangan sessiya (masalan kursGroupId da) yangi 20s vaqtni olishini tekshirish
  const ctxNewKursSession = makeCtx({
    chatId: kursGroupId,
    chatType: "supergroup",
    userId: manualUserId,
    isAdmin: true,
    text: "/start@jdakimyoquizbot quiz_KURS_D03",
    match: "quiz_KURS_D03",
    api,
  });
  await handleStart(ctxNewKursSession as any);
  assert.equal(quizManager.isQuizActive(kursGroupId), true);
  assert.equal(
    quizManager.getSession(kursGroupId)?.quiz.questions[0].timeLimitSeconds,
    20,
    "Yangi boshlangan kurs sessiyasi yangi 20s vaqtni olishi shart"
  );

  // Inline kartochka va dars tasdiqlash menyusi ham 20 soniyani ko'rsatishi
  const iqAfter20 = makeInlineCtx({ userId: manualUserId, query: "3" });
  await handleInlineQuery(iqAfter20 as any);
  assert.ok(
    iqAfter20.getResults()[0].input_message_content.message_text.includes("⏱ 20 soniya")
  );

  const ctxConfirmAfter20 = makeCtx({
    chatId: manualUserId,
    chatType: "private",
    userId: manualUserId,
    callbackData: "m:k:d:3",
    api,
  });
  await handleMenuCallback(ctxConfirmAfter20 as any);
  assert.ok(
    ctxConfirmAfter20.edits[0].text.includes("har biriga 20 soniya"),
    "Dars tasdiqlash menyusi joriy 20 soniyani ko'rsatishi shart"
  );

  // 25 soniya ham qabul qilinishi
  const okTime25 = await reqApi6("PATCH", "/api/admin/settings", {
    kursQuestionTimeSeconds: 25,
  });
  assert.equal(okTime25.status, 200);
  assert.equal(okTime25.data.settings.kursQuestionTimeSeconds, 25);

  await handleStopQuizCommand(
    makeCtx({
      chatId: manualUserId,
      chatType: "private",
      userId: manualUserId,
      api,
    }) as any
  );
  await handleStopQuizCommand(
    makeCtx({
      chatId: kursGroupId,
      chatType: "supergroup",
      userId: manualUserId,
      isAdmin: true,
      api,
    }) as any
  );

  console.log("  ✅ 3-bosqich (B1, B2, B3, B5) testlari 100% o'tdi!");

  await new Promise<void>((resolve) => server6.close(() => resolve()));
  clearKursDarslarForTest();
  resetShellStateForTest();
  resetBotSettingsState();
  resetFirestoreState();

  console.log("  ✅ Admin kirish (Google One Tap, 30 kunlik sirpanuvchi sessiya) va BFF route testlari 100% o'tdi!");
  console.log("\n🎉 BARCHA KURS QOBIG'I TESTLARI MUVAFFAQIYATLI YAKUNLANDI!");
}

runKursQobiqTests().catch((err) => {
  console.error("❌ Kurs qobig'i testida xatolik:", err);
  process.exit(1);
});
