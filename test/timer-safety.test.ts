import assert from "node:assert";
import { Quiz, QuizSession } from "../src/quiz/types.js";
import { ISessionStorage, SerializedSession } from "../src/quiz/sessionStorage.js";
import { QuizManager, TelegramApiSender } from "../src/quiz/quizManager.js";

/**
 * Taymer xavfsizligi va xotira tozalanishi testlari:
 * 1. Quiz tugagach pollToSession xaritasi bo'shaydi (xotira o'smaydi).
 * 2. finishQuiz taymer ichida xato bersa, jarayon yiqilmaydi va qayta urinib yakunlanadi.
 * 3. Doimiy xatoda qayta urinishlar cheklangan va sessiya "finishing" holatida xavfsiz qoladi.
 */

const unhandled: unknown[] = [];
process.on("unhandledRejection", (reason) => {
  unhandled.push(reason);
});

class MockApi implements TelegramApiSender {
  public messages: string[] = [];
  private pollCounter = 1;
  private msgCounter = 100;
  constructor(private prefix: string) {}

  async sendPoll() {
    return { message_id: this.msgCounter++, poll: { id: `${this.prefix}_poll_${this.pollCounter++}` } };
  }
  async stopPoll() {
    return { ok: true };
  }
  async sendMessage(_chatId: number | string, text: string) {
    this.messages.push(text);
    return { message_id: this.msgCounter++ };
  }
}

/** Xotiradagi saqlash; "finishing" holatidagi dastlabki `failFinishingSaves` ta yozuvda xato beradi. */
class FlakyStorage implements ISessionStorage {
  public saved = new Map<number, string>();
  public finishingFailures = 0;
  constructor(private failFinishingSaves: number) {}

  async saveSession(session: QuizSession): Promise<void> {
    if (session.status === "finishing" && this.finishingFailures < this.failFinishingSaves) {
      this.finishingFailures++;
      throw new Error("Firestore vaqtinchalik ishlamayapti (sinov)");
    }
    this.saved.set(session.chatId, session.status);
  }
  async deleteSession(chatId: number): Promise<void> {
    this.saved.delete(chatId);
  }
  async loadAllSessions(): Promise<SerializedSession[]> {
    return [];
  }
}

function makeQuiz(questionCount: number): Quiz {
  return {
    id: "timer_safety",
    title: "Taymer xavfsizligi sinovi",
    description: "Sinov",
    groupOnly: true,
    questions: Array.from({ length: questionCount }, (_, i) => ({
      id: `ts_${i + 1}`,
      question: `Savol ${i + 1}?`,
      options: ["A", "B", "C", "D"],
      correctOptionId: 0,
      timeLimitSeconds: 1,
    })),
  };
}

async function waitFor(cond: () => boolean, timeoutMs: number, label: string): Promise<void> {
  const start = Date.now();
  while (!cond()) {
    if (Date.now() - start > timeoutMs) {
      throw new Error(`Kutish vaqti tugadi: ${label}`);
    }
    await new Promise((r) => setTimeout(r, 50));
  }
}

async function scenarioMemoryCleanup(): Promise<void> {
  const chatId = -1007001;
  const api = new MockApi("mem");
  const qm = new QuizManager(new FlakyStorage(0));

  await qm.startQuiz(chatId, makeQuiz(2), api);
  await waitFor(() => qm.getTrackedPollCount() === 1, 5000, "1-poll yuborilishi");

  // Javob beramiz (pauza ishlamasligi uchun)
  const res = await qm.handlePollAnswer({
    pollId: "mem_poll_1",
    user: { id: 1, first_name: "Ali" },
    optionIds: [qm.getSession(chatId)!.quiz.questions[0].correctOptionId],
  });
  assert.strictEqual(res, true, "Javob qabul qilinishi kerak");

  await waitFor(() => !qm.getSession(chatId), 15000, "quiz yakunlanishi");
  assert.strictEqual(qm.getTrackedPollCount(), 0, "Quiz tugagach pollToSession bo'sh bo'lishi kerak");
  assert.ok(api.messages.some((m) => m.includes("yakunlandi")), "Natija xabari yuborilishi kerak");

  // Yopilgan pollga kech kelgan javob rad etiladi
  const late = await qm.handlePollAnswer({ pollId: "mem_poll_1", user: { id: 2, first_name: "Vali" }, optionIds: [0] });
  assert.strictEqual(late, false, "Yopilgan pollga javob rad etilishi kerak");
  console.log("  ✅ Quiz tugagach pollToSession tozalandi, kech javob rad etildi");
}

async function scenarioFinishRetrySucceeds(): Promise<void> {
  const chatId = -1007002;
  const api = new MockApi("retry");
  const storage = new FlakyStorage(2);
  const qm = new QuizManager(storage);

  await qm.startQuiz(chatId, makeQuiz(1), api);
  await waitFor(() => !qm.getSession(chatId), 15000, "qayta urinishdan so'ng yakunlanish");

  assert.strictEqual(storage.finishingFailures, 2, "Ikki marta xato berishi kerak edi");
  assert.ok(api.messages.some((m) => m.includes("yakunlandi")), "Qayta urinishdan so'ng natija e'lon qilinishi kerak");
  assert.strictEqual(storage.saved.has(chatId), false, "Sessiya bazadan o'chirilishi kerak");
  console.log("  ✅ finishQuiz xatosi jarayonni yiqitmadi, 2 xatodan so'ng quiz yakunlandi");
}

async function scenarioFinishRetryGivesUp(): Promise<void> {
  const chatId = -1007003;
  const api = new MockApi("giveup");
  const storage = new FlakyStorage(Number.POSITIVE_INFINITY);
  const qm = new QuizManager(storage);

  await qm.startQuiz(chatId, makeQuiz(1), api);
  const expectedFailures = 1 + QuizManager.FINISH_RETRY_MAX_ATTEMPTS;
  await waitFor(() => storage.finishingFailures >= expectedFailures, 15000, "barcha qayta urinishlar");
  await new Promise((r) => setTimeout(r, 1500));

  assert.strictEqual(storage.finishingFailures, expectedFailures, "Qayta urinishlar soni cheklangan bo'lishi kerak");
  assert.strictEqual(qm.getSession(chatId)?.status, "finishing", "Sessiya finishing holatida xavfsiz qolishi kerak");
  assert.ok(!api.messages.some((m) => m.includes("yakunlandi")), "Natija saqlanmasa xabar yuborilmasligi kerak");

  // /stop baribir ishlaydi
  assert.strictEqual(await qm.stopQuiz(chatId, api), true);
  assert.strictEqual(qm.getSession(chatId), undefined);
  console.log(`  ✅ Doimiy xatoda ${QuizManager.FINISH_RETRY_MAX_ATTEMPTS} ta qayta urinishdan so'ng to'xtadi, /stop ishlaydi`);
}

async function run() {
  console.log("=== Taymer xavfsizligi va xotira tozalanishi testlari ===\n");
  QuizManager.FINISH_RETRY_BASE_DELAY_MS = 50;

  await Promise.all([scenarioMemoryCleanup(), scenarioFinishRetrySucceeds(), scenarioFinishRetryGivesUp()]);

  assert.deepStrictEqual(unhandled, [], "Ushlanmagan Promise xatolari bo'lmasligi kerak");
  console.log("  ✅ Ushlanmagan Promise xatolari yo'q");
  console.log("\n🎉 Taymer xavfsizligi testlari muvaffaqiyatli o'tdi!");
  process.exit(0);
}

run().catch((err) => {
  console.error("❌ Test muvaffaqiyatsiz:", err);
  process.exit(1);
});
