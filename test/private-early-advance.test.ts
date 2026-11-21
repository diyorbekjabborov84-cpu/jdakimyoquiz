import assert from "node:assert";
import { Quiz, QuizSession } from "../src/quiz/types.js";
import { ISessionStorage, SerializedSession } from "../src/quiz/sessionStorage.js";
import { QuizManager, TelegramApiSender } from "../src/quiz/quizManager.js";

/**
 * Shaxsiy chatda yagona ishtirokchi javob berganda savol vaqti tugashini kutmasdan
 * keyingi savolga o'tiladi. Guruhda esa vaqt oxirigacha kutiladi (boshqalar ham javob beradi).
 */

class MockApi implements TelegramApiSender {
  public messages: string[] = [];
  public stoppedPolls = 0;
  private pollCounter = 1;
  private msgCounter = 100;
  constructor(private prefix: string) {}
  async sendPoll() {
    return { message_id: this.msgCounter++, poll: { id: `${this.prefix}_poll_${this.pollCounter++}` } };
  }
  async stopPoll() {
    this.stoppedPolls++;
    return { ok: true };
  }
  async sendMessage(_chatId: number | string, text: string) {
    this.messages.push(text);
    return { message_id: this.msgCounter++ };
  }
}

class MemoryStorage implements ISessionStorage {
  async saveSession(_s: QuizSession): Promise<void> {}
  async deleteSession(_chatId: number): Promise<void> {}
  async loadAllSessions(): Promise<SerializedSession[]> {
    return [];
  }
}

function makeQuiz(count: number, timeLimitSeconds: number): Quiz {
  return {
    id: "KURS_D99",
    title: "99-dars: sinov",
    description: "Sinov",
    questions: Array.from({ length: count }, (_, i) => ({
      id: `pe_${i + 1}`,
      question: `Savol ${i + 1}?`,
      options: ["A", "B", "C", "D"],
      correctOptionId: 1,
      timeLimitSeconds,
    })),
  };
}

async function waitFor(cond: () => boolean, timeoutMs: number, label: string): Promise<void> {
  const start = Date.now();
  while (!cond()) {
    if (Date.now() - start > timeoutMs) throw new Error(`Kutish vaqti tugadi: ${label}`);
    await new Promise((r) => setTimeout(r, 50));
  }
}

QuizManager.PRIVATE_EARLY_ADVANCE_DELAY_MS = 100;

async function privateChatAdvancesEarly(): Promise<void> {
  const userId = 555001;
  const api = new MockApi("prv");
  const qm = new QuizManager(new MemoryStorage());
  // 30 soniyalik savollar: erta o'tish ishlamasa, test vaqt chegarasidan oshib ketadi
  await qm.startQuiz(userId, makeQuiz(3, 30), api);

  const started = Date.now();
  for (let i = 1; i <= 3; i++) {
    await waitFor(() => qm.getSession(userId)?.currentPollId === `prv_poll_${i}`, 10000, `${i}-savol yuborilishi`);
    const ok = await qm.handlePollAnswer({
      pollId: `prv_poll_${i}`,
      user: { id: userId, first_name: "Talaba" },
      optionIds: [i === 2 ? 0 : 1],
    });
    assert.strictEqual(ok, true, `${i}-javob qabul qilinishi kerak`);
  }

  await waitFor(() => !qm.getSession(userId), 15000, "quiz yakunlanishi");
  const elapsed = Date.now() - started;
  assert.ok(elapsed < 15000, `3 ta 30 soniyalik savol vaqt tugashini kutmasdan o'tishi kerak (ketgan: ${elapsed}ms)`);
  assert.strictEqual(api.stoppedPolls, 3, "Har bir savol javobdan keyin yopilishi kerak");
  const result = api.messages.find((m) => m.includes("yakunlandi"));
  assert.ok(result, "Natija xabari yuborilishi kerak");
  assert.ok(result!.includes("2"), "Natijada 2 ta to'g'ri javob ko'rinishi kerak");
  assert.strictEqual(qm.getTrackedPollCount(), 0, "Pollar xotiradan tozalanishi kerak");
  console.log(`  ✅ Shaxsiy chat: 3 savol ${Math.round(elapsed / 1000)}s da tugadi (vaqt tugashi kutilmadi)`);
}

async function groupChatWaitsForTimer(): Promise<void> {
  const chatId = -1009901;
  const api = new MockApi("grp");
  const qm = new QuizManager(new MemoryStorage());
  await qm.startQuiz(chatId, makeQuiz(2, 30), api);
  await waitFor(() => qm.getSession(chatId)?.currentPollId === "grp_poll_1", 10000, "1-savol yuborilishi");

  const ok = await qm.handlePollAnswer({
    pollId: "grp_poll_1",
    user: { id: 777, first_name: "Ali" },
    optionIds: [1],
  });
  assert.strictEqual(ok, true);
  await new Promise((r) => setTimeout(r, 1500));
  assert.strictEqual(qm.getSession(chatId)?.currentPollId, "grp_poll_1", "Guruhda savol vaqt tugaguncha ochiq qolishi kerak");
  assert.strictEqual(api.stoppedPolls, 0, "Guruhda poll erta yopilmasligi kerak");

  await qm.stopQuiz(chatId, api);
  console.log("  ✅ Guruh: bitta javobdan keyin ham savol vaqti oxirigacha kutiladi");
}

async function lateDuplicateIgnored(): Promise<void> {
  const userId = 555002;
  const api = new MockApi("dup");
  const qm = new QuizManager(new MemoryStorage());
  await qm.startQuiz(userId, makeQuiz(2, 30), api);
  await waitFor(() => qm.getSession(userId)?.currentPollId === "dup_poll_1", 10000, "1-savol");

  const answer = { pollId: "dup_poll_1", user: { id: userId, first_name: "T" }, optionIds: [1] };
  assert.strictEqual(await qm.handlePollAnswer(answer), true);
  assert.strictEqual(await qm.handlePollAnswer(answer), false, "Takroriy javob rad etilishi kerak");

  await waitFor(() => qm.getSession(userId)?.currentPollId === "dup_poll_2", 10000, "2-savolga o'tish");
  assert.strictEqual(await qm.handlePollAnswer(answer), false, "Yopilgan savolga kech javob rad etilishi kerak");
  assert.strictEqual(qm.getLeaderboard(userId)[0].score, 1, "Ball ikki marta hisoblanmasligi kerak");

  await qm.stopQuiz(userId, api);
  console.log("  ✅ Takroriy va kech javoblar ballni buzmaydi");
}

(async () => {
  console.log("Shaxsiy chatda erta o'tish testlari...");
  await privateChatAdvancesEarly();
  await groupChatWaitsForTimer();
  await lateDuplicateIgnored();
  console.log("🎉 Shaxsiy chatda erta o'tish testlari muvaffaqiyatli o'tdi!");
  process.exit(0);
})().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
