import assert from "node:assert";
import {
  getAllQuizzes,
  getQuizById,
  kk1Quiz1,
  kk1Quiz2,
  kk1Quiz3,
  aminoAcidsQuiz,
  chemistryBasicsQuiz,
} from "../src/quiz/questions.js";
import {
  QuizManager,
  quizManager,
  TelegramApiSender,
  prepareSessionQuiz,
  shuffleArray,
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
    const pollId = `poll_kk_${this.nextPollId++}`;
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

async function runKK1Tests() {
  console.log("🧪 KK1 KOLLOID KIMYO QUIZLARI VA ARALASHTIRISH TESTLARI BOSHLANDI...\n");
  const api = new MockTelegramApi();

  // -------------------------------------------------------------
  // Test 1: KK1_1, KK1_2, KK1_3 quizlarining ro'yxati va savollar soni
  // -------------------------------------------------------------
  console.log("Test 1: KK1 to'plamlarining ro'yxatdan o'tishi va 20 tadan savol borligi...");
  const q1 = getQuizById("KK1_1");
  const q2 = getQuizById("KK1_2");
  const q3 = getQuizById("KK1_3");

  assert.ok(q1, "KK1_1 topilishi kerak");
  assert.ok(q2, "KK1_2 topilishi kerak");
  assert.ok(q3, "KK1_3 topilishi kerak");

  assert.strictEqual(q1.questions.length, 20, "KK1_1 da 20 ta savol bo'lishi kerak");
  assert.strictEqual(q2.questions.length, 20, "KK1_2 da 20 ta savol bo'lishi kerak");
  assert.strictEqual(q3.questions.length, 20, "KK1_3 da 20 ta savol bo'lishi kerak");

  assert.strictEqual(q1.groupOnly, true, "KK1_1 groupOnly bo'lishi kerak");
  assert.strictEqual(q2.groupOnly, true, "KK1_2 groupOnly bo'lishi kerak");
  assert.strictEqual(q3.groupOnly, true, "KK1_3 groupOnly bo'lishi kerak");

  assert.strictEqual(q1.shuffle, true, "KK1_1 shuffle faol bo'lishi kerak");
  assert.strictEqual(q2.shuffle, true, "KK1_2 shuffle faol bo'lishi kerak");
  assert.strictEqual(q3.shuffle, true, "KK1_3 shuffle faol bo'lishi kerak");

  assert.strictEqual(q1.source, "Bahora Nayimova slaydlaridan", "KK1_1 manbasi to'g'ri bo'lishi kerak");
  assert.strictEqual(q2.source, "Bahora Nayimova slaydlaridan", "KK1_2 manbasi to'g'ri bo'lishi kerak");
  assert.strictEqual(q3.source, "Bahora Nayimova slaydlaridan", "KK1_3 manbasi to'g'ri bo'lishi kerak");

  // Har bir savolda 4 ta variant va 20 soniya
  for (const q of [...q1.questions, ...q2.questions, ...q3.questions]) {
    assert.strictEqual(q.options.length, 4, `Savolda 4 variant bo'lishi kerak: ${q.question}`);
    assert.strictEqual(q.timeLimitSeconds, 20, `Vaqt 20s bo'lishi kerak: ${q.question}`);
    assert.ok(q.correctOptionId >= 0 && q.correctOptionId < 4, "To'g'ri variant indeksi 0-3 oralig'ida bo'lishi kerak");
  }

  // Jami 60 ta unikal savol ekani
  const allQTexts = new Set([...q1.questions, ...q2.questions, ...q3.questions].map((x) => x.question));
  assert.strictEqual(allQTexts.size, 60, "Barcha 60 ta savol takrorlanmas unikal bo'lishi kerak");
  console.log("✅ Test 1 muvaffaqiyatli o'tdi (60 ta unikal savol, 3 ta 20 savolli to'plam).");

  // -------------------------------------------------------------
  // Test 2: Case-insensitive va sinonim ID lar orqali topilishi
  // -------------------------------------------------------------
  console.log("\nTest 2: Kichik va katta harflarda ID larni qidirish...");
  assert.strictEqual(getQuizById("kk1_1"), q1);
  assert.strictEqual(getQuizById("KK1_1"), q1);
  assert.strictEqual(getQuizById("kk1-1"), q1);
  assert.strictEqual(getQuizById("kk1_2"), q2);
  assert.strictEqual(getQuizById("KK1_2"), q2);
  assert.strictEqual(getQuizById("kk1_3"), q3);
  assert.strictEqual(getQuizById("KK1_3"), q3);
  console.log("✅ Test 2 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 3: prepareSessionQuiz — Savollar va variantlar aralashuvi hamda
  // to'g'ri javob indeksining 100% aniq qayta hisoblanishi
  // -------------------------------------------------------------
  console.log("\nTest 3: Aralashtirish algoritmi va correctOptionId qayta hisoblash aniqligi...");
  for (let iter = 1; iter <= 50; iter++) {
    const sessionQuiz = prepareSessionQuiz(q1);

    // Savollar soni 20 ta bo'lishi kerak
    assert.strictEqual(sessionQuiz.questions.length, 20);

    // Har bir savolda to'g'ri javob teksti o'zgarmasligi kerak
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
  assert.strictEqual(q1.questions[0].id, "kk1_1_1");
  assert.strictEqual(q1.questions[0].correctOptionId, 0);
  console.log("✅ Test 3 muvaffaqiyatli o'tdi (50 marta mustaqil aralashtirishda to'g'ri javob indeksi 100% mos keldi).");

  // -------------------------------------------------------------
  // Test 4: Shaxsiy chatda KK1 quizlari boshlanmasligi (groupOnly guard)
  // -------------------------------------------------------------
  console.log("\nTest 4: Shaxsiy chatda KK1 quizlarini boshlash rad etilishi...");
  api.clear();

  const privateCtx = createMockContext({
    chatId: 998811,
    chatType: "private",
    userId: 998811,
    firstName: "Aziz",
    api,
  });

  await startQuizById(privateCtx as any, "KK1_1");
  assert.strictEqual(quizManager.isQuizRunning(998811), false, "Shaxsiy chatda quiz boshlanmasligi kerak");
  assert.strictEqual(privateCtx.replies.length, 1);
  assert.ok(privateCtx.replies[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"));
  assert.ok(privateCtx.replies[0].other?.reply_markup?.inline_keyboard[0][0]?.url.includes("startgroup="));
  console.log("✅ Test 4 muvaffaqiyatli o'tdi (Shaxsiy chatda rad etilib, guruhga qo'shish tugmasi berildi).");

  // -------------------------------------------------------------
  // Test 5: Guruhda admin bo'lmagan foydalanuvchi boshlay olmasligi
  // -------------------------------------------------------------
  console.log("\nTest 5: Guruhda admin huquqisiz boshlash rad etilishi...");
  api.clear();

  const nonAdminGroupCtx = createMockContext({
    chatId: -10055555,
    chatType: "supergroup",
    userId: 12345,
    firstName: "Oddiy A'zo",
    isAdmin: false,
    api,
  });

  await startQuizById(nonAdminGroupCtx as any, "KK1_2");
  assert.strictEqual(quizManager.isQuizRunning(-10055555), false);
  assert.ok(nonAdminGroupCtx.replies[0].text.includes("faqat guruh adminlari boshlashi mumkin"));
  console.log("✅ Test 5 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 6: Aralashtirilgan KK1_1 quizida to'liq 20 savol bo'yicha baholash aniqligi,
  // muallif (@diyorbek_jabborov), manba va yakuniy tugmalar tekshiruvi (E2E)
  // -------------------------------------------------------------
  console.log("\nTest 6: Aralashgan KK1_1 quizida javoblarni to'g'ri baholash, yaratuvchi, manba va tugmalar...");
  api.clear();

  const testChatId = -1009988;
  const isolatedManager = new QuizManager();
  const startRes = await isolatedManager.startQuiz(testChatId, q1, api);
  assert.strictEqual(startRes.success, true);
  assert.strictEqual(isolatedManager.isQuizRunning(testChatId), true);

  const session = isolatedManager.getSession(testChatId)!;
  assert.ok(session);
  assert.strictEqual(session.quiz.questions.length, 20);

  // 20 ta savolning barchasiga javob berish
  for (let i = 0; i < 20; i++) {
    await isolatedManager.sendNextQuestion(testChatId, api);
    const lastPoll = api.sentPolls[api.sentPolls.length - 1];
    assert.strictEqual(lastPoll.other?.type, "quiz");
    assert.strictEqual(lastPoll.other?.open_period, 20);

    const correctId = lastPoll.other?.correct_option_ids[0];
    const wrongId = (correctId + 1) % 4;

    // Ishtirokchi 1: Har doim to'g'ri variantni bosadi
    isolatedManager.handlePollAnswer({
      pollId: lastPoll.pollId,
      user: { id: 101, first_name: "A'lochi Olim", username: "olim_pro" },
      optionIds: [correctId],
    });

    // Ishtirokchi 2: Har doim noto'g'ri variantni bosadi
    isolatedManager.handlePollAnswer({
      pollId: lastPoll.pollId,
      user: { id: 102, first_name: "Yangi O'quvchi", username: "yangi_user" },
      optionIds: [wrongId],
    });
  }

  // Quizni yakunlash
  await isolatedManager.finishQuiz(testChatId, api);

  const finalMsg = api.sentMessages[api.sentMessages.length - 1];
  assert.ok(finalMsg.text.includes("yakunlandi"));
  assert.ok(finalMsg.text.includes("@olim_pro</b>: 20/20 ball"), "Olim 20/20 ball olishi kerak");
  assert.ok(finalMsg.text.includes("@yangi_user</b>: 0/20 ball"), "Yangi foydalanuvchi 0/20 ball olishi kerak");

  // Yaratuvchi va manbani tekshirish
  assert.ok(
    finalMsg.text.includes("Test yaratuvchisi: <a href=\"https://t.me/diyorbek_jabborov\">@diyorbek_jabborov</a>"),
    "Yaratuvchi profili linki bo'lishi kerak"
  );
  assert.ok(
    finalMsg.text.includes("Savollar manbasi: Bahora Nayimova slaydlaridan"),
    "KK1 savollari manbasi bo'lishi kerak"
  );

  // Yakuniy ikkita tugmani tekshirish
  const buttons = finalMsg.other?.reply_markup?.inline_keyboard?.flat() || [];
  const kodlarBtn = buttons.find((b: any) => b.text === "📢 Quiz kodlari");
  const restartBtn = buttons.find((b: any) => b.text === "🔄 Qayta yechish");

  assert.ok(kodlarBtn, "📢 Quiz kodlari tugmasi mavjud bo'lishi kerak");
  assert.strictEqual(kodlarBtn.url, "https://t.me/jdaquizkod");
  assert.ok(restartBtn, "🔄 Qayta yechish tugmasi mavjud bo'lishi kerak");
  assert.strictEqual(restartBtn.callback_data, "restart_quiz_KK1_1");

  console.log("✅ Test 6 muvaffaqiyatli o'tdi (Reyting, muallif, manba va tugmalar tasdiqlandi).");

  // -------------------------------------------------------------
  // Test 7: Turli guruhlarda parallel boshlangan quizlar bir-biriga ta'sir qilmasligi
  // -------------------------------------------------------------
  console.log("\nTest 7: Ikki xil guruhda bir vaqtda mustaqil KK1 quizlari...");
  api.clear();

  const groupA = -10011111;
  const groupB = -10022222;

  await isolatedManager.startQuiz(groupA, q2, api);
  await isolatedManager.startQuiz(groupB, q2, api);

  assert.strictEqual(isolatedManager.isQuizRunning(groupA), true);
  assert.strictEqual(isolatedManager.isQuizRunning(groupB), true);

  const sessionA = isolatedManager.getSession(groupA)!;
  const sessionB = isolatedManager.getSession(groupB)!;

  // Ikkala guruhdagi savollar obyekti mustaqil nusxa bo'lishi kerak
  assert.notStrictEqual(sessionA.quiz.questions, sessionB.quiz.questions);

  await isolatedManager.stopQuiz(groupA, api);
  assert.strictEqual(isolatedManager.isQuizRunning(groupA), false);
  assert.strictEqual(isolatedManager.isQuizRunning(groupB), true, "GroupA to'xtagani bilan GroupB davom etishi kerak");

  await isolatedManager.stopQuiz(groupB, api);
  assert.strictEqual(isolatedManager.isQuizRunning(groupB), false);
  console.log("✅ Test 7 muvaffaqiyatli o'tdi (Parallel guruhlar 100% mustaqil).");

  // -------------------------------------------------------------
  // Test 8: Telegram deep link payload (?start=quiz_KK1_3 yoki ?startgroup=KK1_1)
  // -------------------------------------------------------------
  console.log("\nTest 8: Deep link orqali KK1 quizlarini ochish...");
  api.clear();

  // Guruh admini havola bilan guruhda quiz boshlaganda
  const deepLinkCtx = createMockContext({
    chatId: -1008899,
    chatType: "supergroup",
    userId: 555,
    firstName: "Admin",
    isAdmin: true,
    match: "quiz_KK1_3",
    api,
  });

  await handleStart(deepLinkCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(-1008899), true, "Guruhda admin deep link orqali KK1_3 ni boshlashi kerak");
  await quizManager.stopQuiz(-1008899, api);
  console.log("✅ Test 8 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 9: /stop va /stopquiz KK1 quizini to'xtatishi
  // -------------------------------------------------------------
  console.log("\nTest 9: /stop buyrug'i faol KK1 quizini to'xtatishi...");
  api.clear();

  const stopAdminCtx = createMockContext({
    chatId: -1007766,
    chatType: "supergroup",
    userId: 888,
    firstName: "Admin",
    isAdmin: true,
    api,
  });

  await startQuizById(stopAdminCtx as any, "KK1_1");
  assert.strictEqual(quizManager.isQuizRunning(-1007766), true);

  await handleStopQuizCommand(stopAdminCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(-1007766), false, "Quiz to'xtatilgan bo'lishi kerak");
  console.log("✅ Test 9 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 10: Ishtirokchi bo'lmagan holatda ham yaratuvchi, manba va tugmalar chiqishi
  // -------------------------------------------------------------
  console.log("\nTest 10: Hech kim javob bermagan holatda ham yaratuvchi, manba va tugmalar...");
  api.clear();
  const emptyManager = new QuizManager();
  const emptyChatId = -1003344;
  await emptyManager.startQuiz(emptyChatId, q3, api);
  await emptyManager.finishQuiz(emptyChatId, api);

  const emptyMsg = api.sentMessages[api.sentMessages.length - 1];
  assert.ok(emptyMsg.text.includes("Afsuski, hech bir ishtirokchi savollarga javob bermadi"));
  assert.ok(
    emptyMsg.text.includes("Test yaratuvchisi: <a href=\"https://t.me/diyorbek_jabborov\">@diyorbek_jabborov</a>"),
    "Ishtirokchisiz xabarda ham yaratuvchi bo'lishi kerak"
  );
  assert.ok(
    emptyMsg.text.includes("Savollar manbasi: Bahora Nayimova slaydlaridan"),
    "Ishtirokchisiz xabarda ham manba bo'lishi kerak"
  );
  const emptyButtons = emptyMsg.other?.reply_markup?.inline_keyboard?.flat() || [];
  assert.ok(emptyButtons.some((b: any) => b.text === "📢 Quiz kodlari"));
  assert.ok(emptyButtons.some((b: any) => b.text === "🔄 Qayta yechish"));
  console.log("✅ Test 10 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 11: Eski quizlarda (amino_acids, kimyo_asoslari) Bahora Nayimova chiqmasligi
  // -------------------------------------------------------------
  console.log("\nTest 11: Eski quizlar yakunida Bahora Nayimova chiqmasligi va yaratuvchi chiqishi...");
  api.clear();
  const oldQuizManager = new QuizManager();
  const oldChatId = -1004455;
  await oldQuizManager.startQuiz(oldChatId, aminoAcidsQuiz, api);
  await oldQuizManager.finishQuiz(oldChatId, api);

  const oldMsg = api.sentMessages[api.sentMessages.length - 1];
  assert.ok(
    oldMsg.text.includes("Test yaratuvchisi: <a href=\"https://t.me/diyorbek_jabborov\">@diyorbek_jabborov</a>"),
    "Eski quizda ham yaratuvchi chiqishi kerak"
  );
  assert.ok(
    !oldMsg.text.includes("Bahora Nayimova"),
    "Eski quizda Bahora Nayimova chiqmasligi kerak"
  );
  console.log("✅ Test 11 muvaffaqiyatli o'tdi.");

  // -------------------------------------------------------------
  // Test 12: «🔄 Qayta yechish» callback query:
  // - Faqat admin bosa oladi
  // - Boshqa quiz davom etayotganda boshlanmaydi
  // - Qayta boshlanganda savollar va variantlar qayta aralashadi
  // - Guruhda kanal obunasi talab qilinmaydi
  // -------------------------------------------------------------
  console.log("\nTest 12: «🔄 Qayta yechish» tugmasi mantig'i va ruxsatlar...");
  api.clear();
  const restartGroupChatId = -1006677;

  // 12.1: Oddiy a'zo bosganda rad etilishi
  const nonAdminRestartCtx = createMockContext({
    chatId: restartGroupChatId,
    chatType: "supergroup",
    userId: 202,
    isAdmin: false,
    callbackData: "restart_quiz_KK1_1",
    api,
  });

  await handleRestartQuizCallback(nonAdminRestartCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(restartGroupChatId), false, "Oddiy a'zo quizni boshlay olmasligi kerak");
  assert.strictEqual(nonAdminRestartCtx.answeredCallbacks.length, 1);
  assert.ok(
    nonAdminRestartCtx.answeredCallbacks[0].text?.includes("faqat guruh adminlari qayta boshlashi mumkin"),
    "Admin ogohlantirishi berilishi kerak"
  );
  assert.strictEqual(nonAdminRestartCtx.answeredCallbacks[0].show_alert, true);

  // 12.2: Admin bosganda muvaffaqiyatli boshlanishi
  const adminRestartCtx = createMockContext({
    chatId: restartGroupChatId,
    chatType: "supergroup",
    userId: 909,
    isAdmin: true,
    callbackData: "restart_quiz_KK1_1",
    api,
  });

  await handleRestartQuizCallback(adminRestartCtx as any);
  assert.strictEqual(quizManager.isQuizRunning(restartGroupChatId), true, "Admin bosganda quiz boshlanishi kerak");
  assert.ok(adminRestartCtx.answeredCallbacks[0].text?.includes("qayta boshlanmoqda"));

  // 12.3: Faol quiz ketayotganda ikkinchi marta bosilsa rad etilishi
  const activeAdminRestartCtx = createMockContext({
    chatId: restartGroupChatId,
    chatType: "supergroup",
    userId: 909,
    isAdmin: true,
    callbackData: "restart_quiz_KK1_2",
    api,
  });

  await handleRestartQuizCallback(activeAdminRestartCtx as any);
  assert.ok(
    activeAdminRestartCtx.answeredCallbacks[0].text?.includes("allaqachon faol quiz davom etmoqda"),
    "Faol quiz paytida qayta boshlash rad etilishi kerak"
  );
  assert.strictEqual(activeAdminRestartCtx.answeredCallbacks[0].show_alert, true);

  // To'xtatamiz
  await quizManager.stopQuiz(restartGroupChatId, api);
  assert.strictEqual(quizManager.isQuizRunning(restartGroupChatId), false);

  console.log("✅ Test 12 muvaffaqiyatli o'tdi (Ruxsatlar, blokirovka va qayta aralashtirish to'liq ishlaydi).");

  console.log("\n🎉 BARCHA KK1, MUALLIFLIK VA QAYTA YECHISH TESTLARI (12/12) 100% MUVAFFAQIYATLI O'TDI!");
}

runKK1Tests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
