import assert from "node:assert";
import { d6Quiz } from "../src/quiz/d6Questions.js";
import { getQuizById, allQuizzes } from "../src/quiz/questions.js";
import { QuizManager, prepareSessionQuiz, TelegramApiSender, QuizSession } from "../src/quiz/quizManager.js";
import { JsonFileSessionStorage } from "../src/quiz/sessionStorage.js";

async function runD6Tests() {
  console.log("==================================================================");
  console.log("🧪 D6 (DINSHUNOSLIK — 6-MAVZU: ISLOM DINI) QUIZ TESTLARI");
  console.log("==================================================================");

  // -----------------------------------------------------------------
  // 1. Quiz Ma'lumotlari va Registratsiyasi
  // -----------------------------------------------------------------
  console.log("\n1. D6 quizi konfiguratsiyasi va registratsiyasi...");
  assert.strictEqual(d6Quiz.id, "D6");
  assert.strictEqual(d6Quiz.groupOnly, true, "Quiz faqat guruhlar uchun bo'lishi shart");
  assert.strictEqual(d6Quiz.shuffle, true, "Savollar va variantlar har sessiyada aralashtirilishi shart");
  assert.strictEqual(d6Quiz.source, "", "Savollar manbasi bo'sh satr bo'lishi shart (talab bo'yicha)");
  assert.strictEqual(d6Quiz.questions.length, 40, "Savollar soni aynan 40 ta bo'lishi shart");

  // getQuizById orqali topilishi
  const byD6 = getQuizById("D6");
  const byD6Lower = getQuizById("d6");
  const byQuizD6 = getQuizById("quiz_D6");
  const byStartD6 = getQuizById("start_d6");
  const byD_6 = getQuizById("d_6");
  const byD_Dash_6 = getQuizById("d-6");

  assert.ok(byD6 && byD6.id === "D6", "getQuizById('D6') topilmadi");
  assert.ok(byD6Lower && byD6Lower.id === "D6", "getQuizById('d6') topilmadi");
  assert.ok(byQuizD6 && byQuizD6.id === "D6", "getQuizById('quiz_D6') topilmadi");
  assert.ok(byStartD6 && byStartD6.id === "D6", "getQuizById('start_d6') topilmadi");
  assert.ok(byD_6 && byD_6.id === "D6", "getQuizById('d_6') topilmadi");
  assert.ok(byD_Dash_6 && byD_Dash_6.id === "D6", "getQuizById('d-6') topilmadi");

  console.log("  ✅ D6 quizi ro'yxatga olindi va barcha sinonimlar orqali topildi");

  // -----------------------------------------------------------------
  // 2. 40 ta Savol, Variantlar va To'g'ri Javoblar Tekshiruvi
  // -----------------------------------------------------------------
  console.log("\n2. 40 ta savol, variantlar va to'g'ri javoblar tekshiruvi...");

  const seenIds = new Set<string>();
  const seenQuestions = new Set<string>();

  d6Quiz.questions.forEach((q, idx) => {
    const qNum = idx + 1;
    // ID formati
    assert.strictEqual(q.id, `d6_${qNum}`, `${qNum}-savol ID si d6_${qNum} bo'lishi kerak`);
    assert.ok(!seenIds.has(q.id), `Takroriy savol ID: ${q.id}`);
    seenIds.add(q.id);

    // Savol matni
    assert.ok(q.question && q.question.trim().length > 10, `${qNum}-savol matni yetarli emas`);
    assert.ok(!seenQuestions.has(q.question), `Takroriy savol matni: ${q.question}`);
    seenQuestions.add(q.question);

    // Variantlar soni aynan 4 ta
    assert.strictEqual(q.options.length, 4, `${qNum}-savol variantlari soni 4 ta bo'lishi shart`);
    q.options.forEach((opt, optIdx) => {
      assert.ok(opt && opt.trim().length > 0, `${qNum}-savol ${optIdx}-varianti bo'sh bo'lmasligi kerak`);
    });

    // Variantlar orasida takrorlanish yo'qligi
    const uniqueOptions = new Set(q.options);
    assert.strictEqual(uniqueOptions.size, 4, `${qNum}-savol variantlarida dublikatlar bor`);

    // To'g'ri javob indeksi 0..3 oralig'ida
    assert.ok(
      q.correctOptionId >= 0 && q.correctOptionId <= 3,
      `${qNum}-savol to'g'ri javob indeksi 0-3 oralig'ida emas: ${q.correctOptionId}`
    );

    // Telegram qat'iy cheklovlari tekshiruvi:
    assert.ok(q.question.length <= 300, `${qNum}-savol matni 300 belgidan oshmasligi kerak (joriy: ${q.question.length})`);
    q.options.forEach((opt, optIdx) => {
      assert.ok(opt.length <= 100, `${qNum}-savol ${optIdx}-varianti 100 belgidan oshmasligi kerak (joriy: ${opt.length})`);
    });
    if (q.explanation) {
      assert.ok(q.explanation.length <= 200, `${qNum}-savol izohi 200 belgidan oshmasligi kerak (joriy: ${q.explanation.length})`);
    }

    // Vaqt chegarasi aynan 20 soniya
    assert.strictEqual(q.timeLimitSeconds, 20, `${qNum}-savol vaqti 20 soniya bo'lishi shart`);

    // Izoh mavjudligi
    assert.ok(q.explanation && q.explanation.trim().length > 0, `${qNum}-savol izohi mavjud bo'lishi shart`);
  });

  console.log("  ✅ Barcha 40 ta savol 4 tadan unikal variant, to'g'ri indeks, 20s vaqt va Telegram poll limitlariga mos");

  // -----------------------------------------------------------------
  // 3. Variantlar va Savollarning Aralashishi (Shuffle)
  // -----------------------------------------------------------------
  console.log("\n3. Savollar va variantlar har sessiyada to'g'ri aralashishi...");

  const prepared1 = prepareSessionQuiz(d6Quiz);
  assert.strictEqual(prepared1.questions.length, 40);

  // Aralashgandan keyin ham to'g'ri javoblar buzilmasligi
  prepared1.questions.forEach((q) => {
    const origQ = d6Quiz.questions.find((orig) => orig.id === q.id)!;
    const expectedCorrectText = origQ.options[origQ.correctOptionId];
    const actualCorrectText = q.options[q.correctOptionId];
    assert.strictEqual(
      actualCorrectText,
      expectedCorrectText,
      `Aralashtirishdan keyin to'g'ri javob matni o'zgarib ketdi (${q.id})`
    );
  });
  console.log("  ✅ Savollar va javob variantlari to'g'ri indekslar bilan xavfsiz aralashdi");

  // -----------------------------------------------------------------
  // 4. QuizManager Sessiyasi, 20s lik poll va Manba/Yaratuvchi ko'rinishi
  // -----------------------------------------------------------------
  console.log("\n4. QuizManager sessiyasi, 20s poll va Manba/Yaratuvchi tekshiruvi...");

  const testChatId = -100998822;
  const sessionStorage = new JsonFileSessionStorage("./temp_d6_test_sessions.json");
  const quizManager = new QuizManager(sessionStorage);

  const sentPolls: Array<{ chatId: number; question: string; options: string[]; correctOptionId: number; openPeriod: number }> = [];

  const mockApi: TelegramApiSender = {
    async sendMessage(chatId, text, options) {
      return { message_id: 100, text };
    },
    async sendPoll(chatId, question, options, params) {
      sentPolls.push({
        chatId,
        question,
        options,
        correctOptionId: params?.correct_option_id ?? 0,
        openPeriod: params?.open_period ?? 0,
      });
      return {
        message_id: 200 + sentPolls.length,
        poll: {
          id: `d6_poll_${sentPolls.length}`,
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
        id: "d6_poll",
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

  const startRes = await quizManager.startQuiz(testChatId, d6Quiz, mockApi);
  assert.strictEqual(startRes.success, true);
  await quizManager.sendNextQuestion(testChatId, mockApi);

  assert.strictEqual(sentPolls.length, 1, "1-savol poll sifatida chiqishi kerak");
  assert.strictEqual(sentPolls[0].openPeriod, 20, "Poll ochiq turish vaqti 20 soniya bo'lishi kerak");
  assert.strictEqual(sentPolls[0].options.length, 4, "Poll 4 ta variantga ega bo'lishi kerak");

  // Leaderboard xabarida Test yaratuvchisi va Savollar manbasi tekshiruvi
  const mockSession: QuizSession = {
    chatId: testChatId,
    quiz: d6Quiz,
    currentQuestionIndex: 40,
    scores: {},
    isActive: false,
  };
  const leaderboardMsgs = quizManager.formatLeaderboardMessages(mockSession, []);
  assert.ok(leaderboardMsgs.length > 0);
  assert.ok(
    leaderboardMsgs[0].includes("Test yaratuvchisi: <a href=\"https://t.me/diyorbek_jabborov\">@diyorbek_jabborov</a>"),
    "Test yaratuvchisi ko'rsatilmadi"
  );
  assert.ok(
    leaderboardMsgs[0].includes("Savollar manbasi:"),
    "Savollar manbasi qatori ko'rsatilmadi"
  );

  // To'xtatish
  await quizManager.stopQuiz(testChatId, mockApi, 999);
  try {
    const fs = await import("node:fs");
    if (fs.existsSync("./temp_d6_test_sessions.json")) {
      fs.unlinkSync("./temp_d6_test_sessions.json");
    }
  } catch {}
  console.log("  ✅ QuizManager D6 ni muvaffaqiyatli boshladi, 20s poll yubordi va manba/yaratuvchi formatini to'g'ri chiqardi");

  console.log("\n==================================================================");
  console.log("🎉 BARCHA D6 TESTLARI (4/4) 100% MUVAFFAQIYATLI O'TDI!");
  console.log("==================================================================");
}

runD6Tests().catch((err) => {
  console.error("❌ D6 testlarida xatolik:", err);
  process.exit(1);
});
