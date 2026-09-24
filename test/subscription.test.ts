import assert from "node:assert";
import {
  checkChannelSubscriptions,
  buildSubscriptionMessageAndKeyboard,
  REQUIRED_CHANNELS,
} from "../src/bot/guards/subscriptionGuard.js";
import {
  handleQuizCommand,
  handleQuizByIdCommand,
  handleStopQuizCommand,
  handleCheckSubscriptionCallback,
  startQuizById,
} from "../src/bot/handlers/quiz.js";
import { handleStart } from "../src/bot/handlers/start.js";
import { QuizManager, TelegramApiSender } from "../src/quiz/quizManager.js";
import { getQuizById } from "../src/quiz/questions.js";

// Mock Telegram API Sender
class SubscriptionMockApi implements TelegramApiSender {
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

  // Channel memberships: map of "username:userId" -> boolean
  public memberships = new Map<string, boolean>();
  public shouldFailChannel: string | null = null;

  private nextMessageId = 1000;
  private nextPollId = 1;

  async getChatMember(chatId: number | string, userId: number) {
    if (this.shouldFailChannel === chatId) {
      throw new Error(`Telegram API Error for channel ${chatId}`);
    }
    const key = `${chatId}:${userId}`;
    const isMember = this.memberships.get(key) ?? false;
    if (isMember) {
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
  callbackData?: string;
  api: SubscriptionMockApi;
}) {
  const replies: Array<{ text: string; other?: any }> = [];
  const callbackAlerts: string[] = [];

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
    callbackAlerts,
    reply: async (text: string, other?: any) => {
      replies.push({ text, other });
      return { message_id: 999, text };
    },
    answerCallbackQuery: async (params?: { text?: string; show_alert?: boolean }) => {
      if (params?.text) {
        callbackAlerts.push(params.text);
      }
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

async function runSubscriptionTests() {
  console.log("🧪 MAJBURIY KANAL OBUNASI VA GURUH XULQI TESTLARI BOSHLANDI...\n");

  const api = new SubscriptionMockApi();

  // ========================================================
  // TEST 1: Obuna xabari va tugmalari formati to'g'riligi
  // ========================================================
  console.log("Test 1: Obuna xabari va tugmalari formati to'g'riligi...");
  const subMsg = buildSubscriptionMessageAndKeyboard("amino_acids");
  assert.ok(subMsg.text.includes("@jdaquizkod"), "Xabarda @jdaquizkod bo'lishi kerak");
  assert.ok(subMsg.text.includes("@jdakimyouz"), "Xabarda @jdakimyouz bo'lishi kerak");

  const keyboard = subMsg.reply_markup.inline_keyboard;
  assert.ok(keyboard, "Inline keyboard mavjud bo'lishi kerak");
  assert.strictEqual(keyboard.length, 3, "3 qatorli tugmalar bo'lishi kerak");
  assert.strictEqual(keyboard[0][0].url, "https://t.me/jdaquizkod");
  assert.strictEqual(keyboard[1][0].url, "https://t.me/jdakimyouz");
  assert.strictEqual(keyboard[2][0].text, "✅ A’zo bo‘ldim — tekshirish");
  assert.strictEqual(keyboard[2][0].callback_data, "check_sub_amino_acids", "Quiz ID saqlangan bo'lishi kerak");
  console.log("✅ Test 1 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 2: Obuna bo'lmasdan «✅ A’zo bo‘ldim — tekshirish» bosilganda ogohlantirish
  // ========================================================
  console.log("Test 2: Obuna bo'lmasdan tekshirish tugmasi bosilganda rad etish...");
  const unsubscribedUserId = 888111;
  const ctxCheckFail = createMockContext({
    chatId: unsubscribedUserId,
    chatType: "private",
    userId: unsubscribedUserId,
    callbackData: "check_sub_amino_acids",
    api,
  });

  await handleCheckSubscriptionCallback(ctxCheckFail as any);
  assert.ok(ctxCheckFail.callbackAlerts.length > 0, "Alert yuborilishi kerak");
  assert.ok(
    ctxCheckFail.callbackAlerts[0].includes("hali barcha kanallarga a'zo bo'lmadingiz"),
    "Hali a'zo bo'lmaganligi aytilishi kerak"
  );
  assert.strictEqual(api.sentPolls.length, 0, "Quiz boshlanmasligi kerak");
  console.log("✅ Test 2 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 3: Ikkala kanalga ham a'zo bo'lgach, «✅ A’zo bo‘ldim — tekshirish» bosilganda
  // Shaxsiy chatda quiz boshlanmasligi va guruhga yo'naltirish xabari chiqishi
  // ========================================================
  console.log("Test 3: Obuna tasdiqlangach shaxsiy chatda quiz boshlanmasligi, guruhga yo'naltirish chiqishi...");
  api.memberships.set(`@jdaquizkod:${unsubscribedUserId}`, true);
  api.memberships.set(`@jdakimyouz:${unsubscribedUserId}`, true);

  const ctxCheckSuccess = createMockContext({
    chatId: unsubscribedUserId,
    chatType: "private",
    userId: unsubscribedUserId,
    callbackData: "check_sub_amino_acids",
    api,
  });

  await handleCheckSubscriptionCallback(ctxCheckSuccess as any);
  assert.ok(ctxCheckSuccess.callbackAlerts.some((a) => a.includes("Obuna tasdiqlandi")));

  // Shaxsiy chatda poll yuborilmagan bo'lishi kerak!
  assert.strictEqual(api.sentPolls.length, 0, "Shaxsiy chatda poll YUBORILMASLIGI shart");

  // Guruhga yo'naltirish xabari chiqishi kerak
  assert.strictEqual(ctxCheckSuccess.replies.length, 1);
  assert.ok(
    ctxCheckSuccess.replies[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"),
    "Guruhga yo'naltirish xabari bo'lishi kerak"
  );
  assert.ok(
    ctxCheckSuccess.replies[0].other?.reply_markup?.inline_keyboard?.[0]?.[0]?.url.includes(
      "startgroup=quiz_amino_acids"
    )
  );
  console.log("✅ Test 3 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 4: Deep link (?start=quiz_<ID>) shaxsiy chatda guruhga yo'naltirishi,
  // guruhda esa admin orqali to'g'ridan-to'g'ri boshlanishi
  // ========================================================
  console.log("Test 4: Deep link (?start=quiz_kimyo_asoslari) xulqi...");
  const deepLinkUserId = 888222;
  // Shaxsiy chatda deep link
  const ctxDeepPrivate = createMockContext({
    chatId: deepLinkUserId,
    chatType: "private",
    userId: deepLinkUserId,
    match: "quiz_kimyo_asoslari",
    api,
  });
  await handleStart(ctxDeepPrivate as any);
  assert.strictEqual(ctxDeepPrivate.replies.length, 1);
  assert.ok(
    ctxDeepPrivate.replies[0].text.includes("faqat Telegram guruhlarida o'tkaziladi"),
    "Shaxsiy deep link guruhga yo'naltirishi kerak"
  );
  assert.ok(
    ctxDeepPrivate.replies[0].other?.reply_markup?.inline_keyboard?.[0]?.[0]?.url.includes(
      "startgroup=quiz_kimyo_asoslari"
    )
  );

  // Guruhda admin havola orqali ochganda: obuna so'ralmaydi va to'g'ridan-to'g'ri quiz boshlanadi
  const deepGroupChatId = -1004488;
  const ctxDeepGroup = createMockContext({
    chatId: deepGroupChatId,
    chatType: "supergroup",
    userId: deepLinkUserId,
    isAdmin: true,
    match: "quiz_kimyo_asoslari",
    api,
  });
  await handleStart(ctxDeepGroup as any);
  const deepStartMsg = api.sentMessages.find(
    (m) => m.chatId === deepGroupChatId && m.text.includes("Kimyo asoslari — namuna")
  );
  assert.ok(deepStartMsg !== undefined, "Guruhda admin uchun quiz to'g'ridan-to'g'ri boshlanishi kerak");

  // To'xtatamiz
  await handleStopQuizCommand(ctxDeepGroup as any);
  console.log("✅ Test 4 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 5: Guruhda obuna tekshiruvi UMUMAN BO'LMASLIGI
  // ========================================================
  console.log("Test 5: Guruhda hech kimdan obuna talab qilinmasligi (admin boshlaydi, qatnashchilar javob beradi)...");
  const groupChatId = -10077777;
  const groupAdminUserId = 999111; // Bu admin biror kanalga a'zo EMAS!
  const groupMemberUserId = 999222; // Bu qatnashchi ham biror kanalga a'zo EMAS!

  // Admin kanallarga a'zo emasligini tasdiqlaymiz
  assert.strictEqual(api.memberships.get(`@jdaquizkod:${groupAdminUserId}`), undefined);
  assert.strictEqual(api.memberships.get(`@jdakimyouz:${groupAdminUserId}`), undefined);

  const ctxGroupAdmin = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: groupAdminUserId,
    isAdmin: true,
    api,
  });

  // Guruh admini quizni boshlaydi
  await startQuizById(ctxGroupAdmin as any, "amino_acids");

  // Guruhda e'lon xabari darhol chiqishi kerak (obuna so'ralmasdan!)
  const groupStartMsg = api.sentMessages.find(
    (m) => m.chatId === groupChatId && m.text.includes("Aminokislotalar — suyuqlanish temperaturasi")
  );
  assert.ok(groupStartMsg !== undefined, "Guruhda obunasiz admin quizni to'g'ridan-to'g'ri boshlay olishi kerak");
  assert.strictEqual(ctxGroupAdmin.replies.length, 0, "Guruhda obuna talabi xabari chiqmasligi kerak");

  // Qatnashchi ham javob bera olishi
  // Guruhdagi quizni /stop bilan to'xtatamiz
  await handleStopQuizCommand(ctxGroupAdmin as any);
  console.log("✅ Test 5 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 6: getChatMember Telegram API xatosi berganda
  // ========================================================
  console.log("Test 6: Telegram getChatMember xatolik berganda tushunarli vaqtinchalik xato qaytarish...");
  api.shouldFailChannel = "@jdaquizkod";
  const errorUserId = 444555;
  const ctxError = createMockContext({
    chatId: errorUserId,
    chatType: "private",
    userId: errorUserId,
    api,
  });

  await handleStart(ctxError as any);
  assert.strictEqual(ctxError.replies.length, 1);
  const errorReplyText = ctxError.replies[0].text;
  assert.ok(
    errorReplyText.includes("vaqtinchalik xatolik"),
    "API xatosida vaqtinchalik xato xabari berilishi kerak"
  );
  assert.strictEqual(
    errorReplyText.includes("a'zo bo'ling"),
    false,
    "API xatosida foydalanuvchini 'a'zo emas' deb noto'g'ri ko'rsatmaslik kerak"
  );
  api.shouldFailChannel = null; // Qayta tiklaymiz
  console.log("✅ Test 6 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 7: /quiz buyrug'i @jdaquizkod kanaliga yo'naltirishi (guruhda ham, shaxsiyda ham)
  // ========================================================
  console.log("Test 7: /quiz buyrug'i guruhda ham, shaxsiyda ham kanal xabarini ko'rsatishi va obuna talab qilmasligi...");
  // Guruhda /quiz
  const ctxQuizGroup = createMockContext({
    chatId: -1005555,
    chatType: "group",
    userId: 112233,
    isAdmin: false, // Hatto admin bo'lmagan a'zo yuborsa ham
    api,
  });
  await handleQuizCommand(ctxQuizGroup as any);
  assert.strictEqual(ctxQuizGroup.replies.length, 1);
  assert.ok(
    ctxQuizGroup.replies[0].text.includes("Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz"),
    "Guruhda kanal xabari chiqishi kerak"
  );
  assert.strictEqual(
    ctxQuizGroup.replies[0].other?.reply_markup?.inline_keyboard?.[0]?.[0]?.url,
    "https://t.me/jdaquizkod"
  );

  // Shaxsiy chatda /quiz (obunasiz bo'lsa ham xabar chiqadi, obuna majburlanmaydi)
  const ctxQuizPrivate = createMockContext({
    chatId: 112233,
    chatType: "private",
    userId: 112233,
    api,
  });
  await handleQuizCommand(ctxQuizPrivate as any);
  assert.strictEqual(ctxQuizPrivate.replies.length, 1);
  assert.ok(
    ctxQuizPrivate.replies[0].text.includes("Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz")
  );
  console.log("✅ Test 7 muvaffaqiyatli o'tdi.\n");

  // Obuna tugmasi guruhga ko'chirilsa, admin huquqini chetlab o'tmasin.
  console.log("Test 8: Guruhdagi obuna tugmasi quizni boshlamasligi...");
  const pollsBeforeGroupCallback = api.sentPolls.length;
  const messagesBeforeGroupCallback = api.sentMessages.length;
  const ctxGroupCallback = createMockContext({
    chatId: -1005555,
    chatType: "group",
    userId: unsubscribedUserId,
    isAdmin: false,
    callbackData: "check_sub_amino_acids",
    api,
  });
  await handleCheckSubscriptionCallback(ctxGroupCallback as any);
  assert.strictEqual(api.sentPolls.length, pollsBeforeGroupCallback);
  assert.strictEqual(api.sentMessages.length, messagesBeforeGroupCallback);
  assert.ok(ctxGroupCallback.callbackAlerts[0]?.includes("shaxsiy chatida"));
  console.log("✅ Test 8 muvaffaqiyatli o'tdi.\n");

  // Oddiy /start ham shaxsiy chatda obunani so'rashi kerak.
  console.log("Test 9: Obunasiz shaxsiy /start kanal tugmalarini ko'rsatishi...");
  const startUserId = 777111;
  const ctxStartUnsub = createMockContext({
    chatId: startUserId,
    chatType: "private",
    userId: startUserId,
    api,
  });
  await handleStart(ctxStartUnsub as any);
  assert.strictEqual(ctxStartUnsub.replies.length, 1);
  assert.ok(ctxStartUnsub.replies[0].text.includes("@jdaquizkod"));
  assert.strictEqual(
    ctxStartUnsub.replies[0].other?.reply_markup?.inline_keyboard?.[2]?.[0]?.callback_data,
    "check_sub_start"
  );
  assert.ok(!ctxStartUnsub.replies[0].text.includes("Assalomu alaykum"));
  console.log("✅ Test 9 muvaffaqiyatli o'tdi.\n");

  console.log("Test 10: Obuna tasdiqlangach oddiy /start va tekshirish tugmasi ishlashi...");
  api.memberships.set(`@jdaquizkod:${startUserId}`, true);
  api.memberships.set(`@jdakimyouz:${startUserId}`, true);
  const ctxStartCheck = createMockContext({
    chatId: startUserId,
    chatType: "private",
    userId: startUserId,
    callbackData: "check_sub_start",
    api,
  });
  await handleCheckSubscriptionCallback(ctxStartCheck as any);
  assert.ok(ctxStartCheck.replies[0]?.text.includes("Obuna tasdiqlandi"));
  const ctxStartSub = createMockContext({
    chatId: startUserId,
    chatType: "private",
    userId: startUserId,
    api,
  });
  await handleStart(ctxStartSub as any);
  assert.ok(ctxStartSub.replies[0]?.text.includes("Assalomu alaykum"));
  console.log("✅ Test 10 muvaffaqiyatli o'tdi.\n");

  console.log("Test 11: Guruhdagi /start obunani tekshirmasligi...");
  const ctxGroupStart = createMockContext({
    chatId: -1008888,
    chatType: "supergroup",
    userId: 777222,
    api,
  });
  await handleStart(ctxGroupStart as any);
  assert.ok(ctxGroupStart.replies[0]?.text.includes("JDA Kimyo Quiz Boti faol"));
  assert.ok(!ctxGroupStart.replies[0]?.text.includes("a'zo bo'ling"));
  console.log("✅ Test 11 muvaffaqiyatli o'tdi.\n");

  console.log("🎉 BARCHA MAJBURIY OBUNA VA KANAL INTEGRATSIYASI TESTLARI (11/11) MUVAFFAQIYATLI O'TDI!");
}

runSubscriptionTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
