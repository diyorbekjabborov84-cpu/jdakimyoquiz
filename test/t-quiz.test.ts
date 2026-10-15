import assert from "node:assert";
import {
  t1Quiz,
  t2Quiz,
  t3Quiz,
  t4Quiz,
  t5Quiz,
  t6Quiz,
  t7Quiz,
  t8Quiz,
  t9Quiz,
} from "../src/quiz/tQuestions.js";
import { getQuizById, allQuizzes } from "../src/quiz/questions.js";
import { QuizManager, prepareSessionQuiz, TelegramApiSender } from "../src/quiz/quizManager.js";
import { JsonFileSessionStorage } from "../src/quiz/sessionStorage.js";

async function runTarixTests() {
  console.log("==================================================================");
  console.log("🧪 T1–T9 (O‘ZBEKISTONNING ENG YANGI TARIXI) TESTLARI");
  console.log("==================================================================");

  const tQuizzes = [
    t1Quiz,
    t2Quiz,
    t3Quiz,
    t4Quiz,
    t5Quiz,
    t6Quiz,
    t7Quiz,
    t8Quiz,
    t9Quiz,
  ];

  // -----------------------------------------------------------------
  // 1. Quizlar Ma'lumotlari va Registratsiyasi
  // -----------------------------------------------------------------
  console.log("\n1. T1–T9 quizlari konfiguratsiyasi va registratsiyasi...");
  assert.strictEqual(tQuizzes.length, 9, "Jami 9 ta Tarix quizi bo'lishi shart");

  let totalQuestionsCount = 0;
  tQuizzes.forEach((q, idx) => {
    const pNum = idx + 1;
    assert.strictEqual(q.id, `T${pNum}`);
    assert.strictEqual(q.groupOnly, true);
    assert.strictEqual(q.shuffle, true);
    assert.ok(q.title.includes(`T${pNum}`));
    assert.strictEqual(q.source, "", "Manba bo'sh satr bo'lishi shart");

    // Lookup tekshiruvlari
    const byId = getQuizById(`T${pNum}`);
    const byIdLower = getQuizById(`t${pNum}`);
    const byQuizCmd = getQuizById(`quiz_T${pNum}`);
    const byStartCmd = getQuizById(`start_t${pNum}`);
    const byUnder = getQuizById(`t_${pNum}`);
    const byDash = getQuizById(`t-${pNum}`);

    assert.ok(byId && byId.id === `T${pNum}`, `getQuizById('T${pNum}') topilmadi`);
    assert.ok(byIdLower && byIdLower.id === `T${pNum}`, `getQuizById('t${pNum}') topilmadi`);
    assert.ok(byQuizCmd && byQuizCmd.id === `T${pNum}`, `getQuizById('quiz_T${pNum}') topilmadi`);
    assert.ok(byStartCmd && byStartCmd.id === `T${pNum}`, `getQuizById('start_t${pNum}') topilmadi`);
    assert.ok(byUnder && byUnder.id === `T${pNum}`, `getQuizById('t_${pNum}') topilmadi`);
    assert.ok(byDash && byDash.id === `T${pNum}`, `getQuizById('t-${pNum}') topilmadi`);

    totalQuestionsCount += q.questions.length;
  });

  assert.strictEqual(totalQuestionsCount, 276, "Jami savollar soni aynan 276 ta bo'lishi shart");
  console.log(`  ✅ Barcha 9 ta quiz ro'yxatga olindi, jami ${totalQuestionsCount} ta savol mavjud`);

  // -----------------------------------------------------------------
  // 2. 276 ta Savol va Telegram Cheklovlari Tekshiruvi
  // -----------------------------------------------------------------
  console.log("\n2. Telegram Poll cheklovlari va variantlar unikalligi...");

  const seenIds = new Set<string>();

  tQuizzes.forEach((quiz) => {
    quiz.questions.forEach((q, qIdx) => {
      // ID unikalligi
      assert.ok(!seenIds.has(q.id), `Takroriy savol ID: ${q.id}`);
      seenIds.add(q.id);

      // Telegram limitlari
      assert.ok(
        q.question.length <= 300,
        `${quiz.id} savol ${q.id} matni 300 belgidan oshmasligi kerak (joriy: ${q.question.length})`
      );
      assert.strictEqual(
        q.options.length,
        4,
        `${quiz.id} savol ${q.id} variantlari soni aynan 4 ta bo'lishi shart`
      );
      q.options.forEach((opt, oIdx) => {
        assert.ok(
          opt.length <= 100,
          `${quiz.id} savol ${q.id} ${oIdx}-varianti 100 belgidan oshmasligi kerak (joriy: ${opt.length}, matn: ${opt})`
        );
        assert.ok(opt.trim().length > 0, `${quiz.id} savol ${q.id} ${oIdx}-varianti bo'sh bo'lmasligi kerak`);
      });

      // Variantlar takrorlanmasligi
      const uniqueOpts = new Set(q.options);
      assert.strictEqual(
        uniqueOpts.size,
        4,
        `${quiz.id} savol ${q.id} da variantlar takrorlangan: ${q.options.join(" | ")}`
      );

      // To'g'ri javob indeksi 0..3
      assert.ok(
        q.correctOptionId >= 0 && q.correctOptionId <= 3,
        `${quiz.id} savol ${q.id} noto'g'ri correctOptionId: ${q.correctOptionId}`
      );

      // Taymer 20s
      assert.strictEqual(
        q.timeLimitSeconds,
        20,
        `${quiz.id} savol ${q.id} vaqti 20 soniya bo'lishi shart`
      );
    });
  });

  console.log("  ✅ Barcha 276 ta savol Telegram cheklovlariga (<=300 / <=100 / 4 unikal variant / 20s) to'liq mos");

  // -----------------------------------------------------------------
  // 3. Aralashtirish (Shuffle) Butunligi
  // -----------------------------------------------------------------
  console.log("\n3. Dinamik aralashtirishda to'g'ri javob matni saqlanishi...");

  tQuizzes.forEach((quiz) => {
    const prepared = prepareSessionQuiz(quiz);
    assert.strictEqual(prepared.questions.length, quiz.questions.length);

    prepared.questions.forEach((q) => {
      const orig = quiz.questions.find((o) => o.id === q.id)!;
      const expectedCorrect = orig.options[orig.correctOptionId];
      const actualCorrect = q.options[q.correctOptionId];
      assert.strictEqual(
        actualCorrect,
        expectedCorrect,
        `${quiz.id} aralashtirishdan keyin to'g'ri javob matni buzildi (${q.id})`
      );
    });
  });

  console.log("  ✅ Barcha 9 ta quiz aralashganda ham to'g'ri javoblar buzilmaydi");

  // -----------------------------------------------------------------
  // 4. QuizManager bilan T1 Sessiyasini Sinash
  // -----------------------------------------------------------------
  console.log("\n4. QuizManager T1 sessiyasi va Telegram poll yuborilishi...");

  const testChatId = -100998822;
  const sessionStorage = new JsonFileSessionStorage("./temp_t_test_sessions.json");
  const quizManager = new QuizManager(sessionStorage);

  const sentPolls: Array<{ chatId: number; question: string; options: string[]; openPeriod: number }> = [];

  const mockApi: TelegramApiSender = {
    async sendMessage(chatId, text) {
      return { message_id: 100, text };
    },
    async sendPoll(chatId, question, options, params) {
      sentPolls.push({
        chatId,
        question,
        options,
        openPeriod: params?.open_period ?? 0,
      });
      return {
        message_id: 200 + sentPolls.length,
        poll: {
          id: `t1_poll_${sentPolls.length}`,
          question,
          options: options.map((text, voter_count) => ({ text, voter_count })),
          total_voter_count: 0,
          is_closed: false,
          is_anonymous: false,
          type: "quiz",
          allows_multiple_answers: false,
          correct_option_id: params?.correct_option_id ?? 0,
        },
      };
    },
    async stopPoll(chatId, messageId) {
      return {
        id: "t1_poll",
        question: "test",
        options: [],
        total_voter_count: 0,
        is_closed: true,
        is_anonymous: false,
        type: "quiz",
        allows_multiple_answers: false,
      };
    },
  };

  const startRes = await quizManager.startQuiz(testChatId, t1Quiz, mockApi);
  assert.strictEqual(startRes.success, true);
  await quizManager.sendNextQuestion(testChatId, mockApi);

  assert.strictEqual(sentPolls.length, 1);
  assert.strictEqual(sentPolls[0].openPeriod, 20);
  assert.strictEqual(sentPolls[0].options.length, 4);

  // Leaderboard xabarida yaratuvchi va manba formati
  const mockSession = {
    sessionId: "mock_t_session",
    chatId: testChatId,
    quiz: t1Quiz,
    status: "finishing" as const,
    currentQuestionIndex: 30,
    currentPollId: null,
    currentPollMessageId: null,
    questionStartTime: 0,
    timer: null,
    answeredUsers: new Set<string>(),
    participants: new Map(),
    consecutiveUnansweredCount: 0,
    currentQuestionAnswered: true,
    version: 1,
  };
  const msgs = quizManager.formatLeaderboardMessages(mockSession, []);
  assert.ok(msgs[0].includes("Test yaratuvchisi: <a href=\"https://t.me/diyorbek_jabborov\">@diyorbek_jabborov</a>"));
  assert.ok(msgs[0].includes("Savollar manbasi:"));
  assert.ok(!msgs[0].includes("Tarix fakulteti"), "Eski manba chiqmasligi kerak");

  await quizManager.stopQuiz(testChatId, mockApi, 999);
  try {
    const fs = await import("node:fs");
    if (fs.existsSync("./temp_t_test_sessions.json")) {
      fs.unlinkSync("./temp_t_test_sessions.json");
    }
  } catch {}

  console.log("  ✅ QuizManager T1 quizi boshlandi va xabarda «Test yaratuvchisi» va bo‘sh «Savollar manbasi:» to‘g‘ri shakllandi");

  console.log("\n==================================================================");
  console.log("🎉 BARCHA T1–T9 TESTLARI (4/4) 100% MUVAFFAQIYATLI O'TDI!");
  console.log("==================================================================");
}

runTarixTests().catch((err) => {
  console.error("❌ T1–T9 testlarida xatolik:", err);
  process.exit(1);
});
