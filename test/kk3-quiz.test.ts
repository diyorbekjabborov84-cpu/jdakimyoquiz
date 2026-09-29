import assert from "node:assert";
import {
  getAllQuizzes,
  getQuizById,
  kk3Quiz1,
  kk3Quiz2,
} from "../src/quiz/questions.js";
import {
  QuizManager,
  TelegramApiSender,
  prepareSessionQuiz,
  quizManager,
} from "../src/quiz/quizManager.js";
import {
  startQuizById,
  handleQuizByIdCommand,
  handleStopQuizCommand,
  handleRestartQuizCallback,
  handleResumeQuizCallback,
} from "../src/bot/handlers/quiz.js";
import { handleStart } from "../src/bot/handlers/start.js";

// Mock Telegram API Sender
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

  private nextMessageId = 100;
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
    const pollId = `poll_kk3_${this.nextPollId++}`;
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
    message: {
      text: options.text || "",
      chat: { id: options.chatId, type: options.chatType },
      from: {
        id: options.userId,
        first_name: options.firstName || "TestUser",
        username: options.username || "testuser",
      },
    },
    callbackQuery: options.callbackData
      ? {
          data: options.callbackData,
          message: { chat: { id: options.chatId, type: options.chatType }, message_id: 999 },
          from: {
            id: options.userId,
            first_name: options.firstName || "TestUser",
            username: options.username || "testuser",
          },
        }
      : undefined,
    match: options.match,
    api: options.api,
    me: { username: "jdakimyoquizbot" },
    replies,
    answeredCallbacks,
    reply: async (text: string, other?: any) => {
      replies.push({ text, other });
      return options.api.sendMessage(options.chatId, text, other);
    },
    answerCallbackQuery: async (opts?: any) => {
      answeredCallbacks.push(opts || {});
      return true;
    },
    getChatMember: async (userId: number) => {
      if (options.isAdmin) {
        return { status: "administrator", user: { id: userId } };
      }
      return { status: "member", user: { id: userId } };
    },
  };
}

async function runKK3Tests() {
  console.log("==================================================================");
  console.log("KOLLOID KIMYO — SIRT HODISALARI (KK3_1, KK3_2) INTEGRATSIYA TESTLARI");
  console.log("==================================================================");

  const api = new MockTelegramApi();

  // -------------------------------------------------------------
  // Test 1: Savollar to'plami va strukturasi (40 ta unikal savol)
  // -------------------------------------------------------------
  console.log("\nTest 1: Savollar to'plami va strukturasi tekshiruvi...");
  assert.strictEqual(kk3Quiz1.id, "KK3_1");
  assert.strictEqual(kk3Quiz2.id, "KK3_2");

  assert.strictEqual(kk3Quiz1.questions.length, 20, "KK3_1 da 20 ta savol bo'lishi kerak");
  assert.strictEqual(kk3Quiz2.questions.length, 20, "KK3_2 da 20 ta savol bo'lishi kerak");

  const allKk3Quizzes = [kk3Quiz1, kk3Quiz2];
  const allQuestionTexts = new Set<string>();

  for (const quiz of allKk3Quizzes) {
    assert.strictEqual(quiz.groupOnly, true, `${quiz.id} groupOnly: true bo'lishi kerak`);
    assert.strictEqual(quiz.shuffle, true, `${quiz.id} shuffle: true bo'lishi kerak`);
    assert.strictEqual(
      quiz.source,
      "Bahora Nayimova slaydlaridan",
      `${quiz.id} source to'g'ri ko'rsatilishi kerak`
    );

    for (const q of quiz.questions) {
      assert.ok(q.question && q.question.trim().length > 0, "Savol matni bo'sh bo'lmasligi kerak");
      assert.ok(!q.question.includes("Slayd:"), "Savol matnida Slayd bo'lmasligi kerak");
      assert.ok(!q.question.includes("Izoh:"), "Savol matnida Izoh bo'lmasligi kerak");
      assert.ok(!q.question.includes("Rasm:"), "Savol matnida Rasm bo'lmasligi kerak");
      assert.ok(q.question.length <= 300, "Savol matni 300 belgidan oshmasligi kerak");
      assert.strictEqual(q.options.length, 4, "Aynan 4 ta variant bo'lishi kerak");
      for (const opt of q.options) {
        assert.ok(opt.length <= 100, "Variant 100 belgidan oshmasligi kerak");
      }
      assert.ok(
        q.correctOptionId >= 0 && q.correctOptionId <= 3,
        "To'g'ri javob indeksi 0-3 oralig'ida bo'lishi kerak"
      );
      assert.strictEqual(q.timeLimitSeconds, 20, "Savol vaqti 20 soniya bo'lishi kerak");
      assert.ok(q.explanation && q.explanation.length > 0, "Izoh mavjud bo'lishi kerak");

      allQuestionTexts.add(q.question);
    }
  }

  assert.strictEqual(allQuestionTexts.size, 40, "Barcha 40 ta savol o'zaro unikal bo'lishi kerak");
  console.log("✅ Test 1 muvaffaqiyatli o'tdi (40 ta unikal savol, 4 ta variant, 20s va izohlar tasdiqlandi).");

  // -------------------------------------------------------------
  // Test 2: getQuizById qidiruvi va sinonimlar
  // -------------------------------------------------------------
  console.log("\nTest 2: getQuizById registratsiyasi va sinonimlar...");
  assert.strictEqual(getQuizById("KK3_1"), kk3Quiz1);
  assert.strictEqual(getQuizById("kk3_1"), kk3Quiz1);
  assert.strictEqual(getQuizById("quiz_KK3_1"), kk3Quiz1);
  assert.strictEqual(getQuizById("start_kk3_1"), kk3Quiz1);
  assert.strictEqual(getQuizById("kk3-1"), kk3Quiz1);
  assert.strictEqual(getQuizById("kk_3_1"), kk3Quiz1);
  assert.strictEqual(getQuizById("kk31"), kk3Quiz1);

  assert.strictEqual(getQuizById("KK3_2"), kk3Quiz2);
  assert.strictEqual(getQuizById("kk3_2"), kk3Quiz2);
  assert.strictEqual(getQuizById("quiz_kk3_2"), kk3Quiz2);
  assert.strictEqual(getQuizById("start_kk3_2"), kk3Quiz2);
  assert.strictEqual(getQuizById("kk3-2"), kk3Quiz2);
  assert.strictEqual(getQuizById("kk_3_2"), kk3Quiz2);
  assert.strictEqual(getQuizById("kk32"), kk3Quiz2);

  const registered = getAllQuizzes();
  assert.ok(registered.some((q) => q.id === "KK3_1"));
  assert.ok(registered.some((q) => q.id === "KK3_2"));
  console.log("✅ Test 2 muvaffaqiyatli o'tdi (Barcha ID va sinonimlar registratsiyadan o'tdi).");

  // -------------------------------------------------------------
  // Test 3: prepareSessionQuiz dinamik aralashtirish va to'g'ri javob tekshiruvi
  // -------------------------------------------------------------
  console.log("\nTest 3: Dinamik aralashtirish va to'g'ri javobni qayta hisoblash...");
  for (let iter = 0; iter < 50; iter++) {
    const sessionQuiz = prepareSessionQuiz(kk3Quiz1);
    assert.strictEqual(sessionQuiz.questions.length, 20);

    for (let i = 0; i < sessionQuiz.questions.length; i++) {
      const sq = sessionQuiz.questions[i];
      const origQ = kk3Quiz1.questions.find((q) => q.id === sq.id);
      assert.ok(origQ, `Asl savol topilmadi: ${sq.id}`);

      const origCorrectText = origQ.options[origQ.correctOptionId];
      const newCorrectText = sq.options[sq.correctOptionId];
      assert.strictEqual(
        newCorrectText,
        origCorrectText,
        `Savol ${sq.id} uchun to'g'ri javob matni saqlanmadi!`
      );
      assert.strictEqual(sq.timeLimitSeconds, 20);
    }
  }
  console.log("✅ Test 3 muvaffaqiyatli o'tdi (50 marta mustaqil aralashtirildi, indekslar 100% to'g'ri moslashdi).");

  // -------------------------------------------------------------
  // Test 4: Shaxsiy chatda bloklash va guruhga havola berish
  // -------------------------------------------------------------
  console.log("\nTest 4: Shaxsiy chatda KK3 quizlarini bloklash...");
  api.clear();
  const privateCtx = createMockContext({
    chatId: 12345,
    chatType: "private",
    userId: 12345,
    match: "KK3_1",
    api,
  });

  await handleQuizByIdCommand(privateCtx as any);
  assert.strictEqual(api.sentPolls.length, 0, "Shaxsiy chatda poll yuborilmasligi kerak");
  assert.strictEqual(api.sentMessages.length, 1, "Guruhga yo'naltirish xabari chiqishi kerak");
  assert.ok(
    api.sentMessages[0].text.includes("faqat Telegram guruhlarida"),
    "Guruh xabarnomasi bo'lishi kerak"
  );
  assert.ok(
    api.sentMessages[0].other?.reply_markup?.inline_keyboard[0][0]?.url?.includes("startgroup=quiz_KK3_1"),
    "startgroup=quiz_KK3_1 tugmasi bo'lishi kerak"
  );
  console.log("✅ Test 4 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 5: Shaxsiy chatda deep link (?start=quiz_KK3_2) bloklanishi
  // -------------------------------------------------------------
  console.log("\nTest 5: Shaxsiy chatda deep link (?start=quiz_KK3_2)...");
  api.clear();
  const deepLinkCtx = createMockContext({
    chatId: 54321,
    chatType: "private",
    userId: 54321,
    match: "quiz_KK3_2",
    api,
  });

  await handleStart(deepLinkCtx as any);
  assert.strictEqual(api.sentPolls.length, 0, "Shaxsiy chatda poll boshlanmasligi kerak");
  assert.strictEqual(api.sentMessages.length, 1);
  assert.ok(api.sentMessages[0].text.includes("faqat Telegram guruhlarida"));
  console.log("✅ Test 5 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 6: Guruhda quiz boshlash (/quiz_KK3_1)
  // -------------------------------------------------------------
  console.log("\nTest 6: Guruhda quiz boshlash (/quiz_KK3_1)...");
  api.clear();
  const groupChatId = -100889900;
  const groupCtx = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: 9988,
    match: "KK3_1",
    api,
  });

  await handleQuizByIdCommand(groupCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(groupChatId), true, "Quiz faol bo'lishi kerak");
  assert.strictEqual(api.sentMessages.length, 1, "E'lon xabari chiqishi kerak");
  assert.ok(api.sentMessages[0].text.includes("Kolloid kimyo — 3-mavzu 1-qism (KK3_1)"));

  // 1-savol yuboriladi
  await quizManager.sendNextQuestion(groupChatId, api);
  assert.strictEqual(api.sentPolls.length, 1, "1-savol yuborilishi kerak");
  assert.strictEqual(api.sentPolls[0].other?.open_period, 20, "Telegram taymeri 20 soniya bo'lishi kerak");
  console.log("✅ Test 6 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 7: Guruhda faol quiz turganda yangisi bloklanishi
  // -------------------------------------------------------------
  console.log("\nTest 7: Faol quiz turganda yangi start bloklanishi...");
  api.clear();
  const blockedCtx = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: 7766,
    match: "KK3_2",
    api,
  });

  await handleQuizByIdCommand(blockedCtx as any);
  assert.strictEqual(api.sentPolls.length, 0, "Yangi poll yuborilmasligi kerak");
  assert.strictEqual(api.sentMessages.length, 1, "Ogohlantirish xabari yuborilishi kerak");
  assert.ok(api.sentMessages[0].text.includes("allaqachon faol quiz davom etmoqda"));
  console.log("✅ Test 7 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 8: /stop buyrug'i faol KK3 quizini to'xtatishi
  // -------------------------------------------------------------
  console.log("\nTest 8: /stop buyrug'i orqali to'xtatish...");
  api.clear();
  const stopCtx = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: 9988,
    isAdmin: true,
    api,
  });

  await handleStopQuizCommand(stopCtx as any);
  assert.ok(api.stoppedPolls.length >= 1, "Poll to'xtatilgan bo'lishi kerak");
  assert.ok(api.sentMessages.some((m) => m.text.includes("Quiz to'xtatildi")));
  assert.strictEqual(quizManager.isQuizRunning(groupChatId), false, "Quiz to'xtatilgan bo'lishi kerak");
  console.log("✅ Test 8 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 9: Hech kim javob bermagan holatda yakuniy xabar, muallif, manba va tugmalar
  // -------------------------------------------------------------
  console.log("\nTest 9: Javobsiz yakunlangan KK3 quizi...");
  api.clear();
  const emptyChatId = -1004455;
  const emptyCtx = createMockContext({
    chatId: emptyChatId,
    chatType: "supergroup",
    userId: 1111,
    match: "KK3_2",
    api,
  });

  await handleQuizByIdCommand(emptyCtx as any);
  api.clear();

  // Test QuizManager orqali to'g'ridan-to'g'ri finishQuiz chaqiramiz
  await quizManager.finishQuiz(emptyChatId, api);

  assert.strictEqual(api.sentMessages.length, 1, "Faqat 1 ta yakuniy xabar yuborilishi kerak");
  const finalMsg = api.sentMessages[0];
  assert.ok(finalMsg.text.includes("yakunlandi"));
  assert.ok(finalMsg.text.includes("👥 Qatnashchilar soni: <b>0 ta</b>"), "0 ta qatnashchi ko'rsatilishi kerak");
  assert.ok(finalMsg.text.includes("@diyorbek_jabborov"), "Muallif chiqishi shart");
  assert.ok(finalMsg.text.includes("Bahora Nayimova slaydlaridan"), "Manba chiqishi shart");

  // Ikkala tugma borligi
  const buttons = finalMsg.other?.reply_markup?.inline_keyboard;
  assert.ok(buttons, "Inline keyboard bo'lishi kerak");
  const buttonTexts = buttons.flat().map((b: any) => b.text);
  assert.ok(buttonTexts.some((t: string) => t.includes("📢 Quiz kodlari")), "Kanal tugmasi bo'lishi kerak");
  assert.ok(buttonTexts.some((t: string) => t.includes("🔄 Qayta yechish")), "Qayta yechish tugmasi bo'lishi kerak");
  console.log("✅ Test 9 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 10: «🔄 Qayta yechish» callback orqali KK3_1 ni qayta boshlash
  // -------------------------------------------------------------
  console.log("\nTest 10: «🔄 Qayta yechish» callback query...");
  api.clear();
  const restartChatId = -1005566;
  const restartCtx = createMockContext({
    chatId: restartChatId,
    chatType: "supergroup",
    userId: 5544,
    callbackData: "restart_quiz_KK3_1",
    api,
  });

  await handleRestartQuizCallback(restartCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(restartChatId), true, "Yangi quiz boshlanishi kerak");
  await quizManager.sendNextQuestion(restartChatId, api);
  assert.strictEqual(api.sentPolls.length, 1, "1-savol yuborilishi kerak");
  assert.strictEqual(restartCtx.answeredCallbacks.length, 1);
  assert.ok(restartCtx.answeredCallbacks[0].text?.includes("qayta boshlanmoqda"));

  // To'xtatamiz
  await quizManager.stopQuiz(restartChatId, api);
  console.log("✅ Test 10 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 11: Aqlli pauza va davom ettirish (KK3)
  // -------------------------------------------------------------
  console.log("\nTest 11: KK3 sessiyasida aqlli pauza va resume...");
  api.clear();
  const pauseChatId = -1006677;
  const pauseCtx = createMockContext({
    chatId: pauseChatId,
    chatType: "supergroup",
    userId: 8877,
    match: "KK3_2",
    api,
  });

  await handleQuizByIdCommand(pauseCtx as any);
  await quizManager.sendNextQuestion(pauseChatId, api);
  const activeSession = (quizManager as any).sessions.get(pauseChatId);
  assert.ok(activeSession, "Sessiya topilishi kerak");

  // Aqlli pauza chaqiramiz
  await (quizManager as any).pauseQuiz(pauseChatId, api);

  assert.strictEqual(quizManager.isQuizPaused(pauseChatId), true, "Quiz pauzalangan bo'lishi kerak");
  const pauseMsg = api.sentMessages.find((m) => m.text.includes("Quiz vaqtincha to‘xtatildi"));
  assert.ok(pauseMsg, "Pauza xabari yuborilgan bo'lishi kerak");
  const resumeButton = pauseMsg?.other?.reply_markup?.inline_keyboard[0][0];
  assert.ok(
    resumeButton && resumeButton.callback_data.startsWith(`resume_quiz_${pauseChatId}`),
    "Davom ettirish tugmasi bo'lishi kerak"
  );

  // Resume bosish
  api.clear();
  const resumeCtx = createMockContext({
    chatId: pauseChatId,
    chatType: "supergroup",
    userId: 1234,
    callbackData: resumeButton.callback_data,
    api,
  });

  await handleResumeQuizCallback(resumeCtx as any);
  assert.strictEqual(quizManager.isQuizPaused(pauseChatId), false, "Quiz davom etayotgan bo'lishi kerak");

  // Tozalash
  await quizManager.stopQuiz(pauseChatId, api);
  console.log("✅ Test 11 muvaffaqiyatli o'tdi (Aqlli pauza va resume to'liq ishladi).");

  console.log("\n🎉 BARCHA KK3 KOLLOID KIMYO TESTLARI (11/11) 100% MUVAFFAQIYATLI O'TDI!");
}

runKK3Tests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
