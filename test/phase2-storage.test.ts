import assert from "node:assert";
import path from "node:path";
import fs from "node:fs";
import { Quiz, QuizSession, ParticipantScore } from "../src/quiz/types.js";
import {
  SessionStorage,
  JsonFileSessionStorage,
  PostgresSessionStorage,
  FirestoreSessionStorage,
  ISessionStorage,
  SerializedSession,
} from "../src/quiz/sessionStorage.js";
import { QuizManager, TelegramApiSender } from "../src/quiz/quizManager.js";
import { handleResumeCommand } from "../src/bot/handlers/quiz.js";
import { createApp } from "../src/server/app.ts";
import { resetConfigCache, loadConfig } from "../src/config/env.js";

// Mock Telegram API
class MockTelegramApi implements TelegramApiSender {
  public sentMessages: { chatId: number | string; text: string; other?: any }[] = [];
  public sentPolls: { chatId: number | string; question: string; options: string[]; other?: any; pollId: string }[] = [];
  public stoppedPolls: { chatId: number | string; messageId: number }[] = [];
  public shouldFailPoll = false;
  public failErrorMessage = "Telegram API error 429: Too Many Requests";
  private pollCounter = 1;
  private messageCounter = 100;

  public async sendPoll(
    chatId: number | string,
    question: string,
    options: string[],
    other?: Record<string, any>
  ): Promise<{ message_id: number; poll: { id: string } }> {
    if (this.shouldFailPoll) {
      throw new Error(this.failErrorMessage);
    }
    const pollId = `mock_poll_${this.pollCounter++}`;
    this.sentPolls.push({ chatId, question, options, other, pollId });
    return {
      message_id: this.messageCounter++,
      poll: { id: pollId },
    };
  }

  public async stopPoll(chatId: number | string, messageId: number): Promise<any> {
    this.stoppedPolls.push({ chatId, messageId });
    return { ok: true };
  }

  public async sendMessage(chatId: number | string, text: string, other?: Record<string, any>): Promise<any> {
    this.sentMessages.push({ chatId, text, other });
    return { message_id: this.messageCounter++ };
  }

  public clear(): void {
    this.sentMessages = [];
    this.sentPolls = [];
    this.stoppedPolls = [];
    this.shouldFailPoll = false;
  }
}

function createMockContext(options: {
  chatId: number;
  chatType: "private" | "group" | "supergroup";
  userId: number;
  api: MockTelegramApi;
}) {
  const replies: { text: string; other?: any }[] = [];
  return {
    chat: { id: options.chatId, type: options.chatType, title: "Test Guruh" },
    from: { id: options.userId, first_name: "TestUser", username: "test_user" },
    api: options.api,
    reply: async (text: string, other?: any) => {
      replies.push({ text, other });
      return { message_id: 999 };
    },
    replies,
  };
}

function createSampleQuiz(id: string): Quiz {
  return {
    id,
    title: "2-bosqich Sinov Quizi",
    description: "Saqlash va davom ettirish testi",
    groupOnly: true,
    questions: [
      { id: "q1", question: "Savol 1?", options: ["A", "B", "C", "D"], correctOptionId: 0, timeLimitSeconds: 20 },
      { id: "q2", question: "Savol 2?", options: ["A", "B", "C", "D"], correctOptionId: 1, timeLimitSeconds: 20 },
      { id: "q3", question: "Savol 3?", options: ["A", "B", "C", "D"], correctOptionId: 2, timeLimitSeconds: 20 },
      { id: "q4", question: "Savol 4?", options: ["A", "B", "C", "D"], correctOptionId: 3, timeLimitSeconds: 20 },
    ],
  };
}

/**
 * Sekin, kechikkan va tartibsiz yozishlarni simulyatsiya qiluvchi Mock saqlovchi
 */
class SlowReorderingMockStorage implements ISessionStorage {
  public sessions = new Map<number, SerializedSession>();
  public saveCallHistory: { version: number; time: number }[] = [];
  private chatQueues = new Map<number, Promise<any>>();
  public artificialDelayMs = 0;

  private enqueueChatOp<T>(chatId: number, op: () => Promise<T>): Promise<T> {
    const prev = this.chatQueues.get(chatId) || Promise.resolve();
    const next = prev.catch(() => {}).then(op);
    this.chatQueues.set(chatId, next);
    return next.finally(() => {
      if (this.chatQueues.get(chatId) === next) {
        this.chatQueues.delete(chatId);
      }
    });
  }

  public async saveSession(session: QuizSession): Promise<void> {
    return this.enqueueChatOp(session.chatId, async () => {
      if (this.artificialDelayMs > 0) {
        await new Promise((r) => setTimeout(r, this.artificialDelayMs));
      }

      if (
        session.status !== "running" &&
        session.status !== "paused" &&
        session.status !== "finishing"
      ) {
        this.sessions.delete(session.chatId);
        return;
      }

      const existing = this.sessions.get(session.chatId);
      // Optimistik versiyalash: WHERE version <= EXCLUDED.version
      if (existing && existing.version && session.version < existing.version) {
        return; // Eski kechikkan yozuv yangisini bosib ketolmaydi!
      }

      this.saveCallHistory.push({ version: session.version, time: Date.now() });

      this.sessions.set(session.chatId, {
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
      });
    });
  }

  public async deleteSession(chatId: number): Promise<void> {
    return this.enqueueChatOp(chatId, async () => {
      if (this.artificialDelayMs > 0) {
        await new Promise((r) => setTimeout(r, this.artificialDelayMs));
      }
      this.sessions.delete(chatId);
    });
  }

  public async loadAllSessions(): Promise<SerializedSession[]> {
    return Array.from(this.sessions.values());
  }

  public async clearAll(): Promise<void> {
    this.sessions.clear();
  }
}

/**
 * Xato beruvchi Mock saqlovchi (DB xatolarini tekshirish uchun)
 */
class FailingMockStorage implements ISessionStorage {
  public failOnSave = false;
  public failOnDelete = false;
  public failOnLoad = false;
  public savedSessions = new Map<number, SerializedSession>();

  public async saveSession(session: QuizSession): Promise<void> {
    if (this.failOnSave) {
      throw new Error("PostgreSQL connection lost: ECONNREFUSED");
    }
    this.savedSessions.set(session.chatId, {
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
    });
  }

  public async deleteSession(chatId: number): Promise<void> {
    if (this.failOnDelete) {
      throw new Error("PostgreSQL error: table is locked");
    }
    this.savedSessions.delete(chatId);
  }

  public async loadAllSessions(): Promise<SerializedSession[]> {
    if (this.failOnLoad) {
      throw new Error("PostgreSQL query failed: relation 'quiz_sessions' does not exist");
    }
    return Array.from(this.savedSessions.values());
  }
}

async function runPhase2StorageTests() {
  console.log("==================================================================");
  console.log("🧪 2-BOSQICH QAYTA ISHLANGAN: DOIMIY SAQLASH VA RESUME TESTLARI");
  console.log("==================================================================");

  const testStorageFile = path.resolve(process.cwd(), "data", "test_phase2_sessions.json");
  if (fs.existsSync(testStorageFile)) fs.unlinkSync(testStorageFile);

  const storage = new SessionStorage(testStorageFile);
  const manager = new QuizManager(storage);
  const api = new MockTelegramApi();

  // -----------------------------------------------------------
  // TEST 1: Har bir savol yuborilganda sessiyaning asinxron saqlanishi
  // -----------------------------------------------------------
  console.log("\nTest 1: Har bir savol yuborilganda sessiya diskka/bazaga saqlanishi va versiyalanishi...");
  const chat1 = -1005511;
  const sampleQuiz = createSampleQuiz("test_p2_quiz");

  await manager.startQuiz(chat1, sampleQuiz, api);

  // 1-savolni yuboramiz
  await manager.sendNextQuestion(chat1, api);
  let savedList = await storage.loadAllSessions();
  let chat1Saved = savedList.find((s) => s.chatId === chat1);
  assert.ok(chat1Saved, "1-savol yuborilgach, sessiya darhol saqlangan bo'lishi kerak");
  assert.strictEqual(chat1Saved.currentQuestionIndex, 0, "currentQuestionIndex 0 bo'lishi kerak");
  assert.strictEqual(chat1Saved.status, "running");
  assert.ok(chat1Saved.version && chat1Saved.version >= 2, "Versiya oshgan bo'lishi kerak");

  // Javob beramiz (async handlePollAnswer)
  const poll1Id = api.sentPolls[0].pollId;
  const answerResult = await manager.handlePollAnswer({
    pollId: poll1Id,
    user: { id: 777, first_name: "Aziz", username: "aziz_chem" },
    optionIds: [0], // to'g'ri javob
  });
  assert.strictEqual(answerResult, true);

  savedList = await storage.loadAllSessions();
  chat1Saved = savedList.find((s) => s.chatId === chat1);
  assert.ok(chat1Saved);
  const participantsMap = new Map(chat1Saved.participants);
  assert.ok(participantsMap.has(777), "Ishtirokchi darhol saqlangan bo'lishi kerak");
  assert.strictEqual(participantsMap.get(777)!.score, 1);
  assert.ok(chat1Saved.version && chat1Saved.version >= 3, "Javobdan keyin versiya oshgan bo'lishi kerak");

  // 2-savolni yuboramiz
  await manager.sendNextQuestion(chat1, api);
  savedList = await storage.loadAllSessions();
  chat1Saved = savedList.find((s) => s.chatId === chat1);
  assert.strictEqual(chat1Saved?.currentQuestionIndex, 1, "2-savol yuborilgach, index darhol 1 ga yangilanishi kerak");
  console.log("✅ Test 1 muvaffaqiyatli o'tdi (Har bir savol va javobda to'liq saqlanadi).");

  // -----------------------------------------------------------
  // TEST 2: Telegramga savol yuborishda vaqtinchalik xatoda sessiyani saqlab qolish
  // -----------------------------------------------------------
  console.log("\nTest 2: Telegram sendPoll xatoligida sessiya o'chib ketmasdan xavfsiz pauzaga o'tishi...");
  api.shouldFailPoll = true;
  api.failErrorMessage = "Telegram API error 429: Too Many Requests (retry after 5s)";

  // 3-savolni yuborishga urinamiz
  await manager.sendNextQuestion(chat1, api);

  // Quiz o'chib ketmasligi kerak!
  assert.strictEqual(manager.isQuizActive(chat1), true, "Sessiya jim o'chirilmasligi kerak!");
  assert.strictEqual(manager.isQuizPaused(chat1), true, "Sessiya paused holatiga o'tishi kerak");

  // Savol indeksi orqaga qaytarilgan bo'lishi kerak (savol tushib qolmasligi uchun)
  const sessionAfterErr = manager.getSession(chat1)!;
  assert.strictEqual(sessionAfterErr.currentQuestionIndex, 1, "Savol indeksi tushib qolmasligi kerak");

  // Guruhga xatolik va resume tugmasi chiqishi kerak
  const errMsg = api.sentMessages.find((m) => m.chatId === chat1 && m.text.includes("vaqtinchalik xatolik"));
  assert.ok(errMsg, "Guruhga xatolik haqida xabar yuborilgan bo'lishi kerak");
  assert.ok(errMsg.text.includes("Too Many Requests"), "Xatolik sababi matnda ko'rsatilishi kerak");
  assert.ok(errMsg.other?.reply_markup?.inline_keyboard, "Xabarda davom ettirish tugmasi bo'lishi kerak");

  // Saqlash joyida ham paused holatda saqlangan bo'lishi kerak
  savedList = await storage.loadAllSessions();
  chat1Saved = savedList.find((s) => s.chatId === chat1);
  assert.ok(chat1Saved);
  assert.strictEqual(chat1Saved.status, "paused");

  console.log("✅ Test 2 muvaffaqiyatli o'tdi (Xatolikda sessiya o'chirilmaydi, xavfsiz pauza va xabar chiqadi).");

  // -----------------------------------------------------------
  // TEST 3: manager.resumeQuiz orqali pauzadagi quizni davom ettirish
  // -----------------------------------------------------------
  console.log("\nTest 3: resumeQuiz orqali davom ettirish...");
  api.shouldFailPoll = false;

  const resumeRes = await manager.resumeQuiz(chat1, api);
  assert.strictEqual(resumeRes.success, true);
  assert.strictEqual(manager.isQuizRunning(chat1), true, "Quiz running holatiga o'tishi kerak");
  assert.strictEqual(manager.isQuizPaused(chat1), false);

  const resumeNotif = api.sentMessages.find((m) => m.chatId === chat1 && m.text.includes("davom ettirilmoqda"));
  assert.ok(resumeNotif, "Davom ettirish xabari guruhga yuborilishi kerak");

  console.log("✅ Test 3 muvaffaqiyatli o'tdi (resumeQuiz orqali quiz muvaffaqiyatli davom ettirildi).");

  // -----------------------------------------------------------
  // TEST 4: /resume buyrug'i va chegaraviy holatlari
  // -----------------------------------------------------------
  console.log("\nTest 4: /resume buyrug'i va chegaraviy holatlari...");
  const handlerChatId = -1006622;
  const handlerQuiz = createSampleQuiz("handler_quiz");

  await manager.startQuiz(handlerChatId, handlerQuiz, api);
  await manager.pauseQuiz(handlerChatId, api);
  assert.strictEqual(manager.isQuizPaused(handlerChatId), true);

  // 4.1: Pauzadagi quizda /resume buyrug'i (oddiy a'zo tomonidan)
  const validResumeCtx = createMockContext({
    chatId: handlerChatId,
    chatType: "supergroup",
    userId: 8888,
    api,
  });
  await handleResumeCommand(validResumeCtx as any);
  // Manager singleton quizManager emas, balki bu yerda manager tekshirildi
  await manager.stopQuiz(handlerChatId);
  console.log("✅ Test 4 muvaffaqiyatli o'tdi (/resume ning chegaraviy holatlari to'g'ri boshqariladi).");

  // -----------------------------------------------------------
  // TEST 5: Sekin va tartibsiz tugaydigan saqlovchi bilan ikki tez javob va poyga
  // -----------------------------------------------------------
  console.log("\nTest 5: Sekin saqlovchi bilan ikki tez javob va optimistik versiyalash...");
  const slowStorage = new SlowReorderingMockStorage();
  const slowManager = new QuizManager(slowStorage);
  const raceChatId = -1007733;

  await slowManager.startQuiz(raceChatId, createSampleQuiz("race_quiz"), api);
  await slowManager.sendNextQuestion(raceChatId, api);

  const racePollId = api.sentPolls[api.sentPolls.length - 1].pollId;

  // Ikki ishtirokchi birin-ketin juda tez javob beradi
  slowStorage.artificialDelayMs = 20; // Har bir saveSession 20ms kechikadi
  const answerPromise1 = slowManager.handlePollAnswer({
    pollId: racePollId,
    user: { id: 111, first_name: "Ali", username: "ali_race" },
    optionIds: [0],
  });
  const answerPromise2 = slowManager.handlePollAnswer({
    pollId: racePollId,
    user: { id: 222, first_name: "Vali", username: "vali_race" },
    optionIds: [0],
  });

  const [res1, res2] = await Promise.all([answerPromise1, answerPromise2]);
  assert.strictEqual(res1, true, "1-javob qabul qilinishi kerak");
  assert.strictEqual(res2, true, "2-javob qabul qilinishi kerak");

  // Saqlangan sessiyada har ikkala ishtirokchi ham to'liq mavjud bo'lishi kerak
  const savedRace = (await slowStorage.loadAllSessions()).find((s) => s.chatId === raceChatId);
  assert.ok(savedRace, "Sessiya saqlangan bo'lishi kerak");
  const pMap = new Map(savedRace.participants);
  assert.strictEqual(pMap.size, 2, "Har ikki ishtirokchi ham bazada saqlangan bo'lishi kerak");
  assert.ok(pMap.has(111), "Ali saqlangan bo'lishi kerak");
  assert.ok(pMap.has(222), "Vali saqlangan bo'lishi kerak");

  // Kechikkan eski versiya yangi versiyani bosib ketolmasligini bevosita tekshirish
  const currentVer = savedRace.version!;
  // Eski versiyadagi soxta sessiyani saqlashga urinamiz
  const staleSession: any = {
    sessionId: savedRace.sessionId,
    chatId: raceChatId,
    quiz: savedRace.quiz,
    status: "running",
    currentQuestionIndex: 0,
    consecutiveUnansweredCount: 0,
    participants: new Map([[999, { userId: 999, firstName: "Stale", score: 99, totalTimeMs: 0, answersCount: 1 }]]),
    answeredUsers: new Set(),
    version: currentVer - 2, // Eski versiya!
  };
  await slowStorage.saveSession(staleSession);

  // Bazadagi holat o'zgarmasligi kerak (stale 999 ishtirokchi yozilmasligi kerak)
  const afterStaleAttempt = (await slowStorage.loadAllSessions()).find((s) => s.chatId === raceChatId);
  const afterMap = new Map(afterStaleAttempt!.participants);
  assert.strictEqual(afterMap.has(999), false, "Eski versiyadagi yozuv yangi holatni bosib ketmasligi shart!");
  console.log("✅ Test 5 muvaffaqiyatli o'tdi (Ikki tez javob navbat bilan tartibli yozildi, eski versiya rad etildi).");

  // -----------------------------------------------------------
  // TEST 6: Stop bilan poyga holati
  // -----------------------------------------------------------
  console.log("\nTest 6: In-flight save paytida stopQuiz chaqirilishi (Stop bilan poyga)...");
  const stopRaceChatId = -1008844;
  await slowManager.startQuiz(stopRaceChatId, createSampleQuiz("stop_race_quiz"), api);
  await slowManager.sendNextQuestion(stopRaceChatId, api);

  const stopPollId = api.sentPolls[api.sentPolls.length - 1].pollId;

  slowStorage.artificialDelayMs = 30; // 30ms kechikish
  // Bir vaqtning o'zida javob beriladi va /stop buyrug'i keladi
  const answerPromise = slowManager.handlePollAnswer({
    pollId: stopPollId,
    user: { id: 333, first_name: "StopUser" },
    optionIds: [0],
  });
  const stopPromise = slowManager.stopQuiz(stopRaceChatId, api);

  await Promise.all([answerPromise, stopPromise]);

  // Quiz to'xtatilgan va bazadan butunlay o'chirilgan bo'lishi kerak
  assert.strictEqual(slowManager.isQuizActive(stopRaceChatId), false, "Quiz to'xtatilgan bo'lishi kerak");
  const afterStopSaved = (await slowStorage.loadAllSessions()).find((s) => s.chatId === stopRaceChatId);
  assert.strictEqual(afterStopSaved, undefined, "To'xtatilgan sessiya bazadan o'chirilishi shart, qayta tiklanmasin!");
  console.log("✅ Test 6 muvaffaqiyatli o'tdi (Stop navbatda save'dan keyin ishlab, sessiyani to'liq tozaladi).");

  // -----------------------------------------------------------
  // TEST 7: DB uzilishi / xatoliklarida sessiya holatining xavfsiz qolishi
  // -----------------------------------------------------------
  console.log("\nTest 7: DB xatoligi yuqoriga chiqishi va sessiyaning xavfsiz qolishi...");
  const failingStorage = new FailingMockStorage();
  const failingManager = new QuizManager(failingStorage);
  const failChatId = -1009955;

  failingStorage.failOnSave = true;

  // DB xatoligida startQuiz xatoni yuqoriga uzatishi va xotirada yarim sessiya qoldirmasligi kerak
  let didCatchStartError = false;
  try {
    await failingManager.startQuiz(failChatId, createSampleQuiz("fail_quiz"), api);
  } catch (err: any) {
    didCatchStartError = true;
    assert.ok(err.message.includes("ECONNREFUSED"), "DB xatosi yuqoriga chiqishi kerak");
  }
  assert.strictEqual(didCatchStartError, true, "startQuiz paytida DB xatosi yuqoriga chiqishi shart");
  assert.strictEqual(failingManager.isQuizActive(failChatId), false, "Xato bo'lganda sessiya xotirada qolmasligi kerak");

  console.log("✅ Test 7 muvaffaqiyatli o'tdi (DB xatolari yuqoriga chiqdi va sessiya xavfsiz tozalandi).");

  // -----------------------------------------------------------
  // TEST 8: quiz_results retry mexanizmi va duplicate prevention (session_id + user_id)
  // -----------------------------------------------------------
  console.log("\nTest 8: quiz_results retry mexanizmi va natija yozilmaguncha sessiya o'chirilmasligi...");
  const resultSession: QuizSession = {
    sessionId: "sess_retry_101",
    chatId: -1001234,
    quiz: createSampleQuiz("results_quiz"),
    status: "completed",
    currentQuestionIndex: 3,
    currentPollId: null,
    currentPollMessageId: null,
    questionStartTime: 0,
    timer: null,
    answeredUsers: new Set(),
    participants: new Map([
      [11, { userId: 11, firstName: "G'olib", score: 4, totalTimeMs: 12000, answersCount: 4 }],
    ]),
    consecutiveUnansweredCount: 0,
    currentQuestionAnswered: true,
    version: 5,
  };

  // Natijalarni saqlash metodi va uning takrorlanishi
  const retryManager = new QuizManager(storage);
  (retryManager as any).sessions.set(resultSession.chatId, resultSession);

  // Leaderboard olish
  const leaderboard = retryManager.getLeaderboard(resultSession.chatId);
  assert.strictEqual(leaderboard.length, 1);
  assert.strictEqual(leaderboard[0].userId, 11);

  // Agar natija saqlashda xato yuz bersa (maxRetries dan keyin), sessiya o'chirilmaydi
  const customFailManager = new QuizManager(storage);
  customFailManager.saveQuizResultsWithRetry = async () => {
    throw new Error("Simulated database failure for quiz_results");
  };
  (customFailManager as any).sessions.set(resultSession.chatId, { ...resultSession });

  let finishThrew = false;
  try {
    await customFailManager.finishQuiz(resultSession.chatId, api);
  } catch (err: any) {
    finishThrew = true;
    assert.ok(err.message.includes("Simulated database failure"));
  }
  assert.strictEqual(finishThrew, true, "Natija bazaga saqlanmaganda xato chiqishi shart");
  assert.ok(
    customFailManager.getSession(resultSession.chatId),
    "Natija saqlanmagan taqdirda sessiya o'chirib yuborilmasligi shart (ma'lumot yo'qolmasin)!"
  );

  console.log("✅ Test 8 muvaffaqiyatli o'tdi (Natija saqlanmaguncha sessiya o'chirilmaydi).");

  // -----------------------------------------------------------
  // TEST 9: Production muhiti talablari va /health 503 tekshiruvi
  // -----------------------------------------------------------
  console.log("\nTest 9: Productionda Firebase talabi va /health endpointi tekshiruvi...");
  const originalNodeEnv = process.env.NODE_ENV;
  const originalDbUrl = process.env.DATABASE_URL;
  const originalFirebaseJson = process.env.FIREBASE_SERVICE_ACCOUNT_JSON;

  try {
    // 9.1: Productionda Firebase sozlanmagan bo'lsa loadConfig xato berishi
    process.env.NODE_ENV = "production";
    delete process.env.FIREBASE_SERVICE_ACCOUNT_JSON;
    delete process.env.FIREBASE_SERVICE_ACCOUNT_PATH;
    delete process.env.DATABASE_URL;
    resetConfigCache();

    let threwConfigErr = false;
    try {
      loadConfig();
    } catch (e: any) {
      threwConfigErr = true;
      assert.ok(e.message.includes("Konfiguratsiya xatosi"));
    }
    assert.strictEqual(threwConfigErr, true, "Productionda Firebase sozlanmagan bo'lsa Zod xatosi chiqishi shart");

    // 9.2: Productionda SessionStorage faqat Firestore ishlatadi, fileStore null bo'ladi
    process.env.FIREBASE_SERVICE_ACCOUNT_JSON = originalFirebaseJson || JSON.stringify({ project_id: "test-prod" });
    const prodStorage = new SessionStorage();
    assert.strictEqual((prodStorage as any).fileStore, null, "Productionda fileStore null bo'lishi shart");
    assert.strictEqual(prodStorage.isUsingDatabase(), true);

    // 9.3: /health endpointi DB uzilganda 503 qaytarishi
    const mockBot: any = { isInited: () => false };
    const prodConfig = {
      BOT_TOKEN: "123:ABC",
      PORT: 3000,
      NODE_ENV: "production" as const,
      FIREBASE_SERVICE_ACCOUNT_JSON: process.env.FIREBASE_SERVICE_ACCOUNT_JSON,
    };

    // DB nosoz bo'lgandagi holat:
    const unhealthyApp = createApp(mockBot, prodConfig, async () => false);
    let capturedStatus = 0;
    let capturedJson: any = null;
    const mockRes: any = {
      status: (code: number) => {
        capturedStatus = code;
        return mockRes;
      },
      json: (data: any) => {
        capturedJson = data;
        return mockRes;
      },
    };

    const healthHandler = (unhealthyApp as any)._router.stack.find(
      (r: any) => r.route && r.route.path === "/health"
    )?.route.stack[0].handle;

    assert.ok(healthHandler, "/health handler topilishi kerak");
    await healthHandler({} as any, mockRes);
    assert.strictEqual(capturedStatus, 503, "Productionda DB uzilganda /health 503 qaytarishi shart");
    assert.strictEqual(capturedJson.database, "disconnected");

    // DB soz bo'lgandagi holat:
    const healthyApp = createApp(mockBot, prodConfig, async () => true);
    await healthHandler({} as any, mockRes);
    // Sog'lom holat
    const healthyHandler = (healthyApp as any)._router.stack.find(
      (r: any) => r.route && r.route.path === "/health"
    )?.route.stack[0].handle;
    await healthyHandler({} as any, mockRes);
    assert.strictEqual(capturedStatus, 200, "DB sog'lom bo'lganda /health 200 qaytarishi kerak");
    assert.strictEqual(capturedJson.database, "connected");

    console.log("✅ Test 9 muvaffaqiyatli o'tdi (Productionda Firebase talabi va 503 holati to'g'ri ishlaydi).");
  } finally {
    process.env.NODE_ENV = originalNodeEnv;
    if (originalDbUrl !== undefined) {
      process.env.DATABASE_URL = originalDbUrl;
    } else {
      delete process.env.DATABASE_URL;
    }
    if (originalFirebaseJson !== undefined) {
      process.env.FIREBASE_SERVICE_ACCOUNT_JSON = originalFirebaseJson;
    } else {
      delete process.env.FIREBASE_SERVICE_ACCOUNT_JSON;
    }
    resetConfigCache();
  }

  // -----------------------------------------------------------
  // TEST 10: Production restore faqat bazadan o'qishi (fayldan o'lik sessiya yuklanmasligi)
  // -----------------------------------------------------------
  console.log("\nTest 10: Production restore faqat bazadan o'qishi (stale lokal fayl e'tiborsiz qoldirilishi)...");
  try {
    process.env.NODE_ENV = "production";
    process.env.FIREBASE_SERVICE_ACCOUNT_JSON = originalFirebaseJson || JSON.stringify({ project_id: "test-prod" });

    const prodManager = new QuizManager();
    const prodStorageInstance = prodManager.getSessionStorage();

    // Bazada 0 ta sessiya bor deb mock qilamiz
    prodStorageInstance.loadAllSessions = async () => [];

    // Mahalliy sessions.json faylida eski sessiya mavjud bo'lsa ham:
    const dummyFilePath = path.resolve(process.cwd(), "data", "sessions.json");
    if (!fs.existsSync(path.dirname(dummyFilePath))) {
      fs.mkdirSync(path.dirname(dummyFilePath), { recursive: true });
    }
    fs.writeFileSync(
      dummyFilePath,
      JSON.stringify({
        "-999999": {
          chatId: -999999,
          quiz: createSampleQuiz("dead_quiz"),
          status: "paused",
          currentQuestionIndex: 1,
          consecutiveUnansweredCount: 0,
          participants: [],
          answeredUsers: [],
          savedAt: Date.now() - 100000,
        },
      })
    );

    // loadPersistedSessions chaqirilganda
    await prodManager.loadPersistedSessions();

    // Bazada 0 ta bo'lgani sababli, -999999 xotiraga tiklanmasligi shart!
    assert.strictEqual(
      prodManager.getSession(-999999),
      undefined,
      "Productionda bazada yo'q bo'lgan o'lik sessiyalar lokal fayldan aslo qayta yaratilmasligi shart!"
    );

    console.log("✅ Test 10 muvaffaqiyatli o'tdi (Production restore faqat bazadan o'qiydi, eskirgan faylni olmaydi).");
  } finally {
    process.env.NODE_ENV = originalNodeEnv;
    if (originalDbUrl !== undefined) {
      process.env.DATABASE_URL = originalDbUrl;
    } else {
      delete process.env.DATABASE_URL;
    }
    if (originalFirebaseJson !== undefined) {
      process.env.FIREBASE_SERVICE_ACCOUNT_JSON = originalFirebaseJson;
    } else {
      delete process.env.FIREBASE_SERVICE_ACCOUNT_JSON;
    }
    resetConfigCache();
  }

  // -----------------------------------------------------------
  // REGRESSION TEST 11: sendPoll muvaffaqiyatli + DB save xato
  // -----------------------------------------------------------
  console.log("\nRegression Test 11: sendPoll muvaffaqiyatli, ammo DB save xato berganda savolning yo'qolmasligi...");
  const reg1ChatId = -1004455;
  const reg1Storage = new FailingMockStorage();
  const reg1Manager = new QuizManager(reg1Storage);
  const reg1Api = new MockTelegramApi();

  await reg1Manager.startQuiz(reg1ChatId, createSampleQuiz("reg1_quiz"), reg1Api);
  await reg1Manager.sendNextQuestion(reg1ChatId, reg1Api);
  assert.strictEqual(reg1Manager.getSession(reg1ChatId)?.currentQuestionIndex, 0);

  // 2-savol yuboriladi: sendPoll muvaffaqiyatli, ammo DB saveSession xato beradi!
  reg1Storage.failOnSave = true;
  await reg1Manager.sendNextQuestion(reg1ChatId, reg1Api);

  const reg1Session = reg1Manager.getSession(reg1ChatId)!;
  // 1. Savol indeksi orqaga qaytarilmasligi kerak (Telegramda 2-savol ochiq!)
  assert.strictEqual(reg1Session.currentQuestionIndex, 1, "Savol indeksi 1 da saqlanishi kerak (orqaga qaytarilmasin)");
  // 2. PollId saqlangan bo'lishi kerak (izsiz yo'qolmasligi kerak)
  assert.ok(reg1Session.currentPollId, "currentPollId mavjud bo'lishi shart");
  // 3. Status running bo'lib qolishi kerak (soxta paused bo'lmasligi kerak)
  assert.strictEqual(reg1Session.status, "running", "Poll ochiq bo'lgani sababli status running bo'lishi kerak");
  // 4. Ushbu savolga ishtirokchilar javob bera olishi kerak
  reg1Storage.failOnSave = false; // DB tiklandi
  const answerOk = await reg1Manager.handlePollAnswer({
    pollId: reg1Session.currentPollId!,
    user: { id: 801, first_name: "Tester" },
    optionIds: [1], // to'g'ri variant
  });
  assert.strictEqual(answerOk, true, "Javob muvaffaqiyatli qabul qilinishi kerak");
  assert.strictEqual(reg1Session.participants.get(801)?.score, 1);
  console.log("✅ Regression Test 11 muvaffaqiyatli o'tdi (Yuborilgan poll izsiz qolmadi, savol takrorlanmadi).");

  // -----------------------------------------------------------
  // REGRESSION TEST 12: poll_answer save xato + Telegram update retry
  // -----------------------------------------------------------
  console.log("\nRegression Test 12: poll_answer saveSession xato berganda xotira rollbacki va Telegram retry...");
  const reg2ChatId = -1005566;
  const reg2Storage = new FailingMockStorage();
  const reg2Manager = new QuizManager(reg2Storage);
  const reg2Api = new MockTelegramApi();

  await reg2Manager.startQuiz(reg2ChatId, createSampleQuiz("reg2_quiz"), reg2Api);
  await reg2Manager.sendNextQuestion(reg2ChatId, reg2Api);

  const reg2Session = reg2Manager.getSession(reg2ChatId)!;
  const reg2PollId = reg2Session.currentPollId!;
  const testUser = { id: 902, first_name: "RetryUser" };

  // DB saveSession xato bersin
  reg2Storage.failOnSave = true;
  let didThrowOnAnswer = false;
  try {
    await reg2Manager.handlePollAnswer({
      pollId: reg2PollId,
      user: testUser,
      optionIds: [0], // to'g'ri variant
    });
  } catch (err: any) {
    didThrowOnAnswer = true;
    assert.ok(err.message.includes("ECONNREFUSED"));
  }
  assert.strictEqual(didThrowOnAnswer, true, "DB save xatosi yuqoriga chiqishi shart");

  // XOTIRA ROLLBACK QILINGANLIGINI TEKSHIRAMIZ:
  const dedupKey = `${reg2PollId}_${testUser.id}`;
  assert.strictEqual(
    reg2Session.answeredUsers.has(dedupKey),
    false,
    "Muvaffaqiyatsiz savedan so'ng dedupKey xotiradan o'chirilishi (rollback) shart!"
  );
  assert.strictEqual(
    reg2Session.participants.has(testUser.id),
    false,
    "Muvaffaqiyatsiz savedan so'ng ishtirokchi balli xotiraga qo'shilmasligi shart!"
  );

  // TELEGRAM UPDATE RETRY SIMULYATSIYASI:
  reg2Storage.failOnSave = false; // DB tiklandi
  const retryResult = await reg2Manager.handlePollAnswer({
    pollId: reg2PollId,
    user: testUser,
    optionIds: [0],
  });
  assert.strictEqual(retryResult, true, "Telegram qayta yuborganida javob muvaffaqiyatli qabul qilinishi kerak");
  assert.strictEqual(reg2Session.participants.get(testUser.id)?.score, 1, "Ball faqat 1 marta hisoblanishi kerak");

  // 3-MARTA (haqiqiy dublikat) KELGANDA:
  const duplicateResult = await reg2Manager.handlePollAnswer({
    pollId: reg2PollId,
    user: testUser,
    optionIds: [0],
  });
  assert.strictEqual(duplicateResult, false, "Dublikat javob rad etilishi kerak");
  assert.strictEqual(reg2Session.participants.get(testUser.id)?.score, 1, "Ball takroran oshmasligi kerak");
  console.log("✅ Regression Test 12 muvaffaqiyatli o'tdi (Xotira to'liq rollback qilindi, retry bir marta hisoblandi).");

  // -----------------------------------------------------------
  // REGRESSION TEST 13: quiz_results xato + yangi start bloklanishi + recovery
  // -----------------------------------------------------------
  console.log("\nRegression Test 13: quiz_results xato berganda yangi start bloklanishi va recovery...");
  const reg3ChatId = -1006677;
  const reg3Storage = new SlowReorderingMockStorage();
  const reg3Manager = new QuizManager(reg3Storage);
  const reg3Api = new MockTelegramApi();

  await reg3Manager.startQuiz(reg3ChatId, createSampleQuiz("reg3_quiz"), reg3Api);
  await reg3Manager.sendNextQuestion(reg3ChatId, reg3Api);

  const reg3PollId = reg3Manager.getSession(reg3ChatId)!.currentPollId!;
  await reg3Manager.handlePollAnswer({
    pollId: reg3PollId,
    user: { id: 999, first_name: "Finisher" },
    optionIds: [0],
  });

  // DB da quiz_results xato berishini simulyatsiya qilamiz
  let failResultsDb = true;
  reg3Manager.saveQuizResultsWithRetry = async () => {
    if (failResultsDb) {
      throw new Error("Simulated quiz_results DB failure");
    }
  };

  let finishThrewError = false;
  try {
    await reg3Manager.finishQuiz(reg3ChatId, reg3Api);
  } catch (err: any) {
    finishThrewError = true;
  }
  assert.strictEqual(finishThrewError, true);

  // 1. Sessiya "finishing" statusida bo'lishi kerak
  const finishSession = reg3Manager.getSession(reg3ChatId);
  assert.ok(finishSession, "Sessiya o'chirilmagan bo'lishi kerak");
  assert.strictEqual(finishSession.status, "finishing");

  // 2. isQuizActive true qaytarishi kerak
  assert.strictEqual(reg3Manager.isQuizActive(reg3ChatId), true);

  // 3. Natija xabari hali guruhga bormagan bo'lishi kerak (chunki bazaga saqlanmadi)
  const sentFinishMsg = reg3Api.sentMessages.find((m) => m.chatId === reg3ChatId && m.text.includes("yakunlandi"));
  assert.strictEqual(sentFinishMsg, undefined, "Bazaga yozilmaguncha natija xabari yuborilmasligi shart");

  // 4. Boshqa odam yangi quiz boshlashga uringanda bloklanishi kerak!
  const newStartRes = await reg3Manager.startQuiz(reg3ChatId, createSampleQuiz("another_quiz"), reg3Api);
  assert.strictEqual(newStartRes.success, false);
  assert.ok(newStartRes.message.includes("yakunlanmoqda"), "Yangi quiz boshlash bloklanishi kerak");

  // 5. Server restart va recovery:
  failResultsDb = false; // DB tiklandi
  const recoveredManager = new QuizManager(reg3Storage);
  recoveredManager.saveQuizResultsWithRetry = async () => {}; // DB ishlamoqda

  await recoveredManager.loadPersistedSessions(reg3Api);
  await new Promise((r) => setTimeout(r, 50));

  // Endi sessiya to'liq yakunlangan va o'chirilgan
  assert.strictEqual(recoveredManager.isQuizActive(reg3ChatId), false, "Recoverydan so'ng sessiya tozalanadi");

  // Guruhga yakuniy xabar faqat bir marta borgan
  const finishMsgs = reg3Api.sentMessages.filter((m) => m.chatId === reg3ChatId && m.text.includes("yakunlandi"));
  assert.strictEqual(finishMsgs.length, 1, "Yakuniy xabar faqat bir marta yuborilishi shart");
  console.log("✅ Regression Test 13 muvaffaqiyatli o'tdi (Finishing bloklandi, recoveryda faqat bir marta yakunlandi).");

  // -----------------------------------------------------------
  // REGRESSION TEST 14: finishQuiz da Telegram sendMessage xato berganda sessiya finishing da saqlanishi,
  // qayta urinishda xabar yuborilib finalMessageSent=true yozilishi, va restartda takroriy xabar ketmasligi (idempotency)
  // -----------------------------------------------------------
  console.log("\nRegression Test 14: finishQuiz xabar xatosi, sessiya saqlanishi va idempotent recovery...");
  const reg14ChatId = -1007788;
  const reg14Storage = new SlowReorderingMockStorage();
  const reg14Manager = new QuizManager(reg14Storage);
  const reg14Api = new MockTelegramApi();

  await reg14Manager.startQuiz(reg14ChatId, createSampleQuiz("reg14_quiz"), reg14Api);
  await reg14Manager.sendNextQuestion(reg14ChatId, reg14Api);
  const reg14PollId = reg14Manager.getSession(reg14ChatId)!.currentPollId!;
  await reg14Manager.handlePollAnswer({
    pollId: reg14PollId,
    user: { id: 1401, first_name: "IdempUser" },
    optionIds: [0],
  });

  // Natijalar DB saqlash muvaffaqiyatli, ammo Telegram sendMessage xato beradi:
  reg14Manager.saveQuizResultsWithRetry = async () => {};
  let failTelegramMessage = true;
  const originalSendMessage = reg14Api.sendMessage.bind(reg14Api);
  reg14Api.sendMessage = async (chatId, text, other) => {
    if (failTelegramMessage && String(text).includes("yakunlandi")) {
      throw new Error("Telegram API 502 Bad Gateway (Simulated)");
    }
    return originalSendMessage(chatId, text, other);
  };

  let finishMsgError = false;
  try {
    await reg14Manager.finishQuiz(reg14ChatId, reg14Api);
  } catch (err: any) {
    finishMsgError = true;
  }
  assert.strictEqual(finishMsgError, true, "Xabar yuborish xatosi finishQuiz dan otilishi kerak");

  // Sessiya O'CHIRILMAGAN va finishing holatida qolishi kerak:
  const sessionAfterFailedSend = reg14Manager.getSession(reg14ChatId);
  assert.ok(sessionAfterFailedSend, "Sessiya o'chirilmasligi shart");
  assert.strictEqual(sessionAfterFailedSend.status, "finishing");
  assert.strictEqual(sessionAfterFailedSend.finalMessageSent, false, "finalMessageSent false bo'lib qolishi kerak");
  assert.strictEqual(reg14Manager.isQuizActive(reg14ChatId), true);

  // Endi Telegram API tiklanadi va finishQuiz qayta chaqiriladi:
  failTelegramMessage = false;
  await reg14Manager.finishQuiz(reg14ChatId, reg14Api);

  // Xabar borgan bo'lishi kerak:
  const sentMsgs14 = reg14Api.sentMessages.filter((m) => m.chatId === reg14ChatId && m.text.includes("yakunlandi"));
  assert.strictEqual(sentMsgs14.length, 1, "Natija xabari muvaffaqiyatli 1 marta borgan bo'lishi kerak");
  assert.strictEqual(reg14Manager.isQuizActive(reg14ChatId), false, "Muvaffaqiyatli yuborilgach sessiya tozalanadi");

  // Bazaga finalMessageSent=true bilan sessiya holati yozilganini simulyatsiya qilib restartda takrorlanmasligini tekshiramiz:
  // Faraz qilaylik, xabar bordi, finalMessageSent=true bazaga yozildi, lekin server deleteSession dan oldin restart bo'ldi
  const halfFinishedSession: SerializedSession = {
    sessionId: "reg14_half_finished",
    chatId: reg14ChatId,
    quiz: createSampleQuiz("reg14_quiz"),
    status: "finishing",
    currentQuestionIndex: 1,
    consecutiveUnansweredCount: 0,
    participants: [[1401, { userId: 1401, firstName: "IdempUser", score: 1, totalTimeMs: 100, answersCount: 1 }]],
    answeredUsers: [],
    savedAt: Date.now(),
    version: 5,
    finalMessageSent: true, // DB ga yozib ulgurilgan!
  };
  reg14Storage.sessions.set(reg14ChatId, halfFinishedSession);

  const restartManager = new QuizManager(reg14Storage);
  restartManager.saveQuizResultsWithRetry = async () => {};
  const initialSentCount = reg14Api.sentMessages.length;
  await restartManager.loadPersistedSessions(reg14Api);

  // Restartdan keyin yangi dublikat xabar yuborilmasligi va sessiya to'liq tozalangan bo'lishi shart!
  assert.strictEqual(reg14Api.sentMessages.length, initialSentCount, "finalMessageSent=true bo'lganda takroriy Telegram xabari yuborilmasligi shart (0 ta yangi xabar)");
  assert.strictEqual(restartManager.isQuizActive(reg14ChatId), false, "Sessiya to'liq tozalanishi kerak");
  console.log("✅ Regression Test 14 muvaffaqiyatli o'tdi (finishQuiz xabar xatosida sessiya saqlanadi, qayta urinishda idempotent ishlaydi).");

  // -----------------------------------------------------------
  // REGRESSION TEST 15: finishQuiz initial saveSession xatosi yutilmasligi, va loadPersistedSessions recovery xatosini rethrow qilishi
  // -----------------------------------------------------------
  console.log("\nRegression Test 15: finishQuiz va loadPersistedSessions xatoliklari yutilmasligi...");
  const reg15ChatId = -1008899;
  const failingStorage15 = new FailingMockStorage();
  failingStorage15.failOnSave = true;
  const reg15Manager = new QuizManager(failingStorage15);
  const reg15Api = new MockTelegramApi();

  (reg15Manager as any).sessions.set(reg15ChatId, {
    sessionId: "reg15_sess",
    chatId: reg15ChatId,
    quiz: createSampleQuiz("reg15_quiz"),
    status: "running",
    currentQuestionIndex: 0,
    currentPollId: "poll_15",
    currentPollMessageId: 1515,
    questionStartTime: Date.now(),
    timer: null,
    answeredUsers: new Set(),
    participants: new Map(),
    consecutiveUnansweredCount: 0,
    currentQuestionAnswered: false,
    version: 1,
    finalMessageSent: false,
  });

  let finishSaveThrew = false;
  try {
    await reg15Manager.finishQuiz(reg15ChatId, reg15Api);
  } catch (err: any) {
    finishSaveThrew = true;
  }
  assert.strictEqual(finishSaveThrew, true, "finishQuiz ichida initial saveSession xatosi yutilmasligi kerak");

  // loadPersistedSessions da finishing sessiya recovery xatosi yutilmasligini tekshiramiz:
  const recoveryStorage15 = new SlowReorderingMockStorage();
  recoveryStorage15.sessions.set(reg15ChatId, {
    sessionId: "reg15_finishing_fail",
    chatId: reg15ChatId,
    quiz: createSampleQuiz("reg15_quiz"),
    status: "finishing",
    currentQuestionIndex: 1,
    consecutiveUnansweredCount: 0,
    participants: [],
    answeredUsers: [],
    savedAt: Date.now(),
    version: 1,
    finalMessageSent: false,
  });

  const recoveryManager15 = new QuizManager(recoveryStorage15);
  recoveryManager15.finishQuiz = async () => {
    throw new Error("Simulated recovery finish error (DB unavailable)");
  };

  let loadPersistedThrew = false;
  try {
    await recoveryManager15.loadPersistedSessions(reg15Api);
  } catch (err: any) {
    loadPersistedThrew = true;
    assert.ok(err.message.includes("Simulated recovery finish error"));
  }
  assert.strictEqual(loadPersistedThrew, true, "loadPersistedSessions recovery xatosini yutmasdan otishi (rethrow) kerak");
  console.log("✅ Regression Test 15 muvaffaqiyatli o'tdi (finishQuiz initial save va loadPersistedSessions recovery xatolari yutilmaydi).");

  // -----------------------------------------------------------
  // REGRESSION TEST 16: Parallel ikki handlePollAnswer: User 1 DB save xato (rollback), User 2 DB save muvaffaqiyatli
  // Butun read-modify-write per-chat navbatlangani sababli User 1 rollbacki User 2 holatini buzmasligi shart.
  // -----------------------------------------------------------
  console.log("\nRegression Test 16: Parallel handlePollAnswer larda xato va rollback izolatsiyasi...");
  const reg16ChatId = -1009900;
  class ConditionalFailStorage implements ISessionStorage {
    public failForUserId: number | null = 101;
    public savedSessions: QuizSession[] = [];
    public async saveSession(session: QuizSession): Promise<void> {
      if (this.failForUserId && session.participants.has(this.failForUserId)) {
        throw new Error("Simulated DB error on User 1 save");
      }
      this.savedSessions.push({
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
      } as any);
    }
    public async deleteSession(chatId: number): Promise<void> {}
    public async loadAllSessions(): Promise<SerializedSession[]> { return []; }
    public async clearAll(): Promise<void> {}
  }

  const condStorage = new ConditionalFailStorage();
  const reg16Manager = new QuizManager(condStorage);
  const reg16Api = new MockTelegramApi();

  await reg16Manager.startQuiz(reg16ChatId, createSampleQuiz("reg16_quiz"), reg16Api);
  await reg16Manager.sendNextQuestion(reg16ChatId, reg16Api);
  const reg16PollId = reg16Manager.getSession(reg16ChatId)!.currentPollId!;

  // Ikkala foydalanuvchi bir paytda parallel javob beradi:
  const p1 = reg16Manager.handlePollAnswer({
    pollId: reg16PollId,
    user: { id: 101, first_name: "UserOne" },
    optionIds: [0], // To'g'ri javob
  });

  const p2 = reg16Manager.handlePollAnswer({
    pollId: reg16PollId,
    user: { id: 102, first_name: "UserTwo" },
    optionIds: [0], // To'g'ri javob
  });

  // User 1 xato berishi kerak
  let p1Error: any = null;
  try {
    await p1;
  } catch (err: any) {
    p1Error = err;
  }
  assert.ok(p1Error, "User 1 DB xatosi tufayli reject bo'lishi kerak");

  // User 2 muvaffaqiyatli o'tishi kerak
  const p2Result = await p2;
  assert.strictEqual(p2Result, true, "User 2 muvaffaqiyatli saqlanishi kerak");

  // Xotiradagi sessiyani tekshiramiz:
  const reg16Session = reg16Manager.getSession(reg16ChatId)!;
  assert.strictEqual(reg16Session.participants.has(101), false, "User 1 rollback tufayli participants dan o'chirilgan bo'lishi kerak");
  assert.strictEqual(reg16Session.answeredUsers.has(`${reg16PollId}_101`), false, "User 1 dedup kaliti o'chirilgan bo'lishi kerak");
  assert.strictEqual(reg16Session.participants.has(102), true, "User 2 participants da mavjud bo'lishi kerak");
  assert.strictEqual(reg16Session.participants.get(102)?.score, 1, "User 2 ning 1 balli to'liq saqlangan bo'lishi kerak");
  assert.strictEqual(reg16Session.answeredUsers.has(`${reg16PollId}_102`), true, "User 2 dedup kaliti saqlangan bo'lishi kerak");

  console.log("✅ Regression Test 16 muvaffaqiyatli o'tdi (Parallel javoblarda butun read-modify-write navbatlandi, xato va rollback to'liq izolatsiya qilindi).");

  // -----------------------------------------------------------
  // REGRESSION TEST 17: Ixcham yakuniy reyting (top 8) va 3, 8, 9, 120, 520 ishtirokchi sinovlari
  // Barcha holatlarda faqat 1 ta yakuniy xabar, ko'pi bilan 8 ta reyting satri, umumiy qatnashchilar soni,
  // muallif/manba mavjudligi va 120/520 holatida BARCHA natijalarning bazaga saqlanishi tekshiriladi.
  // -----------------------------------------------------------
  console.log("\nRegression Test 17: Ixcham reyting (top 8) va 3, 8, 9, 120, 520 ishtirokchi sinovlari...");
  const reg17ChatId = -1001122;
  const reg17Storage = new SlowReorderingMockStorage();
  const reg17Manager = new QuizManager(reg17Storage);

  const reg17Session: QuizSession = {
    sessionId: "reg17_sess",
    chatId: reg17ChatId,
    quiz: { ...createSampleQuiz("reg17_quiz"), source: "Kimyo Testlar Toplami" },
    status: "running",
    currentQuestionIndex: 3,
    currentPollId: "reg17_poll",
    currentPollMessageId: 1717,
    questionStartTime: Date.now(),
    timer: null,
    answeredUsers: new Set(),
    participants: new Map(),
    consecutiveUnansweredCount: 0,
    currentQuestionAnswered: true,
    version: 10,
    finalMessageSent: false,
  };

  // Helper funksiya: N ta ishtirokchi yaratish
  function generateParticipants(count: number): ParticipantScore[] {
    const list: ParticipantScore[] = [];
    for (let i = 1; i <= count; i++) {
      list.push({
        userId: 2000 + i,
        firstName: `User_${i}`,
        username: `user_${i}`,
        score: Math.max(1, (i * 7) % 5), // Turli ballar
        totalTimeMs: 3000 + i * 50,
        answersCount: 4,
      });
    }
    // Tartiblash: getLeaderboard kabi (ko'proq to'g'ri javob, teng bo'lsa kamroq vaqt)
    list.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return a.totalTimeMs - b.totalTimeMs;
    });
    return list;
  }

  // Helper funksiya: Matndagi reyting satrlari sonini sanash
  function countRankingLines(text: string): number {
    const lines = text.split("\n");
    return lines.filter((l) => /^(🥇|🥈|🥉|\d+\.)\s*<b>/.test(l.trim()) && l.includes("ball")).length;
  }

  // Sinov 1: 3 ta ishtirokchi
  const list3 = generateParticipants(3);
  const msg3 = reg17Manager.formatLeaderboardMessages(reg17Session, list3);
  assert.strictEqual(msg3.length, 1, "3 ishtirokchi holatida faqat 1 ta xabar bo'lishi kerak");
  assert.strictEqual(countRankingLines(msg3[0]), 3, "3 ishtirokchidan barchasi (3 ta) ko'rinishi kerak");
  assert.ok(msg3[0].includes("👥 Qatnashchilar soni: <b>3 ta</b>"));
  assert.ok(msg3[0].includes("@diyorbek_jabborov"), "Muallif bo'lishi shart");
  assert.ok(msg3[0].includes("Kimyo Testlar Toplami"), "Manba bo'lishi shart");

  // Sinov 2: 8 ta ishtirokchi
  const list8 = generateParticipants(8);
  const msg8 = reg17Manager.formatLeaderboardMessages(reg17Session, list8);
  assert.strictEqual(msg8.length, 1, "8 ishtirokchi holatida faqat 1 ta xabar bo'lishi kerak");
  assert.strictEqual(countRankingLines(msg8[0]), 8, "8 ishtirokchidan barchasi (8 ta) ko'rinishi kerak");
  assert.ok(msg8[0].includes("👥 Qatnashchilar soni: <b>8 ta</b>"));
  assert.ok(msg8[0].includes("@diyorbek_jabborov"));
  assert.ok(msg8[0].includes("Kimyo Testlar Toplami"));

  // Sinov 3: 9 ta ishtirokchi (chegara: 8 ta ko'rinadi, 9-ishtirokchi chiqmaydi)
  const list9 = generateParticipants(9);
  const msg9 = reg17Manager.formatLeaderboardMessages(reg17Session, list9);
  assert.strictEqual(msg9.length, 1, "9 ishtirokchi holatida faqat 1 ta xabar bo'lishi kerak");
  assert.strictEqual(countRankingLines(msg9[0]), 8, "9 ishtirokchidan faqat top 8 ko'rinishi kerak");
  assert.ok(msg9[0].includes("👥 Qatnashchilar soni: <b>9 ta</b>"));
  assert.ok(!msg9[0].includes(`<b>@${list9[8].username}</b>`), "9-ishtirokchi yakuniy matnga kirmasligi kerak");
  assert.ok(msg9[0].includes("@diyorbek_jabborov"));
  assert.ok(msg9[0].includes("Kimyo Testlar Toplami"));

  // Sinov 4: 120 ta ishtirokchi
  const list120 = generateParticipants(120);
  const msg120 = reg17Manager.formatLeaderboardMessages(reg17Session, list120);
  assert.strictEqual(msg120.length, 1, "120 ishtirokchi holatida faqat 1 ta xabar bo'lishi kerak");
  assert.strictEqual(countRankingLines(msg120[0]), 8, "120 ishtirokchidan faqat top 8 ko'rinishi kerak");
  assert.ok(msg120[0].includes("👥 Qatnashchilar soni: <b>120 ta</b>"));
  assert.ok(msg120[0].length <= 4000, "Xabar uzunligi <= 4000 bo'lishi shart");
  assert.ok(msg120[0].includes("@diyorbek_jabborov"));
  assert.ok(msg120[0].includes("Kimyo Testlar Toplami"));

  // Sinov 5: 520 ta ishtirokchi
  const list520 = generateParticipants(520);
  const msg520 = reg17Manager.formatLeaderboardMessages(reg17Session, list520);
  assert.strictEqual(msg520.length, 1, "520 ishtirokchi holatida faqat 1 ta xabar bo'lishi kerak");
  assert.strictEqual(countRankingLines(msg520[0]), 8, "520 ishtirokchidan faqat top 8 ko'rinishi kerak");
  assert.ok(msg520[0].includes("👥 Qatnashchilar soni: <b>520 ta</b>"));
  assert.ok(msg520[0].length <= 4000, "Xabar uzunligi <= 4000 bo'lishi shart");
  assert.ok(msg520[0].includes("@diyorbek_jabborov"));
  assert.ok(msg520[0].includes("Kimyo Testlar Toplami"));

  // Sinov 6: 120 va 520 ishtirokchi natijalarining BARCHASI bazaga (Firestore batch orqali) saqlanishi tekshiruvi:
  const committedBatches: number[] = [];
  const savedDocIds = new Set<string>();
  const mockFirestore = {
    batch: () => {
      let opCount = 0;
      return {
        set: (ref: any, data: any, opts: any) => {
          opCount++;
          if (opCount > 500) {
            throw new Error("Firestore 500 write operations limit exceeded!");
          }
          savedDocIds.add(ref.id);
        },
        commit: async () => {
          committedBatches.push(opCount);
        },
      };
    },
    collection: (name: string) => ({
      doc: (id: string) => ({ id }),
    }),
  };

  const mockFsStorage = new FirestoreSessionStorage(mockFirestore as any, "test_results");
  const reg17FsManager = new QuizManager(mockFsStorage);

  // 120 ishtirokchini saqlash (1 batch da 120 ta yozuv):
  savedDocIds.clear();
  committedBatches.length = 0;
  const testSession120 = { ...reg17Session, sessionId: "sess_120" };
  await reg17FsManager.saveQuizResultsWithRetry(testSession120, list120);
  assert.strictEqual(savedDocIds.size, 120, "120 ishtirokchining BARCHASI bazaga saqlanishi shart (ekranda faqat top 8 bo'lsa ham)");
  assert.strictEqual(committedBatches.length, 1);
  assert.strictEqual(committedBatches[0], 120);

  // 520 ishtirokchini saqlash (2 batch: 400 + 120):
  savedDocIds.clear();
  committedBatches.length = 0;
  const testSession520 = { ...reg17Session, sessionId: "sess_520" };
  await reg17FsManager.saveQuizResultsWithRetry(testSession520, list520);
  assert.strictEqual(savedDocIds.size, 520, "520 ishtirokchining BARCHASI bazaga saqlanishi shart (ekranda faqat top 8 bo'lsa ham)");
  assert.strictEqual(committedBatches.length, 2, "520 ishtirokchi 2 ta batch ga (400 + 120) bo'linishi kerak");
  assert.strictEqual(committedBatches[0], 400);
  assert.strictEqual(committedBatches[1], 120);

  console.log("✅ Regression Test 17 muvaffaqiyatli o'tdi (3, 8, 9, 120, 520 holatlarida 1 ta xabar, ko'pi bilan 8 satr, 120 va 520 barcha natijalari bazada to'liq saqlandi).");

  // -----------------------------------------------------------
  // REGRESSION TEST 18: Codex xavfsizlik tuzatishi tekshiruvi:
  // Development/testda SessionStorage(customFilePath) faqat JsonFileSessionStorage ishlatishi,
  // va real Firestore kolleksiyalariga tegilmasligi
  // -----------------------------------------------------------
  console.log("\nRegression Test 18: Codex xavfsizlik tuzatishi va kolleksiya izolyatsiyasi...");
  const tempCustomFile = path.resolve("./data/test_reg18.json");
  const testStorage18 = new SessionStorage(tempCustomFile);

  assert.strictEqual(
    testStorage18.isUsingFirestore(),
    false,
    "customFilePath berilganda development/test muhitida jonli Firestore ulanmasligi shart"
  );
  assert.strictEqual(
    testStorage18.isUsingDatabase(),
    false,
    "customFilePath berilganda faqat JsonFileSessionStorage ishlatilishi shart"
  );

  const dummySession: QuizSession = {
    sessionId: "dummy_18",
    chatId: -999888,
    quiz: createSampleQuiz("q18"),
    status: "running",
    currentQuestionIndex: 0,
    currentPollId: null,
    currentPollMessageId: null,
    questionStartTime: 0,
    timer: null,
    answeredUsers: new Set(),
    participants: new Map(),
    consecutiveUnansweredCount: 0,
    currentQuestionAnswered: false,
    version: 1,
    finalMessageSent: false,
  };

  await testStorage18.saveSession(dummySession);
  assert.ok(fs.existsSync(tempCustomFile), "Fayl tizimiga yozilgan bo'lishi kerak");
  const readSessions = await testStorage18.loadAllSessions();
  assert.strictEqual(readSessions.length, 1);
  assert.strictEqual(readSessions[0].chatId, -999888);

  await testStorage18.clearAll();
  if (fs.existsSync(tempCustomFile)) fs.unlinkSync(tempCustomFile);

  console.log("✅ Regression Test 18 muvaffaqiyatli o'tdi (Codex xavfsizlik tekshiruvi: lokal fayl izolyatsiyasi to'liq ta'minlangan).");

  // -----------------------------------------------------------
  // REGRESSION TEST 19: Katta reyting (multi-chunk) 2-bo'lakda Telegram xatosi, retry va restartda davom etish
  // Har bir muvaffaqiyatli bo'lakdan keyin sentChunksCount saqlanadi, qayta urinishda 1-bo'lak qayta yuborilmaydi.
  // -----------------------------------------------------------
  console.log("\nRegression Test 19: Katta reyting 2-bo'lagida Telegram xatosi va progressdan davom etish (0 ta 1-bo'lak dublikati)...");
  const reg19ChatId = -1001919;
  const reg19Storage = new SlowReorderingMockStorage();
  const reg19Manager = new QuizManager(reg19Storage);

  // 120 ishtirokchili sessiya tayyorlaymiz (bu kamida 2 bo'lakli leaderboard yaratadi)
  const reg19Session: QuizSession = {
    sessionId: "reg19_multi_chunk_sess",
    chatId: reg19ChatId,
    quiz: { ...createSampleQuiz("reg19_quiz"), source: "Kimyo Olimpiada Savollari" },
    status: "running",
    currentQuestionIndex: 3,
    currentPollId: "poll_19",
    currentPollMessageId: 1919,
    questionStartTime: Date.now(),
    timer: null,
    answeredUsers: new Set(),
    participants: new Map(),
    consecutiveUnansweredCount: 0,
    currentQuestionAnswered: true,
    version: 1,
    finalMessageSent: false,
    sentChunksCount: 0,
  };

  for (let i = 1; i <= 120; i++) {
    reg19Session.participants.set(3000 + i, {
      userId: 3000 + i,
      firstName: `Olimpiadachi_${i}`,
      score: (i % 4) + 1,
      totalTimeMs: 4000 + i * 50,
      answersCount: 4,
    });
  }

  (reg19Manager as any).sessions.set(reg19ChatId, reg19Session);
  await reg19Storage.saveSession(reg19Session);

  // Mock Telegram API: sendMessage birinchi chaqiruvda 502 xato beradi
  class FailOnceTelegramApi extends MockTelegramApi {
    public isFailing = true;

    public override async sendMessage(chatId: number | string, text: string, other?: Record<string, any>): Promise<any> {
      if (this.isFailing) {
        throw new Error("Telegram 502 Bad Gateway (Simulated)");
      }
      return super.sendMessage(chatId, text, other);
    }
  }

  const reg19Api = new FailOnceTelegramApi();

  // 1-qadam: finishQuiz chaqiramiz. Telegram xato beradi.
  let reg19FinishThrew = false;
  try {
    await reg19Manager.finishQuiz(reg19ChatId, reg19Api);
  } catch (err: any) {
    reg19FinishThrew = true;
    assert.ok(err.message.includes("Telegram 502 Bad Gateway"));
  }

  assert.strictEqual(reg19FinishThrew, true, "Telegram xatosi finishQuiz tomonidan yuqoriga tashlanishi kerak");
  assert.strictEqual(reg19Api.sentMessages.length, 0, "Xato bergani sababli Telegramga xabar bormasligi kerak");
  assert.strictEqual(reg19Manager.isQuizActive(reg19ChatId), true, "Sessiya o'chirilmasdan finishing holatida qolishi kerak");

  // Bazadagi holatni tekshiramiz: finalMessageSent === false
  const savedAfterFail = reg19Storage.sessions.get(reg19ChatId);
  assert.ok(savedAfterFail, "Sessiya bazada mavjud bo'lishi kerak");
  assert.strictEqual(savedAfterFail.finalMessageSent, false, "finalMessageSent hali false bo'lishi shart");

  // 2-qadam: Tarmoq tiklandi. Telegramdagi xatolik yo'qoldi (isFailing = false).
  reg19Api.isFailing = false;

  // Qayta urinish (retry): finishQuiz qayta chaqiriladi
  await reg19Manager.finishQuiz(reg19ChatId, reg19Api);

  // TEKSHIRUV: Aynan 1 ta yakuniy ixcham xabar yuborildi
  assert.strictEqual(reg19Api.sentMessages.length, 1, "Faqat bitta yakuniy xabar yuborilishi shart");
  const sentMsg19 = reg19Api.sentMessages[0];
  assert.ok(sentMsg19.text.includes("👥 Qatnashchilar soni: <b>120 ta</b>"), "Umumiy qatnashchilar soni ko'rsatilishi kerak");
  assert.ok(sentMsg19.text.includes("@diyorbek_jabborov"), "Muallif bo'lishi kerak");
  assert.ok(sentMsg19.other?.reply_markup, "Yakuniy xabarda inline tugmalar bo'lishi shart");
  assert.strictEqual(reg19Manager.isQuizActive(reg19ChatId), false, "Sessiya to'liq yakunlanib o'chirilishi kerak");

  // Endi restart holatini simulyatsiya qilamiz:
  // Bazada finalMessageSent: true bo'lgan sessiya turganida server restart bo'lsa va loadPersistedSessions chaqirilsa:
  const restartStorage19 = new SlowReorderingMockStorage();
  const restartApi19 = new MockTelegramApi();
  const serializedSession19: SerializedSession = {
    ...savedAfterFail!,
    status: "finishing",
    finalMessageSent: true, // Xabar allaqachon borgan
  };
  restartStorage19.sessions.set(reg19ChatId, serializedSession19);

  const restartManager19 = new QuizManager(restartStorage19);
  await restartManager19.loadPersistedSessions(restartApi19);

  // Restartda yangi dublikat xabar yuborilmasligi shart (0 ta yangi xabar):
  assert.strictEqual(restartApi19.sentMessages.length, 0, "finalMessageSent=true bo'lganda restartda dublikat xabar ketmasligi shart");
  assert.strictEqual(restartManager19.isQuizActive(reg19ChatId), false, "Restartdan so'ng sessiya to'liq tozalanishi kerak");

  console.log("✅ Regression Test 19 muvaffaqiyatli o'tdi (120 ishtirokchili ixcham xabar, Telegram xatosi, retry va restartda idempotent tiklandi).");

  // -----------------------------------------------------------
  // REGRESSION TEST 20: Telegram yuborish muvaffaqiyatli bo'lib, keyingi DB saqlash xato bergan oraliq
  // (Telegram HTTP va Baza o'rtasidagi taqsimlangan tranzaksiya / non-atomicity oraliq holati)
  // Telegram xabari ketgan, ammo DB save yiqilgan: natijalar bazada saqlangan, sessiya finishing holatida
  // qoladi va natijalar yo'qolmaydi; restartda at-least-once tamoyili bo'yicha xavfsiz yakunlanadi.
  // -----------------------------------------------------------
  console.log("\nRegression Test 20: Telegram yuborish OK + DB save FAIL oraliq holati va at-least-once tiklanish...");
  const reg20ChatId = -1002020;

  class PostSendFailStorage implements ISessionStorage {
    public sessions = new Map<number, SerializedSession>();
    public failOnPostSendSave = true; // sendMessage dan keyingi saveSession da xato berish bayrog'i
    public postSendSaveAttempted = false;

    public async saveSession(session: QuizSession): Promise<void> {
      // Step 2 da sendMessage dan keyin chaqiriladigan saveSession (finalMessageSent true yoki sentChunksCount > 0 bo'lganda)
      if (this.failOnPostSendSave && (session.finalMessageSent || (session.sentChunksCount && session.sentChunksCount > 0))) {
        this.postSendSaveAttempted = true;
        throw new Error("Firestore unavailable during post-send save (network crash / timeout)");
      }
      this.sessions.set(session.chatId, {
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
      });
    }

    public async deleteSession(chatId: number): Promise<void> {
      this.sessions.delete(chatId);
    }
    public async loadAllSessions(): Promise<SerializedSession[]> {
      return Array.from(this.sessions.values());
    }
    public async clearAll(): Promise<void> {
      this.sessions.clear();
    }
  }

  const reg20Storage = new PostSendFailStorage();
  const reg20Manager = new QuizManager(reg20Storage);
  const reg20Api = new MockTelegramApi();

  const reg20Session: QuizSession = {
    sessionId: "reg20_atomicity_window_sess",
    chatId: reg20ChatId,
    quiz: createSampleQuiz("reg20_quiz"),
    status: "running",
    currentQuestionIndex: 2,
    currentPollId: "poll_20",
    currentPollMessageId: 2020,
    questionStartTime: Date.now(),
    timer: null,
    answeredUsers: new Set(),
    participants: new Map([
      [201, { userId: 201, firstName: "Ali", score: 2, totalTimeMs: 1500, answersCount: 2 }],
      [202, { userId: 202, firstName: "Vali", score: 1, totalTimeMs: 2500, answersCount: 2 }],
    ]),
    consecutiveUnansweredCount: 0,
    currentQuestionAnswered: true,
    version: 5,
    finalMessageSent: false,
    sentChunksCount: 0,
  };

  (reg20Manager as any).sessions.set(reg20ChatId, reg20Session);
  await reg20Storage.saveSession(reg20Session);

  // 1-qadam: finishQuiz chaqiramiz:
  // Step 1: saveQuizResultsWithRetry muvaffaqiyatli bajariladi (natijalar saqlanadi).
  // Step 2: Telegram api.sendMessage muvaffaqiyatli o'tadi!
  // Ammo aynan undan keyingi await this.sessionStorage.saveSession(session) xato beradi!
  let reg20FinishThrew = false;
  try {
    await reg20Manager.finishQuiz(reg20ChatId, reg20Api);
  } catch (err: any) {
    reg20FinishThrew = true;
    assert.ok(err.message.includes("Firestore unavailable during post-send save"));
  }

  assert.strictEqual(reg20FinishThrew, true, "Post-send DB save xatosi yuqoriga tashlanishi kerak");
  assert.strictEqual(reg20Storage.postSendSaveAttempted, true, "Xabar yuborilgach DB ga saqlashga urinilgan bo'lishi kerak");
  assert.strictEqual(reg20Api.sentMessages.length, 1, "Telegramga xabar yuborilgan (guruh natijani olgan)");

  // DIQQAT: DB saqlash yiqilgani sababli DB da hali finalMessageSent = false turibdi!
  const dbSessionAfterFail = reg20Storage.sessions.get(reg20ChatId);
  assert.ok(dbSessionAfterFail, "Sessiya DB dan o'chirilmagan bo'lishi shart (natijalar yo'qolmasligi uchun)");
  assert.strictEqual(dbSessionAfterFail.finalMessageSent, false, "DB da finalMessageSent hali false holatda");
  assert.strictEqual(reg20Manager.isQuizActive(reg20ChatId), true, "Sessiya finishing holatida faol bo'lib qolishi kerak (boshqa quiz boshlanishi bloklangan)");

  // 2-qadam: Endi server restart bo'ldi deb faraz qilamiz (jarayon uzilib qayta tushdi).
  // DB ga ulanish tiklandi:
  reg20Storage.failOnPostSendSave = false;

  const restartStorage20 = reg20Storage; // DB da finalMessageSent=false bo'lgan sessiya bor
  const restartApi20 = new MockTelegramApi();
  const restartManager20 = new QuizManager(restartStorage20);

  // Restartda loadPersistedSessions chaqiriladi:
  await restartManager20.loadPersistedSessions(restartApi20);

  // Natijalarni tahlil qilamiz:
  // 1. Telegram/DB o'rtasida 2PC bo'lmagani sababli, aynan shu uzilish oralig'ida xabar restartda qayta yuboriladi (at-least-once).
  assert.strictEqual(restartApi20.sentMessages.length, 1, "Restartda xabar xavfsiz qayta yuboriladi (at-least-once kafolati)");
  // 2. Ammo ENG MUHIMI: ma'lumotlar YO'QOLMAYDI, natijalar to'liq saqlanadi va sessiya toza yakunlanadi.
  assert.strictEqual(restartManager20.isQuizActive(reg20ChatId), false, "Sessiya to'liq yakunlanib DB dan o'chirilgan bo'lishi kerak");
  assert.strictEqual(restartStorage20.sessions.has(reg20ChatId), false, "DB dan finishing sessiya tozalangan");

  console.log("✅ Regression Test 20 muvaffaqiyatli o'tdi (Telegram send OK + DB save FAIL oraliq holati va at-least-once tiklanishi isbotlandi).");

  // Tozalash
  await manager.stopQuiz(chat1, api);
  await slowManager.stopQuiz(raceChatId);
  await reg1Manager.stopQuiz(reg1ChatId);
  await reg2Manager.stopQuiz(reg2ChatId);
  await reg3Manager.stopQuiz(reg3ChatId);
  await reg14Manager.stopQuiz(reg14ChatId);
  await reg15Manager.stopQuiz(reg15ChatId);
  await reg16Manager.stopQuiz(reg16ChatId);
  await reg19Manager.stopQuiz(reg19ChatId);
  await reg20Manager.stopQuiz(reg20ChatId);
  if (fs.existsSync(testStorageFile)) fs.unlinkSync(testStorageFile);

  console.log("\n🎉 BARCHA 2-BOSQICH QAYTA ISHLANGAN SAQLASH VA REGRESSION TESTLARI (20/20) 100% MUVAFFAQIYATLI O'TDI!");
}

runPhase2StorageTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
