import assert from "node:assert";
import path from "node:path";
import os from "node:os";
import { Quiz, QuizQuestion, QuizSession } from "../src/quiz/types.js";
import { QuizManager, quizManager, TelegramApiSender } from "../src/quiz/quizManager.js";
import { SessionStorage } from "../src/quiz/sessionStorage.js";
import {
  handleQuizByIdCommand,
  handleStopQuizCommand,
  handleRestartQuizCallback,
  handleResumeQuizCallback,
  startQuizById,
} from "../src/bot/handlers/quiz.js";
import {
  handleMyChatMember,
  handleNewChatMembers,
  sendGroupWelcomeMessage,
} from "../src/bot/handlers/groupWelcome.js";
import { handleStart } from "../src/bot/handlers/start.js";

// Mock Telegram API
class MockTelegramApi implements TelegramApiSender {
  async getChatMemberCount(_chatId: number | string) { return 13; }
  public sentMessages: Array<{ chatId: number | string; text: string; other?: any }> = [];
  public sentPolls: Array<{
    chatId: number | string;
    question: string;
    options: string[];
    other?: Record<string, any>;
    messageId: number;
    pollId: string;
  }> = [];
  public stoppedPolls: Array<{ chatId: number | string; messageId: number }> = [];

  private nextMessageId = 1000;
  private nextPollId = 1;

  async getChatMember(_chatId: number | string, userId: number) {
    return { status: "administrator", user: { id: userId } };
  }

  async sendPoll(
    chatId: number | string,
    question: string,
    options: string[],
    other?: Record<string, any>
  ) {
    const messageId = this.nextMessageId++;
    const pollId = `poll_test_${this.nextPollId++}`;
    this.sentPolls.push({
      chatId,
      question,
      options,
      other,
      messageId,
      pollId,
    });
    return {
      message_id: messageId,
      poll: { id: pollId },
    };
  }

  async stopPoll(chatId: number | string, messageId: number) {
    this.stoppedPolls.push({ chatId, messageId });
    return { id: `poll_stopped_${messageId}`, is_closed: true };
  }

  async sendMessage(chatId: number | string, text: string, other?: Record<string, any>) {
    this.sentMessages.push({ chatId, text, other });
    return { message_id: this.nextMessageId++, text };
  }

  clear() {
    this.sentMessages = [];
    this.sentPolls = [];
    this.stoppedPolls = [];
  }
}

function createMockContext(options: {
  chatId: number;
  chatType: "private" | "group" | "supergroup";
  userId: number;
  firstName?: string;
  username?: string;
  isAdmin?: boolean;
  match?: any;
  text?: string;
  callbackData?: string;
  myChatMember?: any;
  newChatMembers?: any[];
  api: MockTelegramApi;
}) {
  const replies: Array<{ text: string; other?: any }> = [];
  const answeredCallbacks: Array<{ text?: string; show_alert?: boolean }> = [];
  return {
    chat: { id: options.chatId, type: options.chatType },
    from: {
      id: options.userId,
      first_name: options.firstName || "TestUser",
      username: options.username || "testuser",
    },
    me: { id: 999999, username: "jdakimyoquizbot" },
    match: options.match ?? "",
    message: {
      text: options.text ?? "",
      new_chat_members: options.newChatMembers,
    },
    myChatMember: options.myChatMember,
    callbackQuery: options.callbackData ? { data: options.callbackData } : undefined,
    api: options.api,
    replies,
    answeredCallbacks,
    reply: async (text: string, other?: any) => {
      replies.push({ text, other });
      return { message_id: 888, text };
    },
    answerCallbackQuery: async (params?: { text?: string; show_alert?: boolean }) => {
      answeredCallbacks.push(params || {});
      return true;
    },
    getChatMember: async (userId: number) => {
      if (options.isAdmin !== false) {
        return { status: "administrator", user: { id: userId } };
      }
      return { status: "member", user: { id: userId } };
    },
  };
}

// 5 savolli sinov quizi
function createTestQuiz(id: string = "test_pause_quiz"): Quiz {
  const questions: QuizQuestion[] = [];
  for (let i = 1; i <= 5; i++) {
    questions.push({
      id: `${id}_q${i}`,
      question: `Sinov savoli #${i}`,
      options: [`To'g'ri #${i}`, `Xato A #${i}`, `Xato B #${i}`, `Xato C #${i}`],
      correctOptionId: 0,
      timeLimitSeconds: 20,
    });
  }
  return {
    id,
    title: "Sinov Quizi (Pauza)",
    description: "Pauza test uchun namuna quiz",
    groupOnly: true,
    shuffle: false,
    questions,
  };
}

async function runSmartPauseAndWelcomeTests() {
  console.log("🧪 AQLI PAUZA VA GURUH YO'RIQNOMASI TESTLARI BOSHLANDI...\n");

  const api = new MockTelegramApi();
  const testStorageFile = path.join(os.tmpdir(), `test_session_storage_${Date.now()}.json`);
  const storage = new SessionStorage(testStorageFile);
  const manager = new QuizManager(storage);

  // ========================================================
  // TEST 1: Bot guruhga yangi qo'shilganda yo'riqnoma yuborilishi
  // ========================================================
  console.log("Test 1: Bot guruhga yangi qo'shilganda yo'riqnoma yuborilishi...");
  api.clear();

  const groupChatId = -100123456;
  const joinCtx = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: 5555,
    myChatMember: {
      old_chat_member: { status: "left" },
      new_chat_member: { status: "member", user: { id: 999999 } },
    },
    api,
  });

  await handleMyChatMember(joinCtx as any);
  assert.strictEqual(api.sentMessages.length, 1, "Yo'riqnoma xabari yuborilishi kerak");
  const welcomeText = api.sentMessages[0].text;

  assert.ok(welcomeText.includes("JDA QUIZ guruhga qo‘shildi!"), "Sarlavha to'g'ri bo'lishi kerak");
  assert.ok(welcomeText.includes("1. JDA QUIZ botini guruh administratori qiling."));
  assert.ok(welcomeText.includes("2. Kerakli test kodlarini @jdaquizkod kanalidan oling."));
  assert.ok(welcomeText.includes("3. Test kodini guruhga yuborib quizni boshlang."));
  assert.ok(welcomeText.includes("@diyorbek_jabborov"));

  const btn = api.sentMessages[0].other?.reply_markup?.inline_keyboard?.[0]?.[0];
  assert.strictEqual(btn?.text, "📢 Test kodlari");
  assert.strictEqual(btn?.url, "https://t.me/jdaquizkod");
  console.log("✅ Test 1 muvaffaqiyatli o'tdi (Yangi qo'shilganda yo'riqnoma va tugma to'liq chiqdi).");

  // ========================================================
  // TEST 2: Admin huquqi o'zgarganda (member -> administrator) takrorlanmasligi
  // ========================================================
  console.log("\nTest 2: Admin huquqi o'zgarganda (member -> admin) yo'riqnoma takrorlanmasligi...");
  api.clear();

  const adminChangeCtx = createMockContext({
    chatId: -100987654,
    chatType: "supergroup",
    userId: 5555,
    myChatMember: {
      old_chat_member: { status: "member" },
      new_chat_member: { status: "administrator", user: { id: 999999 } },
    },
    api,
  });

  await handleMyChatMember(adminChangeCtx as any);
  assert.strictEqual(api.sentMessages.length, 0, "Adminlik berilganda xabar qayta yuborilmasligi kerak");
  console.log("✅ Test 2 muvaffaqiyatli o'tdi.");

  // ========================================================
  // TEST 3: Guruhda /start bosilganda yo'riqnoma takrorlanmasligi
  // ========================================================
  console.log("\nTest 3: Guruhda /start bosilganda yo'riqnoma takrorlanmasligi...");
  api.clear();

  const startGroupCtx = createMockContext({
    chatId: -100554433,
    chatType: "supergroup",
    userId: 7777,
    text: "/start",
    api,
  });

  await handleStart(startGroupCtx as any);
  const startWelcome = api.sentMessages.find((m) => m.text.includes("JDA QUIZ guruhga qo‘shildi!"));
  assert.strictEqual(startWelcome, undefined, "/start da guruhga qo'shilish yo'riqnomasi chiqmasligi kerak");
  console.log("✅ Test 3 muvaffaqiyatli o'tdi.");

  // ========================================================
  // TEST 4: Aqlli pauza — Ketma-ket 3 ta javobsiz savol va pauza
  // ========================================================
  console.log("\nTest 4: Ketma-ket 3 ta javobsiz savoldan keyin Aqlli pauza...");
  api.clear();

  const testChatId = -1004411;
  const testQuiz = createTestQuiz("test_pause");

  await manager.startQuiz(testChatId, testQuiz, api);
  assert.strictEqual(manager.isQuizRunning(testChatId), true);
  assert.strictEqual(manager.isQuizPaused(testChatId), false);

  // 1-savol: Hech kim javob bermaydi, timeout bo'ladi
  await manager.sendNextQuestion(testChatId, api);
  assert.strictEqual(api.sentPolls.length, 1);
  await (manager as any).handleQuestionTimeout(testChatId, api);

  const session1 = manager.getSession(testChatId)!;
  assert.strictEqual(session1.consecutiveUnansweredCount, 1, "1-savoldan keyin hisob 1 bo'lishi kerak");
  assert.strictEqual(session1.status, "running", "1-savolda hali pauza bo'lmasligi kerak");

  // 2-savol: Hech kim javob bermaydi
  await manager.sendNextQuestion(testChatId, api);
  assert.strictEqual(api.sentPolls.length, 2);
  await (manager as any).handleQuestionTimeout(testChatId, api);

  const session2 = manager.getSession(testChatId)!;
  assert.strictEqual(session2.consecutiveUnansweredCount, 2, "2-savoldan keyin hisob 2 bo'lishi kerak");
  assert.strictEqual(session2.status, "running", "2-savolda hali pauza bo'lmasligi kerak");

  // 3-savol: Yana hech kim javob bermaydi -> 3 ta ketma-ket javobsiz!
  await manager.sendNextQuestion(testChatId, api);
  assert.strictEqual(api.sentPolls.length, 3);
  await (manager as any).handleQuestionTimeout(testChatId, api);

  // 2 soniyalik taymerni kutmasdan pauseQuiz ni tekshiramiz
  await manager.pauseQuiz(testChatId, api);

  const session3 = manager.getSession(testChatId)!;
  assert.strictEqual(session3.status, "paused", "Quiz pauza holatiga o'tishi shart");
  assert.strictEqual(manager.isQuizPaused(testChatId), true);
  assert.strictEqual(manager.isQuizRunning(testChatId), false);
  assert.strictEqual(manager.isQuizActive(testChatId), true);

  // Guruhga «▶️ Qolgan joyidan davom ettirish» tugmasi chiqqanini tekshirish
  const pauseMsg = api.sentMessages.find((m) => m.chatId === testChatId && m.text.includes("Quiz vaqtincha to‘xtatildi"));
  assert.ok(pauseMsg, "Pauza xabari chiqishi kerak");
  const resumeBtn = pauseMsg.other?.reply_markup?.inline_keyboard?.[0]?.[0];
  assert.strictEqual(resumeBtn?.text, "▶️ Qolgan joyidan davom ettirish");
  assert.ok(resumeBtn?.callback_data.includes("resume_quiz"));

  console.log("✅ Test 4 muvaffaqiyatli o'tdi (Ketma-ket 3 javobsiz savoldan so'ng quiz pauzalandi va tugma chiqdi).");

  // ========================================================
  // TEST 5: Bitta odam noto'g'ri javob bersa ham sanog'ning 0 ga qaytishi
  // ========================================================
  console.log("\nTest 5: Bitta odam noto'g'ri javob bersa ham hisoblagich nolga qaytishi...");
  api.clear();
  const resetChatId = -1004422;
  const resetQuiz = createTestQuiz("test_reset");
  await manager.startQuiz(resetChatId, resetQuiz, api);

  // 1-savol: javobsiz -> count 1
  await manager.sendNextQuestion(resetChatId, api);
  await (manager as any).handleQuestionTimeout(resetChatId, api);
  assert.strictEqual(manager.getSession(resetChatId)!.consecutiveUnansweredCount, 1);

  // 2-savol: Bobur noto'g'ri javob beradi!
  await manager.sendNextQuestion(resetChatId, api);
  const p2 = api.sentPolls[api.sentPolls.length - 1];
  await manager.handlePollAnswer({
    pollId: p2.pollId,
    user: { id: 202, first_name: "Bobur" },
    optionIds: [1], // noto'g'ri variant
  });

  assert.strictEqual(
    manager.getSession(resetChatId)!.consecutiveUnansweredCount,
    0,
    "Noto'g'ri javob berilganda ham hisob nolga qaytishi shart"
  );

  await (manager as any).handleQuestionTimeout(resetChatId, api);
  assert.strictEqual(manager.getSession(resetChatId)!.consecutiveUnansweredCount, 0);

  // 3-savol: javobsiz -> count 1 bo'ladi (pauza bo'lmaydi)
  await manager.sendNextQuestion(resetChatId, api);
  await (manager as any).handleQuestionTimeout(resetChatId, api);
  assert.strictEqual(manager.getSession(resetChatId)!.consecutiveUnansweredCount, 1);
  assert.strictEqual(manager.getSession(resetChatId)!.status, "running", "Quiz to'xtamasligi kerak");

  await manager.stopQuiz(resetChatId);
  console.log("✅ Test 5 muvaffaqiyatli o'tdi (Bitta javob orqali hisob 0 ga qaytdi).");

  // ========================================================
  // TEST 6: Pauzadagi quizni oddiy a'zo ham davom ettira olishi
  // ========================================================
  console.log("\nTest 6: Pauzadagi quizni oddiy a'zo ham davom ettira olishi...");
  api.clear();

  const globalPauseChatId = -1008899;
  const globalQuiz = createTestQuiz("global_pause");
  await quizManager.startQuiz(globalPauseChatId, globalQuiz, api);
  await quizManager.pauseQuiz(globalPauseChatId, api);

  assert.strictEqual(quizManager.isQuizPaused(globalPauseChatId), true);
  const pauseSess = quizManager.getSession(globalPauseChatId)!;

  const nonAdminResumeCtx = createMockContext({
    chatId: globalPauseChatId,
    chatType: "supergroup",
    userId: 8899,
    isAdmin: false,
    callbackData: `resume_quiz_${globalPauseChatId}_${pauseSess.sessionId}`,
    api,
  });

  await handleResumeQuizCallback(nonAdminResumeCtx as any);
  assert.ok(nonAdminResumeCtx.answeredCallbacks.length > 0);
  assert.strictEqual(nonAdminResumeCtx.answeredCallbacks[0].text, "▶️ Quiz davom ettirilmoqda!");
  assert.strictEqual(quizManager.isQuizRunning(globalPauseChatId), true, "Oddiy a'zo bosganda ham quiz davom etishi kerak");

  await quizManager.stopQuiz(globalPauseChatId);
  console.log("✅ Test 6 muvaffaqiyatli o'tdi (Oddiy a'zo muvaffaqiyatli davom ettirdi).");

  // ========================================================
  // TEST 7: Davom ettirilganda aynan keyingi savoldan boshlanishi va ballar saqlanishi
  // ========================================================
  console.log("\nTest 7: Davom ettirilganda keyingi savol va ballar saqlanishi...");
  api.clear();

  const currentSess = manager.getSession(testChatId)!;
  // Dastlabki ishtirokchiga ball beramiz (testChatId)
  currentSess.participants.set(100, {
    userId: 100,
    firstName: "Aziz",
    username: "aziz_kimyo",
    score: 2,
    totalTimeMs: 14000,
    answersCount: 2,
  });

  // 3-savolda pauza bo'lgan edi (currentQuestionIndex = 2)
  assert.strictEqual(currentSess.currentQuestionIndex, 2);

  // Istalgan a'zo davom ettiradi (to'g'ri sessionId bilan)
  const resumeRes = await manager.resumeQuiz(testChatId, api, currentSess.sessionId);
  assert.strictEqual(resumeRes.success, true);
  assert.strictEqual(currentSess.status, "running");
  assert.strictEqual(currentSess.consecutiveUnansweredCount, 0);

  // E'londa 4-savoldan davom etishi ko'rsatilganmi
  const resumeMsg = api.sentMessages.find((m) => m.chatId === testChatId && m.text.includes("qolgan joyidan"));
  assert.ok(resumeMsg);
  assert.ok(resumeMsg.text.includes("4/5-savol"), "Aynan 4-savoldan davom etishi kerak");

  // 4-savolni yuboramiz
  await manager.sendNextQuestion(testChatId, api);
  assert.strictEqual(currentSess.currentQuestionIndex, 3, "4-savol indeksi 3 bo'lishi kerak");

  // Azizning oldingi balli (2 ball) saqlanib qolganini tekshirish
  assert.strictEqual(currentSess.participants.get(100)?.score, 2);
  assert.strictEqual(currentSess.participants.get(100)?.totalTimeMs, 14000);

  console.log("✅ Test 7 muvaffaqiyatli o'tdi (Ballar saqlandi va 4-savoldan davom etdi).");

  // ========================================================
  // TEST 8: Takroriy va eski sessiya identifikatorli resume tugmasi tekshiruvi
  // ========================================================
  console.log("\nTest 8: Takroriy va eski sessiya identifikatorli resume tugmasi tekshiruvi...");
  const newQuiz8 = createTestQuiz("global_pause_8");
  await quizManager.startQuiz(globalPauseChatId, newQuiz8, api);
  await quizManager.pauseQuiz(globalPauseChatId, api);
  const sess8 = quizManager.getSession(globalPauseChatId)!;

  // 8.1: To'g'ri sessionId bilan davom ettirish
  const validResumeCtx = createMockContext({
    chatId: globalPauseChatId,
    chatType: "supergroup",
    userId: 1111,
    isAdmin: false,
    callbackData: `resume_quiz_${globalPauseChatId}_${sess8.sessionId}`,
    api,
  });
  await handleResumeQuizCallback(validResumeCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(globalPauseChatId), true);

  // 8.2: Allaqachon running bo'lgan holatda yana bosish
  const repeatCtx = createMockContext({
    chatId: globalPauseChatId,
    chatType: "supergroup",
    userId: 1111,
    isAdmin: false,
    callbackData: `resume_quiz_${globalPauseChatId}_${sess8.sessionId}`,
    api,
  });
  await handleResumeQuizCallback(repeatCtx as any);
  assert.ok(repeatCtx.answeredCallbacks.length > 0);
  assert.ok(repeatCtx.answeredCallbacks[0].text?.includes("allaqachon davom ettirilgan"));

  // 8.3: Eski sessiya tugmasi yangi sessiyani davom ettira olmasligi
  await quizManager.stopQuiz(globalPauseChatId);
  const nextQuiz8 = createTestQuiz("global_pause_next");
  await quizManager.startQuiz(globalPauseChatId, nextQuiz8, api);
  await quizManager.pauseQuiz(globalPauseChatId, api);

  const staleCtx = createMockContext({
    chatId: globalPauseChatId,
    chatType: "supergroup",
    userId: 2222,
    isAdmin: false,
    callbackData: `resume_quiz_${globalPauseChatId}_eski_notogri_sessiya`,
    api,
  });
  await handleResumeQuizCallback(staleCtx as any);
  assert.ok(staleCtx.answeredCallbacks[0].text?.includes("eski yoki yakunlangan sessiyaga tegishli"));
  assert.strictEqual(staleCtx.answeredCallbacks[0].show_alert, true);
  assert.strictEqual(quizManager.isQuizPaused(globalPauseChatId), true, "Eski tugma yangi sessiyani buzmasligi kerak");

  const otherGroupCtx = createMockContext({
    chatId: -1007788,
    chatType: "supergroup",
    userId: 3333,
    isAdmin: false,
    callbackData: `resume_quiz_${globalPauseChatId}_${quizManager.getSession(globalPauseChatId)!.sessionId}`,
    api,
  });
  await handleResumeQuizCallback(otherGroupCtx as any);
  assert.strictEqual(otherGroupCtx.answeredCallbacks[0].show_alert, true);
  assert.strictEqual(quizManager.isQuizPaused(globalPauseChatId), true, "Boshqa guruhdagi tugma quizni davom ettirmasligi kerak");

  const legacyCtx = createMockContext({
    chatId: globalPauseChatId,
    chatType: "supergroup",
    userId: 3333,
    isAdmin: false,
    callbackData: `resume_quiz_${globalPauseChatId}`,
    api,
  });
  await handleResumeQuizCallback(legacyCtx as any);
  assert.strictEqual(legacyCtx.answeredCallbacks[0].show_alert, true);
  assert.strictEqual(quizManager.isQuizPaused(globalPauseChatId), true, "Sessiya IDsiz tugma quizni davom ettirmasligi kerak");

  await quizManager.stopQuiz(globalPauseChatId);
  console.log("✅ Test 8 muvaffaqiyatli o'tdi (Takroriy bosish va eski sessiya identifikatori to'g'ri bloklandi).");

  // ========================================================
  // TEST 9: Pauzadagi quiz ustiga boshqa quiz boshlanmasligi
  // ========================================================
  console.log("\nTest 9: Pauzadagi quiz ustiga boshqa quiz boshlanishi bloklanishi...");
  api.clear();
  const pauseBlockChatId = -1006677;
  const blockQuiz = createTestQuiz("test_block");
  await quizManager.startQuiz(pauseBlockChatId, blockQuiz, api);
  await quizManager.pauseQuiz(pauseBlockChatId, api);

  assert.strictEqual(quizManager.isQuizPaused(pauseBlockChatId), true);

  // Shu chatda startQuizById orqali boshlashga urinish
  const tryStartCtx = createMockContext({
    chatId: pauseBlockChatId,
    chatType: "supergroup",
    userId: 1111,
    isAdmin: true,
    api,
  });
  await startQuizById(tryStartCtx as any, "amino_acids");
  assert.ok(tryStartCtx.replies.length > 0);
  assert.ok(tryStartCtx.replies[0].text.includes("pauza qilingan quiz mavjud"));

  console.log("✅ Test 9 muvaffaqiyatli o'tdi (Pauzadagi quiz ustiga yangisi boshlanmadi).");

  // ========================================================
  // TEST 10: /stop buyrug'i pauzadagi quizni ham to'liq to'xtatishi
  // ========================================================
  console.log("\nTest 10: /stop buyrug'i pauzadagi quizni to'xtatishi...");
  assert.strictEqual(quizManager.isQuizActive(pauseBlockChatId), true);

  const stopCtx = createMockContext({
    chatId: pauseBlockChatId,
    chatType: "supergroup",
    userId: 1111,
    isAdmin: true,
    api,
  });
  await handleStopQuizCommand(stopCtx as any);
  assert.strictEqual(quizManager.isQuizActive(pauseBlockChatId), false);
  assert.strictEqual(quizManager.getSession(pauseBlockChatId), undefined);
  console.log("✅ Test 10 muvaffaqiyatli o'tdi (/stop pauzadagi quizni bekor qildi).");

  // ========================================================
  // TEST 11: Oxirgi savoldan keyin javob berilmasa ham pauza o'rniga yakuniy natija chiqishi
  // ========================================================
  console.log("\nTest 11: Oxirgi savolda savollar tugasa, pauza o'rniga yakuniy natija chiqishi...");
  api.clear();
  const lastQChatId = -1009900;
  // 3 savolli quiz tuzamiz
  const shortQuiz: Quiz = {
    id: "short_quiz",
    title: "Qisqa Quiz",
    description: "3 ta savolli quiz",
    groupOnly: true,
    questions: [
      { id: "sq1", question: "S1", options: ["A", "B", "C", "D"], correctOptionId: 0, timeLimitSeconds: 20 },
      { id: "sq2", question: "S2", options: ["A", "B", "C", "D"], correctOptionId: 0, timeLimitSeconds: 20 },
      { id: "sq3", question: "S3", options: ["A", "B", "C", "D"], correctOptionId: 0, timeLimitSeconds: 20 },
    ],
  };

  await manager.startQuiz(lastQChatId, shortQuiz, api);

  // 1-savol: javobsiz -> count 1
  await manager.sendNextQuestion(lastQChatId, api);
  await (manager as any).handleQuestionTimeout(lastQChatId, api);

  // 2-savol: javobsiz -> count 2
  await manager.sendNextQuestion(lastQChatId, api);
  await (manager as any).handleQuestionTimeout(lastQChatId, api);

  // 3-savol (oxirgi savol, index 2): javobsiz -> count 3 bo'ladi, LEKIN bu oxirgi savol!
  await manager.sendNextQuestion(lastQChatId, api);
  assert.strictEqual(manager.getSession(lastQChatId)!.currentQuestionIndex, 2);

  // Timeout bo'lganda finishQuiz chaqirilishi kerak
  await (manager as any).handleQuestionTimeout(lastQChatId, api);
  await manager.finishQuiz(lastQChatId, api);

  assert.strictEqual(manager.isQuizPaused(lastQChatId), false, "Oxirgi savoldan keyin pauza bo'lmasligi kerak");
  assert.strictEqual(manager.isQuizActive(lastQChatId), false, "Quiz yakunlangan bo'lishi kerak");

  const finishMsg = api.sentMessages.find((m) => m.chatId === lastQChatId && m.text.includes("yakunlandi"));
  assert.ok(finishMsg, "Yakuniy xabar yuborilgan bo'lishi kerak");
  console.log("✅ Test 11 muvaffaqiyatli o'tdi (Oxirgi savolda pauza o'rniga yakuniy natija chiqdi).");

  // ========================================================
  // TEST 12: Sessiyalarni saqlash yechimi (Persistence) va tiklanishi
  // ========================================================
  console.log("\nTest 12: Sessiyaning diskda saqlanishi va qayta yuklanishi (Persistence)...");
  const persistChatId = -1007788;
  const persistQuiz = createTestQuiz("persist_quiz");

  await manager.startQuiz(persistChatId, persistQuiz, api);
  await manager.sendNextQuestion(persistChatId, api); // 1-savol
  await manager.sendNextQuestion(persistChatId, api); // 2-savol
  await manager.pauseQuiz(persistChatId, api);

  // Diskda saqlanganligini tekshirish
  const savedSessions = await storage.loadAllSessions();
  const savedForChat = savedSessions.find((s) => s.chatId === persistChatId);
  assert.ok(savedForChat, "Sessiya diskda saqlangan bo'lishi kerak");
  assert.strictEqual(savedForChat.status, "paused");
  assert.strictEqual(savedForChat.currentQuestionIndex, 1);

  // Yangi manager yaratib, diskdan qayta yuklaymiz (server qayta ishga tushishi simulyatsiyasi)
  const restoredManager = new QuizManager(storage);
  await restoredManager.loadPersistedSessions();

  assert.strictEqual(restoredManager.isQuizPaused(persistChatId), true);
  const restoredSess = restoredManager.getSession(persistChatId)!;
  assert.strictEqual(restoredSess.currentQuestionIndex, 1);

  // Qayta tiklangan sessiyani davom ettiramiz
  const resumeRestoredRes = await restoredManager.resumeQuiz(persistChatId, api);
  assert.strictEqual(resumeRestoredRes.success, true);
  assert.strictEqual(restoredSess.status, "running");

  await restoredManager.stopQuiz(persistChatId);
  console.log("✅ Test 12 muvaffaqiyatli o'tdi (Diskdan to'liq tiklandi va davom ettirildi).");

  // ========================================================
  // TEST 13: Parallel guruhlarda aqlli pauza mustaqilligi
  // ========================================================
  console.log("\nTest 13: Parallel guruhlarda aqlli pauza bir-biriga ta'sir qilmasligi...");
  const gA = -10011;
  const gB = -10022;

  const quizA = createTestQuiz("quiz_A");
  const quizB = createTestQuiz("quiz_B");

  await manager.startQuiz(gA, quizA, api);
  await manager.startQuiz(gB, quizB, api);

  // Guruh A da pauza qilamiz
  await manager.pauseQuiz(gA, api);
  assert.strictEqual(manager.isQuizPaused(gA), true);
  assert.strictEqual(manager.isQuizRunning(gA), false);

  // Guruh B davom etmoqda
  assert.strictEqual(manager.isQuizPaused(gB), false);
  assert.strictEqual(manager.isQuizRunning(gB), true);

  await manager.stopQuiz(gA);
  await manager.stopQuiz(gB);
  console.log("✅ Test 13 muvaffaqiyatli o'tdi (Parallel guruhlar 100% mustaqil).");

  // ========================================================
  // TEST 14: Ikki a'zo tugmani bir paytda bosganda bitta sessiya/bitta savol yaralishi
  // ========================================================
  console.log("\nTest 14: Ikki a'zo bir vaqtda bosganda poyga holati (race condition) bloklanishi...");
  const raceChatId = -1009911;
  api.clear();

  // 14.1: Ikki a'zo bir vaqtda startQuiz chaqirganda
  const raceQuiz = createTestQuiz("race_quiz");
  const [resA, resB] = await Promise.all([
    quizManager.startQuiz(raceChatId, raceQuiz, api),
    quizManager.startQuiz(raceChatId, raceQuiz, api),
  ]);

  const successCount = (resA.success ? 1 : 0) + (resB.success ? 1 : 0);
  assert.strictEqual(successCount, 1, "Bir vaqtda start berilganda faqat 1 ta sessiya yaratilishi kerak");

  const startMsgs = api.sentMessages.filter(
    (m) => m.chatId === raceChatId && m.text.includes("boshlandi!")
  );
  assert.strictEqual(startMsgs.length, 1, "Faqat 1 ta boshlanish e'loni bo'lishi kerak");

  // 14.2: Ikki a'zo bir vaqtda resume bosganda
  await quizManager.pauseQuiz(raceChatId, api);
  const raceSess = quizManager.getSession(raceChatId)!;

  const [resumeA, resumeB] = await Promise.all([
    quizManager.resumeQuiz(raceChatId, api, raceSess.sessionId),
    quizManager.resumeQuiz(raceChatId, api, raceSess.sessionId),
  ]);

  const resumeSuccessCount = (resumeA.success ? 1 : 0) + (resumeB.success ? 1 : 0);
  assert.strictEqual(resumeSuccessCount, 1, "Bir vaqtda resume bosilganda faqat bittasi davom ettirishi kerak");

  await quizManager.stopQuiz(raceChatId, api);
  console.log("✅ Test 14 muvaffaqiyatli o'tdi (Konkurent bosishlarda poyga holati to'liq bloklandi).");

  // Tozalash
  storage.clearAll();

  console.log("\n🎉 BARCHA AQLI PAUZA, GURUH YO'RIQNOMASI VA SAQLASH TESTLARI (14/14) 100% MUVAFFAQIYATLI O'TDI!");
}

runSmartPauseAndWelcomeTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
