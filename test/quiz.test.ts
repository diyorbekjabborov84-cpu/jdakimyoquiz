import assert from "node:assert";
import { sampleChemistryQuiz } from "../src/quiz/questions.js";
import { QuizManager, TelegramApiSender, escapeHtml } from "../src/quiz/quizManager.js";
import { isGroupAdmin } from "../src/bot/guards/adminGuard.js";

// Mock Telegram API Sender
class MockTelegramApi implements TelegramApiSender {
  public sentMessages: Array<{ chatId: number | string; text: string }> = [];
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
    this.sentMessages.push({ chatId, text });
    return { message_id: this.nextMessageId++, text };
  }
}

async function runQuizTests() {
  console.log("🧪 2-BOSQICH: QUIZ TIZIMI TESTLARI BOSHLANDI...\n");

  // TEST 1: Savollar to'plami va talablar (21 ta aminokislota)
  console.log("Test 1: 21 ta aminokislota savollari to'plami va 4 ta unikal variant tekshiruvi...");
  assert.strictEqual(
    sampleChemistryQuiz.questions.length,
    21,
    "Aynan 21 ta aminokislota savoli bo'lishi kerak"
  );

  const expectedTemperatures: Record<string, string> = {
    Glitsin: "292 °C",
    Alanin: "297 °C",
    Valin: "315 °C",
    Leysin: "337 °C",
    Izoleysin: "284 °C",
    "Asparagin kislota": "270 °C",
    "Glutamin kislota": "249 °C",
    Ornitin: "140 °C",
    Lizin: "224 °C",
    Serin: "228 °C",
    Treonin: "253 °C",
    Sistein: "178 °C",
    Sistin: "260 °C",
    Metionin: "283 °C",
    Fenilalanin: "275 °C",
    Tirozin: "344 °C",
    Triptofan: "382 °C",
    Prolin: "299 °C",
    Oksiprolin: "270 °C",
    Gistidin: "277 °C",
    Arginin: "238 °C",
  };

  for (const q of sampleChemistryQuiz.questions) {
    assert.ok(q.id, "Har bir savol id ga ega bo'lishi kerak");
    assert.ok(q.question.includes("suyuqlanish temperaturasi"), "Savol matni to'g'ri bo'lishi kerak");
    assert.strictEqual(q.options.length, 4, "Har savolda aynan 4 ta variant bo'lishi kerak");
    assert.strictEqual(
      new Set(q.options).size,
      4,
      `Savol variantlari bir-biridan farq qilishi kerak: ${q.question}`
    );
    assert.strictEqual(q.timeLimitSeconds, 20, "Har bir savolga 20 soniya vaqt bo'lishi kerak");
    assert.ok(
      q.correctOptionId >= 0 && q.correctOptionId < 4,
      "To'g'ri javob indeksi 0-3 oralig'ida bo'lishi kerak"
    );

    // Kislota nomi va uning to'g'ri temperaturasi mosligini tekshirish
    let matchedName = "";
    for (const name of Object.keys(expectedTemperatures)) {
      if (q.question.includes(name)) {
        matchedName = name;
        break;
      }
    }
    assert.ok(matchedName.length > 0, `Noma'lum aminokislota savoli: ${q.question}`);
    const expectedTemp = expectedTemperatures[matchedName];
    const actualCorrectOption = q.options[q.correctOptionId];
    assert.strictEqual(
      actualCorrectOption,
      expectedTemp,
      `${matchedName} uchun to'g'ri temperatura ${expectedTemp} bo'lishi kerak, lekin ${actualCorrectOption} ko'rsatilgan`
    );
  }
  console.log(`✅ Test 1 muvaffaqiyatli o'tdi. (21 ta aminokislota savoli va to'g'ri javoblari 100% tasdiqlandi)\n`);

  // TEST 2: HTML Escape xavfsizligi
  console.log("Test 2: Foydalanuvchi ismlari va matnlarni HTML uchun xavfsiz escape qilish...");
  const rawXss = 'Ali <script>alert("xss")</script> & O\'g\'li';
  const escaped = escapeHtml(rawXss);
  assert.strictEqual(
    escaped,
    "Ali &lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt; &amp; O&#039;g&#039;li",
    "Maxsus belgilar to'liq escape qilinishi kerak"
  );
  console.log("✅ Test 2 muvaffaqiyatli o'tdi.\n");

  // TEST 3: Guruhda quiz boshlash va faqat bitta faol quiz bo'lishini tekshirish
  console.log("Test 3: Guruhda bitta faol quiz qoidasi...");
  const qm = new QuizManager();
  const mockApi = new MockTelegramApi();
  const group1Id = -10012345;

  const start1 = await qm.startQuiz(group1Id, sampleChemistryQuiz, mockApi);
  assert.strictEqual(start1.success, true, "1-marta quiz boshlanishi kerak");
  assert.strictEqual(qm.isQuizRunning(group1Id), true, "Quiz faol holatda bo'lishi kerak");

  // Ikkinchi marta boshlashga urinish rad etilishi kerak
  const start2 = await qm.startQuiz(group1Id, sampleChemistryQuiz, mockApi);
  assert.strictEqual(start2.success, false, "Allaqachon faol quiz bo'lsa ikkinchisi boshlanmasligi kerak");
  assert.ok(start2.message.includes("faol quiz davom etmoqda"));
  console.log("✅ Test 3 muvaffaqiyatli o'tdi.\n");

  // TEST 4: Ikki alohida guruh bir vaqtda mustaqil quiz o'tkaza olishi
  console.log("Test 4: Ikki guruhda bir vaqtda parallel quiz ishlashi...");
  const group2Id = -10098765;
  const startGroup2 = await qm.startQuiz(group2Id, sampleChemistryQuiz, mockApi);
  assert.strictEqual(startGroup2.success, true, "2-guruhda ham parallel quiz boshlanishi kerak");
  assert.strictEqual(qm.isQuizRunning(group1Id), true, "1-guruh faol");
  assert.strictEqual(qm.isQuizRunning(group2Id), true, "2-guruh faol");
  console.log("✅ Test 4 muvaffaqiyatli o'tdi.\n");

  // TEST 5: Savollarning Telegram Quiz Poll shaklida yuborilishi (yangi Bot API correct_option_ids)
  console.log("Test 5: Telegram Quiz Poll formatini va yangi correct_option_ids maydonini tekshirish...");
  await qm.sendNextQuestion(group1Id, mockApi);
  const sentPoll = mockApi.sentPolls[mockApi.sentPolls.length - 1];
  assert.ok(sentPoll, "Poll yuborilgan bo'lishi kerak");
  assert.strictEqual(sentPoll.chatId, group1Id);
  assert.strictEqual(sentPoll.other?.type, "quiz", "Poll turi 'quiz' bo'lishi kerak");
  assert.strictEqual(sentPoll.other?.is_anonymous, false, "Poll is_anonymous: false bo'lishi kerak");
  assert.deepStrictEqual(
    sentPoll.other?.correct_option_ids,
    [sampleChemistryQuiz.questions[0].correctOptionId],
    "correct_option_ids array bo'lib uzatilishi kerak"
  );
  assert.strictEqual(
    sentPoll.other?.correct_option_id,
    undefined,
    "Eski correct_option_id maydoni endi uzatilmasligi kerak"
  );
  assert.strictEqual(sentPoll.other?.open_period, 20, "open_period 20 soniya bo'lishi kerak");
  console.log("✅ Test 5 muvaffaqiyatli o'tdi.\n");

  // TEST 6: Takroriy javoblarni elash (Deduplication)
  console.log("Test 6: Takroriy javob ballni 2 marta oshirmasligini tekshirish...");
  const pollId = sentPoll.pollId;
  const correctOption = sampleChemistryQuiz.questions[0].correctOptionId;

  // 1-marta ovoz berish
  const answer1 = qm.handlePollAnswer({
    pollId,
    user: { id: 101, first_name: "Ali <Tester>", username: "ali_user" },
    optionIds: [correctOption],
  });
  assert.strictEqual(answer1, true, "Birinchi javob qabul qilinishi kerak");

  // 2-marta takroriy ovoz berish (Telegram duplicate update simulyatsiyasi)
  const answerDuplicate = qm.handlePollAnswer({
    pollId,
    user: { id: 101, first_name: "Ali <Tester>", username: "ali_user" },
    optionIds: [correctOption],
  });
  assert.strictEqual(answerDuplicate, false, "Takroriy javob rad etilishi kerak");

  const session1 = qm.getSession(group1Id);
  const aliScore = session1?.participants.get(101);
  assert.strictEqual(aliScore?.score, 1, "Ali'ning balli faqat 1 marta oshishi kerak");
  assert.strictEqual(aliScore?.answersCount, 1, "Ali'ning javoblari soni 1 bo'lishi kerak");
  console.log("✅ Test 6 muvaffaqiyatli o'tdi.\n");

  // TEST 7: Eski yoki yopilgan savollardan kech kelgan javoblarni rad etish
  console.log("Test 7: Eski yoki yopilgan savoldan kech kelgan javob ballga qo'shilmasligi...");
  // Keyingi savolga o'tamiz (bu avvalgi savolni yopadi)
  await qm.sendNextQuestion(group1Id, mockApi);
  const lateAnswer = qm.handlePollAnswer({
    pollId, // eski pollId
    user: { id: 104, first_name: "Kechikkan Foydalanuvchi" },
    optionIds: [correctOption],
  });
  assert.strictEqual(lateAnswer, false, "Eski savolga kelgan javob rad etilishi kerak");
  const sessionAfterLate = qm.getSession(group1Id);
  assert.strictEqual(
    sessionAfterLate?.participants.has(104),
    false,
    "Kechikkan foydalanuvchi hisoblanmasligi kerak"
  );
  console.log("✅ Test 7 muvaffaqiyatli o'tdi.\n");

  // TEST 8: Bir nechta ishtirokchilar va tay-breyk (Tie-breaking) reytingi
  console.log("Test 8: Ko'p ishtirokchilar balli va vaqt bo'yicha reyting...");
  const poll2 = mockApi.sentPolls[mockApi.sentPolls.length - 1];
  const poll2Correct = sampleChemistryQuiz.questions[1].correctOptionId;

  // Ali va Bobur to'g'ri javob beradi
  qm.handlePollAnswer({
    pollId: poll2.pollId,
    user: { id: 101, first_name: "Ali <Tester>", username: "ali_user" },
    optionIds: [poll2Correct],
  });
  qm.handlePollAnswer({
    pollId: poll2.pollId,
    user: { id: 102, first_name: "Bobur", username: "bobur_user" },
    optionIds: [poll2Correct],
  });
  // Jamshid noto'g'ri javob beradi
  qm.handlePollAnswer({
    pollId: poll2.pollId,
    user: { id: 103, first_name: "Jamshid" },
    optionIds: [(poll2Correct + 1) % 4],
  });

  const session = qm.getSession(group1Id)!;
  // Bobur javob vaqtini qo'lda simulyatsiya qilamiz: Bobur = 5000ms, Ali = 2000ms
  session.participants.get(101)!.totalTimeMs = 2000;
  session.participants.get(102)!.totalTimeMs = 5000;
  session.participants.get(103)!.totalTimeMs = 1500;

  const leaderboard = qm.getLeaderboard(group1Id);
  assert.strictEqual(leaderboard.length, 3, "3 ta ishtirokchi bo'lishi kerak");

  // 1-o'rin: Ali (2 ball, 2.0s)
  assert.strictEqual(leaderboard[0].userId, 101);
  assert.strictEqual(leaderboard[0].score, 2);

  // 2-o'rin: Bobur (1 ball, 5.0s)
  assert.strictEqual(leaderboard[1].userId, 102);
  assert.strictEqual(leaderboard[1].score, 1);

  // 3-o'rin: Jamshid (0 ball)
  assert.strictEqual(leaderboard[2].userId, 103);
  assert.strictEqual(leaderboard[2].score, 0);

  console.log("✅ Test 8 muvaffaqiyatli o'tdi (Ball va vaqt bo'yicha to'g'ri saralandi).\n");

  // TEST 9: Quizni to'xtatish (/stopquiz) va resurslarni tozalash
  console.log("Test 9: /stopquiz bilan sessiyani to'xtatish...");
  await qm.stopQuiz(group1Id, mockApi);
  assert.strictEqual(qm.isQuizRunning(group1Id), false, "Quiz to'xtatilgan bo'lishi kerak");
  assert.ok(mockApi.sentMessages.some((m) => m.text.includes("Quiz to'xtatildi")));

  // 2-guruh hali ham mustaqil ishlab turganini tekshirish
  assert.strictEqual(qm.isQuizRunning(group2Id), true, "2-guruhdagi quiz to'xtamasdan davom etishi kerak");
  await qm.stopQuiz(group2Id, mockApi);
  console.log("✅ Test 9 muvaffaqiyatli o'tdi.\n");

  // TEST 10: Admin guard tekshiruvi
  console.log("Test 10: Guruh admini huquqi guardi...");
  const mockAdminCtx: any = {
    chat: { type: "supergroup", id: -100111 },
    from: { id: 555 },
    getChatMember: async (id: number) => ({ status: "administrator", user: { id } }),
  };
  const isAdmin = await isGroupAdmin(mockAdminCtx);
  assert.strictEqual(isAdmin, true, "Administratorga ruxsat berilishi kerak");

  const mockMemberCtx: any = {
    chat: { type: "supergroup", id: -100111 },
    from: { id: 666 },
    getChatMember: async (id: number) => ({ status: "member", user: { id } }),
  };
  const isMemberAdmin = await isGroupAdmin(mockMemberCtx);
  assert.strictEqual(isMemberAdmin, false, "Oddiy a'zoga quiz boshlash ruxsat berilmasligi kerak");

  const mockPrivateCtx: any = {
    chat: { type: "private", id: 777 },
    from: { id: 777 },
  };
  const isPrivateAdmin = await isGroupAdmin(mockPrivateCtx);
  assert.strictEqual(isPrivateAdmin, false, "Shaxsiy chatda admin huquqi false bo'lishi kerak");

  console.log("✅ Test 10 muvaffaqiyatli o'tdi.\n");

  // TEST 11: 20 savoldan 15 tasiga javob berilib, 7 tasi to'g'ri bo'lgan holat (YOL_XARITASI qoidasi)
  console.log("Test 11: 20 savoldan 15 javob (7 to'g'ri, 8 noto'g'ri, 5 javobsiz) vaqti va 7/20 ko'rinishi...");
  const quiz20Questions = {
    id: "quiz-20-test",
    title: "20 Savolli Sinov Quizi",
    description: "Vaqt qoidasi testi",
    questions: Array.from({ length: 20 }, (_, i) => ({
      id: `q_${i + 1}`,
      question: `Savol ${i + 1}`,
      options: ["A", "B", "C", "D"],
      correctOptionId: 0,
      timeLimitSeconds: 15,
    })),
  };

  const group20Id = -1002020;
  const mockApi20 = new MockTelegramApi();
  const qm20 = new QuizManager();

  await qm20.startQuiz(group20Id, quiz20Questions, mockApi20);

  // 1-savoldan 20-savolgacha o'tkazamiz
  let totalCalculatedTimeMs = 0;
  for (let i = 0; i < 20; i++) {
    await qm20.sendNextQuestion(group20Id, mockApi20);
    const lastPoll = mockApi20.sentPolls[mockApi20.sentPolls.length - 1];

    if (i < 15) {
      // 15 ta savolga javob beriladi
      const isCorrect = i < 7; // dastlabki 7 tasi to'g'ri, keyingi 8 tasi noto'g'ri
      const chosenOption = isCorrect ? 0 : 1;
      const simulatedTimeMs = (i + 1) * 1000; // Har bir javob uchun 1s, 2s, ... 15s

      // pollToSession xaritasidagi startTime ni o'zgartirib, simulyatsiya qilingan javob vaqtini beramiz
      const pollInfo = (qm20 as any).pollToSession.get(lastPoll.pollId);
      if (pollInfo) {
        pollInfo.startTime = Date.now() - simulatedTimeMs;
      }

      qm20.handlePollAnswer({
        pollId: lastPoll.pollId,
        user: { id: 777, first_name: "Test Foydalanuvchi", username: "tester777" },
        optionIds: [chosenOption],
      });

      totalCalculatedTimeMs += simulatedTimeMs;
    } else {
      // 5 ta savol (16-20) JAVOBSIZ QOLADI (hech qanday javob bosilmaydi)
    }
  }

  const leaderboard20 = qm20.getLeaderboard(group20Id);
  assert.strictEqual(leaderboard20.length, 1, "Bitta ishtirokchi bo'lishi kerak");
  const participant = leaderboard20[0];

  assert.strictEqual(participant.score, 7, "To'g'ri javoblar soni 7 bo'lishi kerak");
  assert.strictEqual(participant.answersCount, 15, "Bosilgan javoblar soni 15 bo'lishi kerak");
  // Date.now() ketma-ket chaqirilgani uchun har javobda bir necha ms farq bo'lishi mumkin.
  // 100 ms tolerans 5 ta javobsiz savolning 15 soniyalik vaqtini yashira olmaydi.
  assert.ok(
    Math.abs(participant.totalTimeMs - totalCalculatedTimeMs) <= 100,
    "Faqat bosilgan 15 ta javobning vaqti yig'ilishi kerak (javobsiz 5 ta savol vaqti qo'shilmaydi)"
  );

  // Quiz yakunlanadi (oxirgi savoldan so'ng finishQuiz chaqiriladi)
  await qm20.sendNextQuestion(group20Id, mockApi20);

  const finalMsg20 = mockApi20.sentMessages[mockApi20.sentMessages.length - 1].text;
  assert.ok(
    finalMsg20.includes("7/20 ball"),
    `Natija 7/20 bo'lishi kerak (savollar soni 20 ta). Xabar: ${finalMsg20}`
  );
  assert.ok(
    finalMsg20.includes("jami javob vaqti:"),
    `Xabarda 'jami javob vaqti' ko'rsatilishi kerak. Xabar: ${finalMsg20}`
  );

  console.log("✅ Test 11 muvaffaqiyatli o'tdi (7/20 ball va faqat 15 ta javob vaqti hisoblandi).\n");

  console.log("🎉 BARCHA 2-BOSQICH YANGILANGAN TESTLARI MUVAFFAQIYATLI O'TDI!");
}

runQuizTests().catch((err) => {
  console.error("❌ Testda xatolik:", err);
  process.exit(1);
});
