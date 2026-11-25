import assert from "node:assert";
import fs from "node:fs";
import {
  dh1Quiz,
  dh2Quiz,
  dh3Quiz,
  dh4Quiz,
  allDhQuizzes,
} from "../src/quiz/dhQuestions.js";
import { d1Quiz } from "../src/quiz/d1Questions.js";
import { d6Quiz } from "../src/quiz/d6Questions.js";
import { getQuizById, allQuizzes } from "../src/quiz/questions.js";
import {
  QuizManager,
  prepareSessionQuiz,
  formatQuizAuthorHtml,
  TelegramApiSender,
  QuizSession,
} from "../src/quiz/quizManager.js";
import { JsonFileSessionStorage } from "../src/quiz/sessionStorage.js";
import { handleInlineQuery } from "../src/bot/handlers/inlineQuery.js";

async function runDhTests() {
  console.log("==================================================================");
  console.log("🧪 DH1–DH4 (DINSHUNOSLIK, DIYORBEK HASANOV — 80 TA SAVOL) TESTLARI");
  console.log("==================================================================");

  // -----------------------------------------------------------------
  // 1. Quizlar konfiguratsiyasi va registratsiyasi
  // -----------------------------------------------------------------
  console.log("\n1. DH1–DH4 quizlari konfiguratsiyasi va registratsiyasi...");
  assert.strictEqual(allDhQuizzes.length, 4, "Jami 4 ta DH quizi bo'lishi shart");

  let totalQuestions = 0;
  allDhQuizzes.forEach((q, idx) => {
    const num = idx + 1;
    const expectedId = `DH${num}`;
    assert.strictEqual(q.id, expectedId);
    assert.strictEqual(q.groupOnly, true, `${expectedId} faqat guruhlar uchun bo'lishi shart`);
    assert.strictEqual(q.shuffle, true, `${expectedId} aralashtirilishi shart`);
    assert.strictEqual(q.bolim, "dinshunoslik");
    assert.strictEqual(q.source, "", `${expectedId} manbasi bo'sh satr bo'lishi shart`);
    assert.strictEqual(q.author, "Diyorbek Hasanov (@Dr_xasanov07)");
    assert.strictEqual(q.questions.length, 20, `${expectedId} da aynan 20 ta savol bo'lishi shart`);
    assert.ok(allQuizzes.some((item) => item.id === expectedId), `${expectedId} allQuizzes ga qo'shilmagan`);

    const variants = [
      expectedId,
      `dh${num}`,
      `quiz_${expectedId}`,
      `start_dh${num}`,
      `dh_${num}`,
      `dh-${num}`,
    ];
    for (const alias of variants) {
      const found = getQuizById(alias);
      assert.ok(found && found.id === expectedId, `getQuizById('${alias}') -> ${expectedId} topilmadi`);
    }

    totalQuestions += q.questions.length;
  });

  assert.strictEqual(totalQuestions, 80, "Jami savollar soni aynan 80 ta bo'lishi shart");
  console.log("  ✅ DH1–DH4 (4 x 20 = 80 ta savol) ro'yxatga olindi va barcha aliaslar orqali topildi");

  // -----------------------------------------------------------------
  // 2. 80 ta savol, variantlar, Telegram limitlari va kalit tekshiruvi
  // -----------------------------------------------------------------
  console.log("\n2. 80 ta savolning tuzilishi, unikal IDlar, limitlar va kalitlari...");

  const seenIds = new Set<string>();
  const seenQuestionsPerQuiz = new Map<string, Set<string>>();

  allDhQuizzes.forEach((quiz, qIdx) => {
    const partNum = qIdx + 1;
    const seenQ = new Set<string>();
    seenQuestionsPerQuiz.set(quiz.id, seenQ);

    quiz.questions.forEach((q, idx) => {
      const n = idx + 1;
      assert.strictEqual(q.id, `dh${partNum}_${n}`, `ID dh${partNum}_${n} bo'lishi shart`);
      assert.ok(!seenIds.has(q.id), `Takroriy ID: ${q.id}`);
      seenIds.add(q.id);

      assert.ok(q.question && q.question.trim().length >= 8, `${q.id} savol matni juda qisqa`);
      assert.ok(q.question.length <= 300, `${q.id} savoli 300 belgidan oshmasligi kerak (${q.question.length})`);
      assert.ok(!seenQ.has(q.question), `${quiz.id} ichida takroriy savol: ${q.question}`);
      seenQ.add(q.question);

      assert.strictEqual(q.options.length, 4, `${q.id} variantlari soni 4 ta bo'lishi shart`);
      q.options.forEach((opt, optIdx) => {
        assert.ok(opt && opt.trim().length > 0, `${q.id} ${optIdx}-varianti bo'sh`);
        assert.ok(opt.length <= 100, `${q.id} ${optIdx}-varianti 100 belgidan oshgan (${opt.length}): ${opt}`);
        assert.ok(!opt.trim().startsWith("*"), `${q.id} variantida * belgisi qolib ketgan: ${opt}`);
        if (opt !== "B. Axmedov") {
          assert.ok(
            !/^[A-Da-dsS][.)]\s*/.test(opt.trim()),
            `${q.id} variantida A/B/C/D prefiksi qolib ketgan: ${opt}`
          );
        }
      });

      const uniqueOptions = new Set(q.options);
      assert.strictEqual(uniqueOptions.size, 4, `${q.id} variantlarida dublikat bor`);

      assert.ok(q.correctOptionId >= 0 && q.correctOptionId <= 3, `${q.id} noto'g'ri indeks`);
      assert.strictEqual(q.timeLimitSeconds, 20, `${q.id} vaqti 20 soniya bo'lishi shart`);
    });
  });

  // Tanlanma kalitlar tekshiruvi (PDF #1..#80)
  assert.strictEqual(dh1Quiz.questions[0].options[dh1Quiz.questions[0].correctOptionId], "610 y");
  assert.strictEqual(dh1Quiz.questions[9].options[dh1Quiz.questions[9].correctOptionId], "Injil");
  assert.strictEqual(dh2Quiz.questions[17].options[dh2Quiz.questions[17].correctOptionId], "2021-yil 4-may");
  assert.strictEqual(dh2Quiz.questions[18].options[dh2Quiz.questions[18].correctOptionId], "1054-yilda");
  assert.strictEqual(dh3Quiz.questions[16].options[dh3Quiz.questions[16].correctOptionId], "Ibodatxona");
  assert.strictEqual(
    dh4Quiz.questions[19].options[dh4Quiz.questions[19].correctOptionId],
    "Nabiy avvalgi shariatni davom ettiradi, rasulga yangi shariat tushadi."
  );

  console.log("  ✅ Barcha 80 ta savol 4 tadan unikal variant, 20s taymer va Telegram cheklovlariga to'liq mos");

  // -----------------------------------------------------------------
  // 3. Aralashtirish (Shuffle) xavfsizligi
  // -----------------------------------------------------------------
  console.log("\n3. Dinamik aralashtirishda to'g'ri javoblar saqlanishi...");

  for (const quiz of allDhQuizzes) {
    const prepared = prepareSessionQuiz(quiz);
    assert.strictEqual(prepared.questions.length, 20);
    prepared.questions.forEach((q) => {
      const orig = quiz.questions.find((o) => o.id === q.id)!;
      assert.strictEqual(
        q.options[q.correctOptionId],
        orig.options[orig.correctOptionId],
        `${q.id} aralashtirilganda to'g'ri javob o'zgardi`
      );
    });
  }
  console.log("  ✅ Barcha 4 ta quiz aralashganda ham javob indekslari to'g'ri saqlandi");

  // -----------------------------------------------------------------
  // 4. Test yaratuvchisi formati va QuizManager sessiyasi
  // -----------------------------------------------------------------
  console.log("\n4. QuizManager sessiyasi, «Diyorbek Hasanov (@Dr_xasanov07)» formati va inline query...");

  assert.strictEqual(
    formatQuizAuthorHtml("Diyorbek Hasanov (@Dr_xasanov07)"),
    'Diyorbek Hasanov (<a href="https://t.me/Dr_xasanov07">@Dr_xasanov07</a>)'
  );
  assert.strictEqual(
    formatQuizAuthorHtml("@Dr_xasanov07"),
    '<a href="https://t.me/Dr_xasanov07">@Dr_xasanov07</a>'
  );
  assert.strictEqual(
    formatQuizAuthorHtml("Diyorbek Hasanov"),
    "Diyorbek Hasanov"
  );
  assert.strictEqual(
    formatQuizAuthorHtml(undefined),
    '<a href="https://t.me/diyorbek_jabborov">@diyorbek_jabborov</a>'
  );

  const testChatId = -100778899;
  const storagePath = "./temp_dh_test_sessions.json";
  const sessionStorage = new JsonFileSessionStorage(storagePath);
  const quizManager = new QuizManager(sessionStorage);

  const sentPolls: Array<{ chatId: number; openPeriod: number; optionsCount: number }> = [];
  const sentMessages: Array<{ text: string }> = [];

  const mockApi: TelegramApiSender = {
    async sendMessage(_chatId, text) {
      sentMessages.push({ text });
      return { message_id: 100, text };
    },
    async sendPoll(chatId, question, options, params) {
      sentPolls.push({
        chatId,
        openPeriod: params?.open_period ?? 0,
        optionsCount: options.length,
      });
      return {
        message_id: 200 + sentPolls.length,
        poll: {
          id: `dh_poll_${sentPolls.length}`,
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
    async stopPoll() {
      return {
        id: "dh_poll",
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

  try {
    const startRes = await quizManager.startQuiz(testChatId, dh1Quiz, mockApi);
    assert.strictEqual(startRes.success, true);
    await quizManager.sendNextQuestion(testChatId, mockApi);
    assert.strictEqual(sentPolls.length, 1);
    assert.strictEqual(sentPolls[0].openPeriod, 20);
    assert.strictEqual(sentPolls[0].optionsCount, 4);

    const mockDhSession: QuizSession = {
      sessionId: "dh_mock_s1",
      chatId: testChatId,
      quiz: dh1Quiz,
      status: "finishing",
      currentQuestionIndex: 19,
      currentPollId: null,
      currentPollMessageId: null,
      questionStartTime: 0,
      timer: null,
      answeredUsers: new Set(),
      participants: new Map([
        [
          111,
          {
            userId: 111,
            firstName: "Ali",
            score: 18,
            totalTimeMs: 42000,
            answersCount: 20,
          },
        ],
      ]),
      consecutiveUnansweredCount: 0,
      currentQuestionAnswered: true,
      version: 1,
    };

    const dhMsgs = quizManager.formatLeaderboardMessages(mockDhSession, quizManager.getLeaderboard(testChatId).length ? quizManager.getLeaderboard(testChatId) : [
      { userId: 111, firstName: "Ali", score: 18, totalTimeMs: 42000, answersCount: 20 },
    ]);
    assert.ok(
      dhMsgs[0].includes('Test yaratuvchisi: Diyorbek Hasanov (<a href="https://t.me/Dr_xasanov07">@Dr_xasanov07</a>)'),
      "DH1 natijasida 'Test yaratuvchisi: Diyorbek Hasanov (@Dr_xasanov07)' havolasi bilan chiqishi shart"
    );

    const d6Msgs = quizManager.formatLeaderboardMessages({ ...mockDhSession, quiz: d6Quiz }, []);
    assert.ok(
      d6Msgs[0].includes('Test yaratuvchisi: <a href="https://t.me/Dr_xasanov07">@Dr_xasanov07</a>'),
      "D6 dagi @Dr_xasanov07 formati o'zgarmasligi shart"
    );

    const d1Msgs = quizManager.formatLeaderboardMessages({ ...mockDhSession, quiz: d1Quiz }, []);
    assert.ok(
      d1Msgs[0].includes('Test yaratuvchisi: <a href="https://t.me/diyorbek_jabborov">@diyorbek_jabborov</a>'),
      "D1 dagi @diyorbek_jabborov formati o'zgarmasligi shart"
    );

    // Inline query qidiruvi ("DH")
    let inlineResults: any[] = [];
    const inlineCtx = {
      from: { id: 777001, first_name: "Student" },
      inlineQuery: { id: "iq_dh", from: { id: 777001 }, query: "DH", offset: "" },
      me: { id: 999, username: "jdakimyoquizbot" },
      api: { getChatMember: async () => ({ status: "left" }) },
      answerInlineQuery: async (results: any[]) => {
        inlineResults = results;
        return true;
      },
    };
    await handleInlineQuery(inlineCtx as any);
    assert.deepStrictEqual(
      inlineResults.map((r) => r.id),
      ["DH1", "DH2", "DH3", "DH4"]
    );

    await quizManager.stopQuiz(testChatId, mockApi);
  } finally {
    if (fs.existsSync(storagePath)) {
      fs.unlinkSync(storagePath);
    }
  }

  console.log("  ✅ DH1–DH4 sessiyasi, «Diyorbek Hasanov (@Dr_xasanov07)» va inline query 100% ishladi");
  console.log("\n==================================================================");
  console.log("🎉 BARCHA DH1–DH4 TESTLARI (4/4) MUVAFFAQIYATLI O'TDI!");
  console.log("==================================================================");
}

runDhTests().catch((err) => {
  console.error("❌ DH1–DH4 testlarida xatolik:", err);
  process.exit(1);
});
