import assert from "node:assert/strict";
import { checkGroupSize } from "../src/bot/guards/groupSizeGuard.js";
import { startQuizById } from "../src/bot/handlers/quiz.js";
import { quizManager } from "../src/quiz/quizManager.js";

async function run() {
  const chat = { id: -1001200, type: "supergroup", title: "Kichik guruh" };
  const makeContext = (count: number | Error) => ({
    chat,
    api: {
      getChatMemberCount: async () => {
        if (count instanceof Error) throw count;
        return count;
      },
    },
  });

  assert.deepEqual(await checkGroupSize(makeContext(12) as any), {
    allowed: false,
    peopleCount: 11,
    message: "Quiz boshlash uchun guruhda kamida 12 kishi bo'lishi kerak. Hozir 11 kishi bor.",
  });
  assert.deepEqual(await checkGroupSize(makeContext(13) as any), {
    allowed: true,
    peopleCount: 12,
  });

  const failure = await checkGroupSize(makeContext(new Error("Telegram unavailable")) as any);
  assert.equal(failure.allowed, false);
  assert.match(failure.message, /tekshirib bo'lmadi/);

  const replies: string[] = [];
  const ctx = {
    ...makeContext(12),
    reply: async (message: string) => { replies.push(message); },
  };
  await startQuizById(ctx as any, "amino_acids");
  assert.equal(quizManager.isQuizActive(chat.id), false);
  assert.match(replies[0], /kamida 12 kishi/);

  console.log("✅ Guruh hajmi: 11 kishi rad, 12 kishi ruxsat, API xatosi rad; kichik guruhda quiz boshlanmadi.");
}

run().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
