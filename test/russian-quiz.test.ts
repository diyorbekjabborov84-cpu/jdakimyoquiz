import assert from "node:assert";
import {
  getAllQuizzes,
  getQuizById,
  russianQuiz1,
  russianQuiz2,
  russianQuiz3,
  russianQuiz4,
  russianQuiz5,
  russianQuiz6,
  allRussianQuizzes,
} from "../src/quiz/questions.js";
import {
  QuizManager,
  quizManager,
  TelegramApiSender,
  prepareSessionQuiz,
} from "../src/quiz/quizManager.js";
import {
  startQuizById,
  handleQuizByIdCommand,
  handleStopQuizCommand,
  handleRestartQuizCallback,
} from "../src/bot/handlers/quiz.js";
import { handleStart } from "../src/bot/handlers/start.js";

// Mock Telegram API Sender
class MockTelegramApi implements TelegramApiSender {
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
    const pollId = `poll_rus_${this.nextPollId++}`;
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
    me: { username: "jdakimyoquizbot" },
    match: options.match ?? "",
    message: { text: options.text ?? "" },
    callbackQuery: options.callbackData ? { data: options.callbackData } : undefined,
    api: options.api,
    replies,
    answeredCallbacks,
    reply: async (text: string, other?: any) => {
      replies.push({ text, other });
      return { message_id: 999, text };
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

async function runRussianQuizTests() {
  console.log("🧪 RUS TILI (R1 - R6) 50 TALIK QUIZLAR TESTI BOSHLANDI...\n");

  const api = new MockTelegramApi();

  // ========================================================
  // TEST 1: Barcha 6 ta 50 talik quiz ro'yxatdan o'tishi va tuzilishi
  // ========================================================
  console.log("Test 1: 6 ta rus tili quizlarining registratsiyasi va 50 talik hajmi...");
  assert.strictEqual(allRussianQuizzes.length, 6, "Aniq 6 ta Rus tili quizi bo'lishi kerak");

  const expectedIds = ["R1", "R2", "R3", "R4", "R5", "R6"];
  for (let i = 0; i < expectedIds.length; i++) {
    const qId = expectedIds[i];
    const quiz = allRussianQuizzes[i];
    assert.strictEqual(quiz.id, qId);
    assert.strictEqual(quiz.questions.length, 50, `${qId} quizi aynan 50 ta savoldan iborat bo'lishi kerak`);
    assert.strictEqual(quiz.groupOnly, true, `${qId} groupOnly: true bo'lishi kerak`);
    assert.strictEqual(quiz.shuffle, true, `${qId} shuffle: true bo'lishi kerak`);

    // Har bir savol 20 soniya, 4 ta variant va to'g'ri javob 0-indeks
    for (let j = 0; j < quiz.questions.length; j++) {
      const q = quiz.questions[j];
      assert.strictEqual(q.timeLimitSeconds, 20, `${qId} savol ${j + 1} 20 soniya bo'lishi kerak`);
      assert.strictEqual(q.options.length, 4, `${qId} savol ${j + 1} 4 ta variantga ega bo'lishi kerak`);
      assert.strictEqual(q.correctOptionId, 0, `${qId} savol ${j + 1} da 1-ustun to'g'ri javob (indeks 0) bo'lishi kerak`);
      assert.ok(q.question.trim().length > 0, "Savol matni bo'sh bo'lmasligi kerak");
    }
  }
  console.log("✅ Test 1 muvaffaqiyatli o'tdi (Barcha R1-R6 quizlari 50 ta savol, 20s, 4 variant, 0-indeks to'g'ri).");

  // ========================================================
  // TEST 2: 6-chi 50 talik (R6) to'ldirilishi tekshiruvi
  // ========================================================
  console.log("\nTest 2: R6 quizi yetmagan qismi R5 dan olingani tekshiruvi...");
  assert.strictEqual(russianQuiz6.questions.length, 50);
  // Dastlabki 48 ta savol manbadagi 251-298 savollar
  // 49 va 50-savollar 5-chi 50 talikdan olingan
  const r6_q49 = russianQuiz6.questions[48];
  const r6_q50 = russianQuiz6.questions[49];
  const r5_q1 = russianQuiz5.questions[0];
  const r5_q2 = russianQuiz5.questions[1];
  assert.strictEqual(r6_q49.question, r5_q1.question, "49-savol R5 ning 1-savoli bilan to'ldirilgan bo'lishi kerak");
  assert.strictEqual(r6_q50.question, r5_q2.question, "50-savol R5 ning 2-savoli bilan to'ldirilgan bo'lishi kerak");
  console.log("✅ Test 2 muvaffaqiyatli o'tdi (R6 aynan 50 taga to'ldirilgan).");

  // ========================================================
  // TEST 3: getQuizById qidiruvining moslashuvchanligi (/start_R1, /quiz_r1, r1)
  // ========================================================
  console.log("\nTest 3: getQuizById ID va prefikslar orqali topilishi...");
  assert.strictEqual(getQuizById("R1"), russianQuiz1);
  assert.strictEqual(getQuizById("r1"), russianQuiz1);
  assert.strictEqual(getQuizById("start_R1"), russianQuiz1);
  assert.strictEqual(getQuizById("start_r1"), russianQuiz1);
  assert.strictEqual(getQuizById("quiz_R1"), russianQuiz1);
  assert.strictEqual(getQuizById("quiz_r1"), russianQuiz1);
  assert.strictEqual(getQuizById("r_1"), russianQuiz1);
  assert.strictEqual(getQuizById("r-1"), russianQuiz1);

  assert.strictEqual(getQuizById("R2"), russianQuiz2);
  assert.strictEqual(getQuizById("start_R2"), russianQuiz2);
  assert.strictEqual(getQuizById("R3"), russianQuiz3);
  assert.strictEqual(getQuizById("start_R3"), russianQuiz3);
  assert.strictEqual(getQuizById("R4"), russianQuiz4);
  assert.strictEqual(getQuizById("start_R4"), russianQuiz4);
  assert.strictEqual(getQuizById("R5"), russianQuiz5);
  assert.strictEqual(getQuizById("start_R5"), russianQuiz5);
  assert.strictEqual(getQuizById("R6"), russianQuiz6);
  assert.strictEqual(getQuizById("start_R6"), russianQuiz6);
  console.log("✅ Test 3 muvaffaqiyatli o'tdi.");

  // ========================================================
  // TEST 4: Aralashtirish algoritmi (prepareSessionQuiz) va to'g'ri javob indeksi
  // ========================================================
  console.log("\nTest 4: prepareSessionQuiz da variantlar aralashganda to'g'ri javob saqlanishi...");
  for (let iter = 1; iter <= 20; iter++) {
    const sessionQuiz = prepareSessionQuiz(russianQuiz1);
    assert.strictEqual(sessionQuiz.questions.length, 50);

    for (const sq of sessionQuiz.questions) {
      const orig = russianQuiz1.questions.find((x) => x.id === sq.id)!;
      const origCorrectText = orig.options[orig.correctOptionId];
      const sessionCorrectText = sq.options[sq.correctOptionId];

      assert.strictEqual(
        sessionCorrectText,
        origCorrectText,
        `Iter ${iter}: ${sq.id} da to'g'ri javob mos kelmadi!`
      );
    }
  }
  console.log("✅ Test 4 muvaffaqiyatli o'tdi (20 marta mustaqil tekshiruvda to'g'ri javob 100% aniq saqlandi).");

  // ========================================================
  // TEST 5: Shaxsiy chatda /start_R1 yoki /quiz_R1 bloklanishi
  // ========================================================
  console.log("\nTest 5: Shaxsiy chatda R1 boshlash bloklanishi va guruhga yo'naltirish...");
  api.clear();

  const privateCtx = createMockContext({
    chatId: 887766,
    chatType: "private",
    userId: 887766,
    match: ["/start_R1", "R1"],
    api,
  });

  await handleQuizByIdCommand(privateCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(887766), false, "Shaxsiy chatda quiz boshlanmasligi shart");
  assert.strictEqual(privateCtx.replies.length, 1);
  assert.ok(privateCtx.replies[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"));
  assert.ok(
    privateCtx.replies[0].other?.reply_markup?.inline_keyboard[0][0]?.url.includes("startgroup=quiz_R1")
  );
  console.log("✅ Test 5 muvaffaqiyatli o'tdi.");

  // ========================================================
  // TEST 6: Guruhda admin /start_R1 orqali test boshlashi
  // ========================================================
  console.log("\nTest 6: Guruhda admin /start_R1 buyrug'i orqali test boshlashi...");
  api.clear();

  const groupChatId = -100551122;
  const adminGroupCtx = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: 1100,
    isAdmin: true,
    match: ["/start_R1", "R1"],
    api,
  });

  await handleQuizByIdCommand(adminGroupCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(groupChatId), true, "Guruhda quiz boshlanishi kerak");
  const startMsg = api.sentMessages.find((m) => m.chatId === groupChatId && m.text.includes("R1"));
  assert.ok(startMsg !== undefined, "E'lon xabari yuborilishi kerak");

  await quizManager.sendNextQuestion(groupChatId, api);
  assert.strictEqual(api.sentPolls.length, 1, "Birinchi poll yuborilishi kerak");
  assert.strictEqual(api.sentPolls[0].other?.open_period, 20, "Poll taymeri 20s bo'lishi kerak");

  // Faol quizni to'xtatamiz
  await handleStopQuizCommand(adminGroupCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(groupChatId), false);
  console.log("✅ Test 6 muvaffaqiyatli o'tdi.");

  // ========================================================
  // TEST 7: Guruhda oddiy foydalanuvchi /start_R1 ni boshlay olishi va /stop da rad etilishi
  // ========================================================
  console.log("\nTest 7: Guruhda oddiy a'zo /start_R1 ni boshlay olishi va /stop da rad etilishi...");
  api.clear();

  const nonAdminCtx = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: 2200,
    isAdmin: false,
    match: ["/start_R1", "R1"],
    api,
  });

  await handleQuizByIdCommand(nonAdminCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(groupChatId), true, "Oddiy a'zo /start_R1 ni boshlay olishi kerak");

  // Oddiy a'zo to'xtata olmasligi kerak
  await handleStopQuizCommand(nonAdminCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(groupChatId), true, "Oddiy a'zo to'xtata olmasligi kerak");
  assert.ok(nonAdminCtx.replies[0].text.includes("faqat guruh adminlariga berilgan"));

  // Admin to'xtatadi
  const adminStopCtx = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: 1100,
    isAdmin: true,
    api,
  });
  await handleStopQuizCommand(adminStopCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(groupChatId), false);
  console.log("✅ Test 7 muvaffaqiyatli o'tdi.");

  // ========================================================
  // TEST 8: Deep link orqali guruhda ?start=R2 ochilishi
  // ========================================================
  console.log("\nTest 8: Deep link (?start=R2 yoki ?startgroup=R2) orqali guruhda ochish...");
  api.clear();

  const deepGroupCtx = createMockContext({
    chatId: -100662233,
    chatType: "supergroup",
    userId: 3300,
    isAdmin: true,
    match: "R2",
    api,
  });

  await handleStart(deepGroupCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(-100662233), true);
  await quizManager.stopQuiz(-100662233, api);
  console.log("✅ Test 8 muvaffaqiyatli o'tdi.");

  // ========================================================
  // TEST 9: Parallel ikkita guruhda mustaqil R1 va R2 quizlari
  // ========================================================
  console.log("\nTest 9: Ikki guruhda parallel R1 va R2 quizlari...");
  api.clear();
  const g1 = -1007711;
  const g2 = -1007722;

  const isolatedManager = new QuizManager();
  await isolatedManager.startQuiz(g1, russianQuiz1, api);
  await isolatedManager.startQuiz(g2, russianQuiz2, api);

  assert.strictEqual(isolatedManager.isQuizRunning(g1), true);
  assert.strictEqual(isolatedManager.isQuizRunning(g2), true);

  await isolatedManager.stopQuiz(g1, api);
  assert.strictEqual(isolatedManager.isQuizRunning(g1), false);
  assert.strictEqual(isolatedManager.isQuizRunning(g2), true);

  await isolatedManager.stopQuiz(g2, api);
  assert.strictEqual(isolatedManager.isQuizRunning(g2), false);
  console.log("✅ Test 9 muvaffaqiyatli o'tdi.");

  // ========================================================
  // TEST 10: 50 talik quiz yakuniy natijalari, ball (X/50) va tugmalar
  // ========================================================
  console.log("\nTest 10: 50 savolli quiz yakuni, 50 dan ball hisobi, muallif va qayta yechish tugmalari...");
  api.clear();
  const simManager = new QuizManager();
  const simChatId = -1008833;

  await simManager.startQuiz(simChatId, russianQuiz1, api);

  // Ishtirokchilar javoblarini simulyatsiya qilish (50 ta savol)
  for (let qIdx = 0; qIdx < 50; qIdx++) {
    await simManager.sendNextQuestion(simChatId, api);
    const lastPoll = api.sentPolls[api.sentPolls.length - 1];
    const correctId = lastPoll.other?.correct_option_ids[0];
    const wrongId = (correctId + 1) % 4;

    // Alisher 50 tasiga to'g'ri javob beradi
    await simManager.handlePollAnswer({
      pollId: lastPoll.pollId,
      user: { id: 10, first_name: "Alisher", username: "alisher" },
      optionIds: [correctId],
    });

    // Bobur 30 tasiga to'g'ri, 20 tasiga noto'g'ri javob beradi
    await simManager.handlePollAnswer({
      pollId: lastPoll.pollId,
      user: { id: 20, first_name: "Bobur", username: "bobur" },
      optionIds: [qIdx < 30 ? correctId : wrongId],
    });
  }

  await simManager.finishQuiz(simChatId, api);
  const finalMsg = api.sentMessages[api.sentMessages.length - 1];

  assert.ok(finalMsg.text.includes("50/50 ball"), "Alisher 50/50 ball olishi kerak");
  assert.ok(finalMsg.text.includes("30/50 ball"), "Bobur 30/50 ball olishi kerak");
  assert.ok(
    finalMsg.text.includes("Test yaratuvchisi: <a href=\"https://t.me/diyorbek_jabborov\">@diyorbek_jabborov</a>"),
    "Yaratuvchi profili bo'lishi kerak"
  );

  const buttons = finalMsg.other?.reply_markup?.inline_keyboard?.flat() || [];
  const restartBtn = buttons.find((b: any) => b.text === "🔄 Qayta yechish");
  assert.ok(restartBtn, "🔄 Qayta yechish tugmasi bo'lishi kerak");
  assert.strictEqual(restartBtn.callback_data, "restart_quiz_R1");

  console.log("✅ Test 10 muvaffaqiyatli o'tdi (Ball 50 tadan hisoblandi, muallif va qayta yechish tasdiqlandi).");

  // ========================================================
  // TEST 11: «🔄 Qayta yechish» orqali R1 ni qayta boshlash
  // ========================================================
  console.log("\nTest 11: «🔄 Qayta yechish» callback orqali R1 ni qayta boshlash...");
  api.clear();

  const restartCtx = createMockContext({
    chatId: simChatId,
    chatType: "supergroup",
    userId: 1100,
    isAdmin: true,
    callbackData: "restart_quiz_R1",
    api,
  });

  await handleRestartQuizCallback(restartCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(simChatId), true);
  await quizManager.stopQuiz(simChatId, api);
  console.log("✅ Test 11 muvaffaqiyatli o'tdi.");

  console.log("\n🎉 BARCHA RUS TILI (R1 - R6) TESTLARI (11/11) 100% MUVAFFAQIYATLI O'TDI!");
}

runRussianQuizTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
