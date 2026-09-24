import assert from "node:assert";
import {
  getAllQuizzes,
  getQuizById,
  aminoAcidsQuiz,
  chemistryBasicsQuiz,
} from "../src/quiz/questions.js";
import { QuizManager, TelegramApiSender } from "../src/quiz/quizManager.js";
import {
  handleQuizCommand,
  handleQuizByIdCommand,
  handleStopQuizCommand,
  startQuizById,
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
  public subscribedUsers = new Set<number>([778899, 554433, 1111, 9999]);

  async getChatMember(_chatId: number | string, userId: number) {
    if (this.subscribedUsers.has(userId)) {
      return { status: "member", user: { id: userId } };
    }
    return { status: "left", user: { id: userId } };
  }

  async sendPoll(
    chatId: number | string,
    question: string,
    options: string[],
    other?: Record<string, any>
  ) {
    const messageId = this.nextMessageId++;
    const pollId = `poll_${this.nextPollId++}`;
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
  api: MockTelegramApi;
}) {
  const replies: Array<{ text: string; other?: any }> = [];
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
    api: options.api,
    replies,
    reply: async (text: string, other?: any) => {
      replies.push({ text, other });
      return { message_id: 999, text };
    },
    getChatMember: async (userId: number) => {
      if (options.isAdmin) {
        return { status: "administrator", user: { id: userId } };
      }
      return { status: "member", user: { id: userId } };
    },
  };
}

async function runMultiQuizTests() {
  console.log("🧪 KO'P QUIZLI TIZIM VA TALABLAR BO'YICHA TESTLAR BOSHLANDI...\n");

  const api = new MockTelegramApi();

  // ========================================================
  // TEST 1: Quizlar ro'yxati va o'zgarmas ID lar tekshiruvi
  // ========================================================
  console.log("Test 1: Quizlar registratsiyasi va o'zgarmas ID lar tekshiruvi...");
  const quizzes = getAllQuizzes();
  assert.ok(quizzes.length >= 2, "Kamida 2 ta quiz ro'yxatda bo'lishi kerak");

  // 1-quiz: Aminokislotalar
  const q1 = getQuizById("amino_acids");
  assert.ok(q1 !== undefined, "amino_acids ID li quiz mavjud bo'lishi kerak");
  assert.strictEqual(q1.id, "amino_acids", "1-quiz IDsi 'amino_acids' bo'lishi kerak");
  assert.strictEqual(q1.questions.length, 21, "1-quiz 21 ta savoldan iborat bo'lishi kerak");
  assert.strictEqual(q1.title, "Aminokislotalar — suyuqlanish temperaturasi");

  // Sinonimlar orqali topish
  assert.strictEqual(getQuizById("amino_acids_temp"), q1);
  assert.strictEqual(getQuizById("jda-chem-amino-acids"), q1);
  assert.strictEqual(getQuizById("1"), q1);

  // 2-quiz: Kimyo asoslari
  const q2 = getQuizById("kimyo_asoslari");
  assert.ok(q2 !== undefined, "kimyo_asoslari ID li quiz mavjud bo'lishi kerak");
  assert.strictEqual(q2.id, "kimyo_asoslari");
  assert.strictEqual(q2.questions.length, 5, "2-quiz 5 ta savoldan iborat bo'lishi kerak");

  // Noma'lum ID tekshiruvi
  assert.strictEqual(getQuizById("noma_lum_id_12345"), undefined);
  console.log("✅ Test 1 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 2: /quiz buyrug'i @jdaquizkod kanaliga yo'naltirishi
  // ========================================================
  console.log("Test 2: /quiz buyrug'i @jdaquizkod kanaliga yo'naltiruvchi xabar va tugmani ko'rsatishi...");
  const ctxQuizList = createMockContext({
    chatId: -1001,
    chatType: "supergroup",
    userId: 101,
    api,
  });
  await handleQuizCommand(ctxQuizList as any);
  assert.strictEqual(ctxQuizList.replies.length, 1);
  const quizListText = ctxQuizList.replies[0].text;
  assert.ok(
    quizListText.includes("Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz"),
    "Kanal xabari bo'lishi kerak"
  );
  assert.ok(
    ctxQuizList.replies[0].other?.reply_markup?.inline_keyboard?.[0]?.[0]?.url ===
      "https://t.me/jdaquizkod",
    "Kanalga havola tugmasi bo'lishi kerak"
  );
  console.log("✅ Test 2 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 3: Noma'lum ID kiritilganda tushunarli xabar berish
  // ========================================================
  console.log("Test 3: Noma'lum quiz ID si uchun xatolik xabari...");
  const ctxUnknown = createMockContext({
    chatId: -1002,
    chatType: "supergroup",
    userId: 102,
    isAdmin: true,
    api,
  });
  await startQuizById(ctxUnknown as any, "not_existing_quiz_id");
  assert.strictEqual(ctxUnknown.replies.length, 1);
  assert.ok(
    ctxUnknown.replies[0].text.includes("Bunday IDga ega quiz topilmadi"),
    "Noma'lum ID uchun xabar bo'lishi kerak"
  );
  assert.ok(ctxUnknown.replies[0].text.includes("/quiz"));
  console.log("✅ Test 3 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 4: Guruhda quizni faqat admin boshlashi mumkinligi
  // ========================================================
  console.log("Test 4: Guruhda faqat admin boshlay olishi (oddiy a'zo rad etilishi)...");
  const ctxGroupNonAdmin = createMockContext({
    chatId: -1003,
    chatType: "group",
    userId: 103,
    isAdmin: false,
    api,
  });
  await startQuizById(ctxGroupNonAdmin as any, "amino_acids");
  assert.strictEqual(ctxGroupNonAdmin.replies.length, 1);
  assert.ok(
    ctxGroupNonAdmin.replies[0].text.includes("faqat ushbu guruh adminlari") ||
    ctxGroupNonAdmin.replies[0].text.includes("faqat guruh adminlari boshlashi mumkin")
  );
  console.log("✅ Test 4 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 5: Shaxsiy chatda barcha quizlar boshlanishi bloklanishi (guruhga yo'naltirish)
  // ========================================================
  console.log("Test 5: Shaxsiy chatda quiz boshlash bloklanishi va guruhga yo'naltirish...");
  const privateChatId = 778899;
  const ctxPrivate = createMockContext({
    chatId: privateChatId,
    chatType: "private",
    userId: 778899,
    isAdmin: false,
    api,
  });

  // kimyo_asoslari shaxsiy chatda
  await startQuizById(ctxPrivate as any, "kimyo_asoslari");
  assert.strictEqual(ctxPrivate.replies.length, 1);
  assert.ok(
    ctxPrivate.replies[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"),
    "Shaxsiy chatda guruhga yo'naltirish xabari chiqishi kerak"
  );
  assert.ok(
    ctxPrivate.replies[0].other?.reply_markup?.inline_keyboard?.[0]?.[0]?.url.includes(
      "startgroup=quiz_kimyo_asoslari"
    ),
    "startgroup havolasi bo'lishi kerak"
  );

  // amino_acids shaxsiy chatda
  const ctxPrivate2 = createMockContext({
    chatId: privateChatId,
    chatType: "private",
    userId: 778899,
    api,
  });
  await startQuizById(ctxPrivate2 as any, "amino_acids");
  assert.strictEqual(ctxPrivate2.replies.length, 1);
  assert.ok(
    ctxPrivate2.replies[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"),
    "amino_acids ham shaxsiy chatda bloklanishi kerak"
  );
  assert.ok(
    ctxPrivate2.replies[0].other?.reply_markup?.inline_keyboard?.[0]?.[0]?.url.includes(
      "startgroup=quiz_amino_acids"
    )
  );

  // Shaxsiy chatda hech qanday poll yuborilmagan bo'lishi kerak
  const privatePoll = api.sentPolls.find((p) => p.chatId === privateChatId);
  assert.strictEqual(privatePoll, undefined, "Shaxsiy chatda poll yuborilmasligi kerak");
  console.log("✅ Test 5 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 6: Bitta guruhda faol quiz turganda ikkinchisini boshlashni bloklash
  // ========================================================
  console.log("Test 6: Bitta guruhda faol quiz turganda ikkinchisi boshlanmasligi...");
  const testGroupChatId = -1004455;
  const ctxGroupAdmin1 = createMockContext({
    chatId: testGroupChatId,
    chatType: "supergroup",
    userId: 8881,
    isAdmin: true,
    api,
  });
  await startQuizById(ctxGroupAdmin1 as any, "kimyo_asoslari");
  const groupStartMsg = api.sentMessages.find(
    (m) => m.chatId === testGroupChatId && m.text.includes("Kimyo asoslari — namuna")
  );
  assert.ok(groupStartMsg !== undefined, "Guruhda admin quizni boshlay olishi kerak");

  // Shu guruhda yana boshqa quiz boshlashga urinish
  const ctxGroupDuplicate = createMockContext({
    chatId: testGroupChatId,
    chatType: "supergroup",
    userId: 8881,
    isAdmin: true,
    api,
  });
  await startQuizById(ctxGroupDuplicate as any, "amino_acids");
  assert.strictEqual(ctxGroupDuplicate.replies.length, 1);
  assert.ok(
    ctxGroupDuplicate.replies[0].text.includes("allaqachon faol quiz davom etmoqda"),
    "Guruhda takroriy boshlash bloklanishi kerak"
  );
  console.log("✅ Test 6 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 7: /stop va /stopquiz:
  // - guruhda faqat admin to'xtatishi (oddiy a'zo rad etilishi)
  // - taymer to'xtashi, yakuniy natija yuborilmasligi
  // ========================================================
  console.log("Test 7: /stop faqat admin tomonidan to'xtatilishi va yakuniy natija yuborilmasligi...");
  // Oddiy a'zo to'xtatishga uringanda
  const ctxStopNonAdmin = createMockContext({
    chatId: testGroupChatId,
    chatType: "supergroup",
    userId: 9992,
    isAdmin: false,
    api,
  });
  await handleStopQuizCommand(ctxStopNonAdmin as any);
  assert.strictEqual(ctxStopNonAdmin.replies.length, 1);
  assert.ok(
    ctxStopNonAdmin.replies[0].text.includes("faqat guruh adminlariga berilgan"),
    "Oddiy a'zo /stop qila olmasligi kerak"
  );

  // Admin to'xtatganda
  const ctxStopAdmin = createMockContext({
    chatId: testGroupChatId,
    chatType: "supergroup",
    userId: 8881,
    isAdmin: true,
    api,
  });
  await handleStopQuizCommand(ctxStopAdmin as any);
  const stopMsg = api.sentMessages.find(
    (m) => m.chatId === testGroupChatId && m.text.includes("Quiz to'xtatildi")
  );
  assert.ok(stopMsg !== undefined, "Quiz to'xtatildi xabari yuborilishi kerak");

  // Yakuniy reyting natijasi yuborilmaganligini tekshiramiz!
  const hasFinishedMsg = api.sentMessages.some(
    (m) => m.chatId === testGroupChatId && m.text.includes("Yakuniy Natijalar va Reyting")
  );
  assert.strictEqual(hasFinishedMsg, false, "To'xtatilganda yakuniy natija YUBORILMASLIGI shart");

  // Qaytadan /stop bosilganda faol quiz yo'qligi xabari
  await handleStopQuizCommand(ctxStopAdmin as any);
  assert.strictEqual(ctxStopAdmin.replies.length, 1);
  assert.ok(ctxStopAdmin.replies[0].text.includes("faol quiz mavjud emas"));
  console.log("✅ Test 7 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 8: Shaxsiy havola orqali ochish (?start=quiz_<ID>)
  // ========================================================
  console.log("Test 8: Havola orqali deep linking (?start=quiz_<ID>)...");
  const deepLinkChatId = 554433;
  // Shaxsiy chatda deep link ochilganda guruhga yo'naltirish
  const ctxDeepLinkPrivate = createMockContext({
    chatId: deepLinkChatId,
    chatType: "private",
    userId: 554433,
    match: "quiz_amino_acids",
    api,
  });
  await handleStart(ctxDeepLinkPrivate as any);
  assert.strictEqual(ctxDeepLinkPrivate.replies.length, 1);
  assert.ok(
    ctxDeepLinkPrivate.replies[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"),
    "Shaxsiy deep link guruhga yo'naltirishi kerak"
  );

  // Guruhda admin deep link orqali ochganda quiz boshlanishi
  const deepGroupChatId = -1006677;
  const ctxDeepLinkGroup = createMockContext({
    chatId: deepGroupChatId,
    chatType: "supergroup",
    userId: 7771,
    isAdmin: true,
    match: "quiz_amino_acids",
    api,
  });
  await handleStart(ctxDeepLinkGroup as any);
  const deepLinkStartMsg = api.sentMessages.find(
    (m) => m.chatId === deepGroupChatId && m.text.includes("Aminokislotalar — suyuqlanish temperaturasi")
  );
  assert.ok(deepLinkStartMsg !== undefined, "Guruhda deep link orqali quiz boshlanishi kerak");

  // Guruhdagi quizni to'xtatamiz
  const ctxDeepLinkStop = createMockContext({
    chatId: deepGroupChatId,
    chatType: "supergroup",
    userId: 7771,
    isAdmin: true,
    api,
  });
  await handleStopQuizCommand(ctxDeepLinkStop as any);
  console.log("✅ Test 8 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 9: Bir vaqtning o'zida ikkita guruhda mustaqil quizlar ishlashi
  // ========================================================
  console.log("Test 9: Bir vaqtning o'zida ikki guruhda mustaqil quizlar ishlashi...");
  const group1 = -1001111;
  const group2 = -1002222;

  const ctxChat1 = createMockContext({
    chatId: group1,
    chatType: "supergroup",
    userId: 1111,
    isAdmin: true,
    api,
  });
  const ctxChat2 = createMockContext({
    chatId: group2,
    chatType: "supergroup",
    userId: 2222,
    isAdmin: true,
    api,
  });

  await startQuizById(ctxChat1 as any, "kimyo_asoslari");
  await startQuizById(ctxChat2 as any, "amino_acids");

  const chat1Msg = api.sentMessages.find((m) => m.chatId === group1 && m.text.includes("Kimyo asoslari"));
  const chat2Msg = api.sentMessages.find((m) => m.chatId === group2 && m.text.includes("Aminokislotalar"));

  assert.ok(chat1Msg !== undefined, "Guruh 1 da 5 savolli quiz boshlanishi kerak");
  assert.ok(chat2Msg !== undefined, "Guruh 2 da 21 savolli quiz boshlanishi kerak");

  // Ikkala guruhni alohida to'xtatish
  await handleStopQuizCommand(ctxChat1 as any);
  await handleStopQuizCommand(ctxChat2 as any);
  console.log("✅ Test 9 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 10: /quiz_<ID> buyrug'i orqali boshlash
  // ========================================================
  console.log("Test 10: /quiz_<ID> buyrug'i (shaxsiyda rad etish, guruhda admin orqali boshlash)...");
  // Shaxsiy chatda rad etilishi
  const ctxRegexPrivate = createMockContext({
    chatId: 9999,
    chatType: "private",
    userId: 9999,
    match: ["/quiz_kimyo_asoslari", "kimyo_asoslari"],
    api,
  });
  await handleQuizByIdCommand(ctxRegexPrivate as any);
  assert.strictEqual(ctxRegexPrivate.replies.length, 1);
  assert.ok(
    ctxRegexPrivate.replies[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"),
    "Shaxsiy chatda /quiz_<ID> rad etilishi kerak"
  );

  // Guruhda admin yuborganda boshlanishi
  const regexGroupChatId = -1009988;
  const ctxRegexGroup = createMockContext({
    chatId: regexGroupChatId,
    chatType: "supergroup",
    userId: 9999,
    isAdmin: true,
    match: ["/quiz_kimyo_asoslari", "kimyo_asoslari"],
    api,
  });
  await handleQuizByIdCommand(ctxRegexGroup as any);
  const regexMsg = api.sentMessages.find((m) => m.chatId === regexGroupChatId && m.text.includes("Kimyo asoslari"));
  assert.ok(regexMsg !== undefined, "Guruhda admin yuborgan /quiz_<ID> buyrug'i quizni boshlashi kerak");
  await handleStopQuizCommand(ctxRegexGroup as any);
  console.log("✅ Test 10 muvaffaqiyatli o'tdi.\n");

  console.log("🎉 BARCHA KO'P QUIZLI TIZIM TESTLARI (10/10) MUVAFFAQIYATLI O'TDI!");
}

runMultiQuizTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
