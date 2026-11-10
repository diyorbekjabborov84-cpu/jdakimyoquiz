import assert from "node:assert";
import {
  handleQuizCommand,
  handleStopQuizCommand,
  handleCheckSubscriptionCallback,
  startQuizById,
} from "../src/bot/handlers/quiz.js";
import { handleStart } from "../src/bot/handlers/start.js";
import { TelegramApiSender } from "../src/quiz/quizManager.js";
import {
  addKursParticipant,
  resetShellStateForTest,
} from "../src/shell/shell.js";
import {
  populateKursMemory,
  clearKursDarslarForTest,
} from "../src/kurs/kursRepository.js";
import { resetBotSettingsState } from "../src/settings/botSettings.js";

class SubscriptionMockApi implements TelegramApiSender {
  async getChatMemberCount(_chatId: number | string) {
    return 13;
  }
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
  console.log("🧪 MAJBURIY OBUNA BEKOR QILINGANI VA QOBIQ XULQI TESTLARI BOSHLANDI...\n");

  resetShellStateForTest();
  resetBotSettingsState();
  clearKursDarslarForTest();

  const api = new SubscriptionMockApi();

  // ========================================================
  // TEST 1: Eski check_sub_* callback bosilganda "Obuna endi talab qilinmaydi" qaytishi
  // ========================================================
  console.log("Test 1: Eski check_sub_* tugmasi bosilganda javob qaytishi...");
  const ctxOldCheckSub = createMockContext({
    chatId: 888111,
    chatType: "private",
    userId: 888111,
    callbackData: "check_sub_amino_acids",
    api,
  });

  await handleCheckSubscriptionCallback(ctxOldCheckSub as any);
  assert.strictEqual(ctxOldCheckSub.callbackAlerts.length, 1);
  assert.strictEqual(ctxOldCheckSub.callbackAlerts[0], "Obuna endi talab qilinmaydi");
  assert.strictEqual(api.sentPolls.length, 0);
  console.log("✅ Test 1 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 2: Shaxsiy chatda oddiy foydalanuvchi /start bosganda obuna so'ralmasligi,
  // balki kurs haqida xabar va adminga yozish tugmasi chiqishi
  // ========================================================
  console.log("Test 2: Shaxsiy chatda oddiy foydalanuvchiga kurs ma'lumoti va admin kontakti chiqishi...");
  const regularUserId = 888222;
  const ctxPrivateStart = createMockContext({
    chatId: regularUserId,
    chatType: "private",
    userId: regularUserId,
    api,
  });

  await handleStart(ctxPrivateStart as any);
  assert.strictEqual(ctxPrivateStart.replies.length, 1);
  const privateReply = ctxPrivateStart.replies[0];
  assert.ok(privateReply.text.includes("Assalomu alaykum"));
  assert.ok(privateReply.text.includes("faqat «Kimyo 0 dan» kursi ishtirokchilari uchun ishlaydi"));
  assert.ok(privateReply.text.includes("@diyorbek_jabborov"));
  assert.ok(!privateReply.text.includes("check_sub"), "Obuna tekshirish tugmasi chiqmasligi kerak");
  assert.strictEqual(
    privateReply.other?.reply_markup?.inline_keyboard?.[0]?.[0]?.text,
    "✉️ Adminga yozish"
  );
  assert.strictEqual(
    privateReply.other?.reply_markup?.inline_keyboard?.[0]?.[0]?.url,
    "https://t.me/diyorbek_jabborov"
  );
  console.log("✅ Test 2 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 3: Shaxsiy chatda kurs a'zosi /start bosganda obunasiz kurs menyusi ochilishi
  // ========================================================
  console.log("Test 3: Kurs ishtirokchisiga shaxsiy chatda obunasiz kurs menyusi ochilishi...");
  populateKursMemory([
    {
      dars: 1,
      mavzu: "Sinov darsi mavzusi",
      testlar: [
        {
          id: "FAKE_D01_T01",
          savol: "Sinov savoli 1?",
          variantlar: { A: "V1", B: "V2", C: "V3", D: "V4" },
          javob: "A",
        },
      ],
    },
  ]);

  const kursUserId = 888333;
  await addKursParticipant({ userId: kursUserId, ism: "Kurs Talabasi" });

  const ctxKursStart = createMockContext({
    chatId: kursUserId,
    chatType: "private",
    userId: kursUserId,
    api,
  });

  await handleStart(ctxKursStart as any);
  assert.strictEqual(ctxKursStart.replies.length, 1);
  assert.ok(ctxKursStart.replies[0].text.includes("«Kimyo 0 dan» — testlar"));
  const firstLessonBtn = ctxKursStart.replies[0].other?.reply_markup?.inline_keyboard?.[0]?.[0];
  assert.ok(firstLessonBtn?.text.includes("1-dars: Sinov darsi mavzusi"));
  assert.strictEqual(firstLessonBtn?.callback_data, "m:k:d:1");
  console.log("✅ Test 3 muvaffaqiyatli o'tdi.\n");

  // ========================================================
  // TEST 4: Asosiy guruhda obunasiz quiz boshlanishi va menyu chiqishi
  // ========================================================
  console.log("Test 4: Asosiy guruhda obunasiz /quiz menyusi va quiz boshlanishi...");
  const groupChatId = -10077777;
  const groupAdminUserId = 999111;

  const ctxGroupMenu = createMockContext({
    chatId: groupChatId,
    chatType: "supergroup",
    userId: groupAdminUserId,
    isAdmin: true,
    api,
  });

  await handleQuizCommand(ctxGroupMenu as any);
  assert.strictEqual(ctxGroupMenu.replies.length, 1);
  assert.ok(ctxGroupMenu.replies[0].text.includes("Testlar bo‘limlari"));

  await startQuizById(ctxGroupMenu as any, "amino_acids");
  const groupStartMsg = api.sentMessages.find(
    (m) => m.chatId === groupChatId && m.text.includes("Aminokislotalar — suyuqlanish temperaturasi")
  );
  assert.ok(groupStartMsg !== undefined, "Guruhda obunasiz quiz to'g'ridan-to'g'ri boshlanishi kerak");

  await handleStopQuizCommand(ctxGroupMenu as any);
  console.log("✅ Test 4 muvaffaqiyatli o'tdi.\n");

  clearKursDarslarForTest();
  resetShellStateForTest();
  resetBotSettingsState();

  console.log("🎉 BARCHA OBUNA VA QOBIQ SINOVLARI (4/4) MUVAFFAQIYATLI O'TDI!");
}

runSubscriptionTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
