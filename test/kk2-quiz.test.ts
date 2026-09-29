import assert from "node:assert";
import {
  getAllQuizzes,
  getQuizById,
  kk2Quiz1,
  kk2Quiz2,
  kk2Quiz3,
} from "../src/quiz/questions.js";
import {
  QuizManager,
  TelegramApiSender,
  prepareSessionQuiz,
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
    const pollId = `poll_kk2_${this.nextPollId++}`;
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
      options.api.sendMessage(options.chatId, text, other);
      return { message_id: 999, text };
    },
    answerCallbackQuery: async (params?: { text?: string; show_alert?: boolean }) => {
      answeredCallbacks.push(params || {});
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

async function runKK2Tests() {
  console.log("🧪 KK2 KOLLOID KIMYO QUIZLARI TESTLARI BOSHLANDI...\n");
  const api = new MockTelegramApi();

  // -------------------------------------------------------------
  // Test 1: KK2_1, KK2_2, KK2_3 to'plamlarining ro'yxati va 20 tadan savol borligi
  // -------------------------------------------------------------
  console.log("Test 1: KK2 to'plamlarining ro'yxatdan o'tishi va 20 tadan savol borligi...");
  const q1 = getQuizById("KK2_1");
  const q2 = getQuizById("KK2_2");
  const q3 = getQuizById("KK2_3");

  assert.ok(q1, "KK2_1 topilishi kerak");
  assert.ok(q2, "KK2_2 topilishi kerak");
  assert.ok(q3, "KK2_3 topilishi kerak");

  assert.strictEqual(q1.questions.length, 20, "KK2_1 da 20 ta savol bo'lishi kerak");
  assert.strictEqual(q2.questions.length, 20, "KK2_2 da 20 ta savol bo'lishi kerak");
  assert.strictEqual(q3.questions.length, 20, "KK2_3 da 20 ta savol bo'lishi kerak");

  assert.strictEqual(q1.groupOnly, true, "KK2_1 groupOnly bo'lishi kerak");
  assert.strictEqual(q2.groupOnly, true, "KK2_2 groupOnly bo'lishi kerak");
  assert.strictEqual(q3.groupOnly, true, "KK2_3 groupOnly bo'lishi kerak");

  assert.strictEqual(q1.shuffle, true, "KK2_1 shuffle faol bo'lishi kerak");
  assert.strictEqual(q2.shuffle, true, "KK2_2 shuffle faol bo'lishi kerak");
  assert.strictEqual(q3.shuffle, true, "KK2_3 shuffle faol bo'lishi kerak");

  assert.strictEqual(q1.source, "Bahora Nayimova slaydlaridan", "KK2_1 manbasi to'g'ri bo'lishi kerak");
  assert.strictEqual(q2.source, "Bahora Nayimova slaydlaridan", "KK2_2 manbasi to'g'ri bo'lishi kerak");
  assert.strictEqual(q3.source, "Bahora Nayimova slaydlaridan", "KK2_3 manbasi to'g'ri bo'lishi kerak");

  // Har bir savolda 4 ta variant, 20 soniya va to'g'ri indeks [0, 3]
  for (const q of [...q1.questions, ...q2.questions, ...q3.questions]) {
    assert.strictEqual(q.options.length, 4, `Savolda 4 variant bo'lishi kerak: ${q.question}`);
    assert.strictEqual(q.timeLimitSeconds, 20, `Vaqt 20s bo'lishi kerak: ${q.question}`);
    assert.ok(q.correctOptionId >= 0 && q.correctOptionId < 4, "To'g'ri variant indeksi 0-3 oralig'ida bo'lishi kerak");
    assert.ok(!q.question.includes("Slayd:"), `Savol matnida Slayd bo'lmasligi kerak: ${q.question}`);
    assert.ok(!q.question.includes("Izoh:"), `Savol matnida Izoh bo'lmasligi kerak: ${q.question}`);
    assert.ok(q.explanation && q.explanation.length > 0, `Savol izohi bo'lishi kerak: ${q.id}`);
  }

  // Jami 60 ta unikal savol ekani
  const allQTexts = new Set([...q1.questions, ...q2.questions, ...q3.questions].map((x) => x.question));
  assert.strictEqual(allQTexts.size, 60, "Barcha 60 ta savol takrorlanmas unikal bo'lishi kerak");
  console.log("✅ Test 1 muvaffaqiyatli o'tdi (60 ta unikal savol, 3 ta 20 savolli to'plam).");

  // -------------------------------------------------------------
  // Test 2: Case-insensitive va sinonim ID lar orqali topilishi
  // -------------------------------------------------------------
  console.log("\nTest 2: Kichik va katta harflarda ID larni qidirish...");
  assert.strictEqual(getQuizById("kk2_1"), q1);
  assert.strictEqual(getQuizById("KK2_1"), q1);
  assert.strictEqual(getQuizById("quiz_KK2_1"), q1);
  assert.strictEqual(getQuizById("start_KK2_1"), q1);
  assert.strictEqual(getQuizById("kk2-1"), q1);
  assert.strictEqual(getQuizById("kk_2_1"), q1);
  assert.strictEqual(getQuizById("kk21"), q1);

  assert.strictEqual(getQuizById("kk2_2"), q2);
  assert.strictEqual(getQuizById("KK2_2"), q2);
  assert.strictEqual(getQuizById("quiz_KK2_2"), q2);
  assert.strictEqual(getQuizById("start_KK2_2"), q2);
  assert.strictEqual(getQuizById("kk2-2"), q2);

  assert.strictEqual(getQuizById("kk2_3"), q3);
  assert.strictEqual(getQuizById("KK2_3"), q3);
  assert.strictEqual(getQuizById("quiz_KK2_3"), q3);
  assert.strictEqual(getQuizById("start_KK2_3"), q3);
  assert.strictEqual(getQuizById("kk2-3"), q3);
  console.log("✅ Test 2 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 3: prepareSessionQuiz — Savollar va variantlar aralashuvi hamda
  // to'g'ri javob indeksining 100% aniq qayta hisoblanishi
  // -------------------------------------------------------------
  console.log("\nTest 3: Aralashtirish algoritmi va correctOptionId qayta hisoblash aniqligi...");
  for (let iter = 1; iter <= 50; iter++) {
    const sessionQuiz = prepareSessionQuiz(q1);

    assert.strictEqual(sessionQuiz.questions.length, 20);

    for (const sq of sessionQuiz.questions) {
      const orig = q1.questions.find((x) => x.id === sq.id)!;
      assert.ok(orig, `Original savol topilishi kerak: ${sq.id}`);

      const origCorrectText = orig.options[orig.correctOptionId];
      const sessionCorrectText = sq.options[sq.correctOptionId];

      assert.strictEqual(
        sessionCorrectText,
        origCorrectText,
        `Iteratsiya ${iter}: ${sq.id} savolida to'g'ri javob teksti mos kelmadi! Kutilgan: "${origCorrectText}", olingan: "${sessionCorrectText}"`
      );
    }
  }

  // Asl q1 obyekti mutatsiya bo'lmagani tekshiruvi
  assert.strictEqual(q1.questions[0].id, "kk2_1_1");
  assert.strictEqual(q1.questions[0].correctOptionId, 1);
  console.log("✅ Test 3 muvaffaqiyatli o'tdi (50 marta mustaqil aralashtirishda to'g'ri javob indeksi 100% mos keldi).");

  // -------------------------------------------------------------
  // Test 4: Shaxsiy chatda KK2 boshlanmasligi va guruhga qo'shish tugmasi chiqishi
  // -------------------------------------------------------------
  console.log("\nTest 4: Shaxsiy chatda KK2 quizi boshlanmasligi...");
  api.clear();
  const privateCtx = createMockContext({
    chatId: 12345,
    chatType: "private",
    userId: 12345,
    api,
  });

  await startQuizById(privateCtx as any, "KK2_1");
  assert.strictEqual(api.sentPolls.length, 0, "Shaxsiy chatda poll yuborilmasligi kerak");
  assert.strictEqual(api.sentMessages.length, 1, "Tushuntirish xabari yuborilishi kerak");
  assert.ok(api.sentMessages[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"));
  assert.ok(
    api.sentMessages[0].other?.reply_markup?.inline_keyboard[0][0]?.url?.includes("startgroup=quiz_KK2_1"),
    "Guruhga qo'shish tugmasi bo'lishi kerak"
  );
  console.log("✅ Test 4 muvaffaqiyatli o'tdi (Shaxsiy chatda rad etildi va havola berildi).");

  // -------------------------------------------------------------
  // Test 5: /start quiz_KK2_2 havolasi shaxsiy chatda guruhga taklif qilishi
  // -------------------------------------------------------------
  console.log("\nTest 5: /start quiz_KK2_2 shaxsiy chatda...");
  api.clear();
  const startCtx = createMockContext({
    chatId: 54321,
    chatType: "private",
    userId: 54321,
    match: "quiz_KK2_2",
    api,
  });

  await handleStart(startCtx as any);
  assert.strictEqual(api.sentPolls.length, 0);
  assert.strictEqual(api.sentMessages.length, 1);
  assert.ok(api.sentMessages[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"));
  assert.ok(
    api.sentMessages[0].other?.reply_markup?.inline_keyboard[0][0]?.url?.includes("startgroup=quiz_KK2_2")
  );
  console.log("✅ Test 5 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 6: Guruhda /quiz_KK2_1 orqali quizning boshlanishi
  // -------------------------------------------------------------
  console.log("\nTest 6: Guruhda /quiz_KK2_1 orqali quiz boshlanishi...");
  api.clear();
  const groupChatId = -1002233;
  const groupCtx = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: 9988,
    match: "KK2_1",
    api,
  });

  const { quizManager } = await import("../src/quiz/quizManager.js");
  await handleQuizByIdCommand(groupCtx as any);

  // E'lon xabari yuborilgan va quiz faol bo'lishi kerak
  assert.strictEqual(quizManager.isQuizRunning(groupChatId), true, "Guruhda quiz faol bo'lishi kerak");
  assert.ok(api.sentMessages.length >= 1, "E'lon xabari yuborilishi kerak");
  assert.ok(api.sentMessages[0].text.includes("KK2_1"));
  assert.ok(api.sentMessages[0].text.includes("20 soniya"));

  // 1-savolni yuboramiz
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
    match: "KK2_2",
    api,
  });

  await handleQuizByIdCommand(blockedCtx as any);
  assert.strictEqual(api.sentPolls.length, 0, "Yangi poll yuborilmasligi kerak");
  assert.strictEqual(api.sentMessages.length, 1, "Ogohlantirish xabari yuborilishi kerak");
  assert.ok(api.sentMessages[0].text.includes("allaqachon faol quiz davom etmoqda"));
  console.log("✅ Test 7 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 8: /stop buyrug'i faol KK2 quizini to'xtatishi
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
  console.log("\nTest 9: Javobsiz yakunlangan KK2 quizi...");
  api.clear();
  const emptyChatId = -1003355;
  const emptyCtx = createMockContext({
    chatId: emptyChatId,
    chatType: "supergroup",
    userId: 1111,
    match: "KK2_3",
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
  // Test 10: «🔄 Qayta yechish» callback orqali KK2_1 ni qayta boshlash
  // -------------------------------------------------------------
  console.log("\nTest 10: «🔄 Qayta yechish» callback query...");
  api.clear();
  const restartChatId = -1004466;
  const restartCtx = createMockContext({
    chatId: restartChatId,
    chatType: "supergroup",
    userId: 5544,
    callbackData: "restart_quiz_KK2_1",
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
  // Test 11: Aqlli pauza va davom ettirish (KK2)
  // -------------------------------------------------------------
  console.log("\nTest 11: KK2 sessiyasida aqlli pauza va resume...");
  api.clear();
  const pauseChatId = -1005577;
  const pauseCtx = createMockContext({
    chatId: pauseChatId,
    chatType: "supergroup",
    userId: 8877,
    match: "KK2_2",
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
  assert.ok(resumeButton && resumeButton.callback_data.startsWith(`resume_quiz_${pauseChatId}`), "Davom ettirish tugmasi bo'lishi kerak");

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

  console.log("\n🎉 BARCHA KK2 KOLLOID KIMYO TESTLARI (11/11) 100% MUVAFFAQIYATLI O'TDI!");
}

runKK2Tests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
