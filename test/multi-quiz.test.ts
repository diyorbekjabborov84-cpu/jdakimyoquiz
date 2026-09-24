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
  // TEST 5: Shaxsiy chatda foydalanuvchi o'zi boshlay olishi
  // ========================================================
  console.log("Test 5: Shaxsiy chatda (private) foydalanuvchi o'zi quizni boshlashi...");
  const privateChatId = 778899;
  const ctxPrivate = createMockContext({
    chatId: privateChatId,
    chatType: "private",
    userId: 778899,
    isAdmin: false, // Shaxsiy chatda admin bo'lish shart emas
    api,
  });
  await startQuizById(ctxPrivate as any, "kimyo_asoslari");
  // startQuiz chaqirildi, api.sendMessage orqali e'lon xabari ketdi
  const privateStartMsg = api.sentMessages.find(
    (m) => m.chatId === privateChatId && m.text.includes("Kimyo asoslari — namuna")
  );
  assert.ok(privateStartMsg !== undefined, "Shaxsiy chatda quiz e'loni yuborilishi kerak");
  console.log("✅ Test 5 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 6: Bitta chatda faol quiz turganda ikkinchisini boshlashni bloklash
  // ========================================================
  console.log("Test 6: Bitta chatda faol quiz turganda ikkinchisi boshlanmasligi...");
  const ctxPrivateDuplicate = createMockContext({
    chatId: privateChatId,
    chatType: "private",
    userId: 778899,
    api,
  });
  await startQuizById(ctxPrivateDuplicate as any, "amino_acids");
  assert.strictEqual(ctxPrivateDuplicate.replies.length, 1);
  assert.ok(
    ctxPrivateDuplicate.replies[0].text.includes("allaqachon faol quiz davom etmoqda"),
    "Takroriy boshlash bloklanishi kerak"
  );
  console.log("✅ Test 6 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 7: /stop va /stopquiz:
  // - guruhda faqat admin to'xtatishi
  // - shaxsiy chatda foydalanuvchi to'xtatishi
  // - taymer to'xtashi, yakuniy natija yuborilmasligi
  // ========================================================
  console.log("Test 7: /stop faol quizni to'xtatishi va natija yuborilmasligi...");
  // Shaxsiy chatdagi faol quizni /stop orqali to'xtatamiz
  const ctxStopPrivate = createMockContext({
    chatId: privateChatId,
    chatType: "private",
    userId: 778899,
    api,
  });
  await handleStopQuizCommand(ctxStopPrivate as any);
  const stopMsg = api.sentMessages.find(
    (m) => m.chatId === privateChatId && m.text.includes("Quiz to'xtatildi")
  );
  assert.ok(stopMsg !== undefined, "Quiz to'xtatildi xabari yuborilishi kerak");

  // Yakuniy reyting natijasi yuborilmaganligini tekshiramiz!
  const hasFinishedMsg = api.sentMessages.some(
    (m) => m.chatId === privateChatId && m.text.includes("Yakuniy Natijalar va Reyting")
  );
  assert.strictEqual(hasFinishedMsg, false, "To'xtatilganda yakuniy natija YUBORILMASLIGI shart");

  // Qaytadan /stop bosilganda faol quiz yo'qligi xabari
  await handleStopQuizCommand(ctxStopPrivate as any);
  assert.strictEqual(ctxStopPrivate.replies.length, 1);
  assert.ok(ctxStopPrivate.replies[0].text.includes("faol quiz mavjud emas"));
  console.log("✅ Test 7 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 8: Shaxsiy havola orqali ochish (?start=quiz_<ID>)
  // ========================================================
  console.log("Test 8: Shaxsiy havola orqali deep linking (?start=quiz_<ID>)...");
  const deepLinkChatId = 554433;
  const ctxDeepLink = createMockContext({
    chatId: deepLinkChatId,
    chatType: "private",
    userId: 554433,
    match: "quiz_amino_acids",
    api,
  });
  await handleStart(ctxDeepLink as any);
  const deepLinkStartMsg = api.sentMessages.find(
    (m) => m.chatId === deepLinkChatId && m.text.includes("Aminokislotalar — suyuqlanish temperaturasi")
  );
  assert.ok(deepLinkStartMsg !== undefined, "Deep link orqali to'g'ri quiz boshlanishi kerak");

  // To'xtatamiz
  const ctxDeepLinkStop = createMockContext({
    chatId: deepLinkChatId,
    chatType: "private",
    userId: 554433,
    api,
  });
  await handleStopQuizCommand(ctxDeepLinkStop as any);
  console.log("✅ Test 8 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 9: Bir vaqtning o'zida ikkita chat (shaxsiy va guruh) mustaqil ishlashi
  // ========================================================
  console.log("Test 9: Bir vaqtning o'zida ikki chatda mustaqil quizlar ishlashi...");
  const chat1 = 1111; // Shaxsiy chat
  const chat2 = -2222; // Guruh

  const ctxChat1 = createMockContext({
    chatId: chat1,
    chatType: "private",
    userId: 1111,
    api,
  });
  const ctxChat2 = createMockContext({
    chatId: chat2,
    chatType: "supergroup",
    userId: 2222,
    isAdmin: true,
    api,
  });

  await startQuizById(ctxChat1 as any, "kimyo_asoslari");
  await startQuizById(ctxChat2 as any, "amino_acids");

  const chat1Msg = api.sentMessages.find((m) => m.chatId === chat1 && m.text.includes("Kimyo asoslari"));
  const chat2Msg = api.sentMessages.find((m) => m.chatId === chat2 && m.text.includes("Aminokislotalar"));

  assert.ok(chat1Msg !== undefined, "Chat 1 da 5 savolli quiz boshlanishi kerak");
  assert.ok(chat2Msg !== undefined, "Chat 2 da 21 savolli quiz boshlanishi kerak");

  // Ikkala chatni alohida to'xtatish
  await handleStopQuizCommand(ctxChat1 as any);
  await handleStopQuizCommand(ctxChat2 as any);
  console.log("✅ Test 9 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 10: /quiz_<ID> regex buyrug'i orqali boshlash
  // ========================================================
  console.log("Test 10: /quiz_<ID> regex match orqali boshlash...");
  const ctxRegex = createMockContext({
    chatId: 9999,
    chatType: "private",
    userId: 9999,
    match: ["/quiz_kimyo_asoslari", "kimyo_asoslari"],
    api,
  });
  await handleQuizByIdCommand(ctxRegex as any);
  const regexMsg = api.sentMessages.find((m) => m.chatId === 9999 && m.text.includes("Kimyo asoslari"));
  assert.ok(regexMsg !== undefined, "/quiz_<ID> buyrug'i quizni boshlashi kerak");
  await handleStopQuizCommand(ctxRegex as any);
  console.log("✅ Test 10 muvaffaqiyatli o'tdi.\n");

  console.log("🎉 BARCHA KO'P QUIZLI TIZIM TESTLARI (10/10) MUVAFFAQIYATLI O'TDI!");
}

runMultiQuizTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
