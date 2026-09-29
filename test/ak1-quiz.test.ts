import assert from "node:assert";
import fs from "node:fs";
import path from "node:path";
import { ak1Quiz } from "../src/quiz/ak1Questions.js";
import { aminoAcidsQuiz, getQuizById, allQuizzes } from "../src/quiz/questions.js";
import { QuizManager, prepareSessionQuiz, TelegramApiSender } from "../src/quiz/quizManager.js";
import { JsonFileSessionStorage } from "../src/quiz/sessionStorage.js";

async function runAk1Tests() {
  console.log("==================================================================");
  console.log("🧪 AK1 (AMINOKISLOTALAR STRUKTURASI) QUIZ VA RASM TESTLARI");
  console.log("==================================================================");

  // -----------------------------------------------------------------
  // 1. Quiz Ma'lumotlari va Registratsiyasi
  // -----------------------------------------------------------------
  console.log("\n1. AK1 quizi konfiguratsiyasi va registratsiyasi...");
  assert.strictEqual(ak1Quiz.id, "AK1");
  assert.strictEqual(ak1Quiz.groupOnly, true, "Quiz faqat guruhlar uchun bo'lishi shart");
  assert.strictEqual(ak1Quiz.shuffle, true, "Savollar va variantlar har sessiyada aralashtirilishi shart");
  assert.strictEqual(ak1Quiz.source, "329–330-betlardagi 17-jadval");
  assert.strictEqual(ak1Quiz.questions.length, 21, "Savollar soni aynan 21 ta bo'lishi shart");

  // getQuizById orqali topilishi
  const byAk1 = getQuizById("AK1");
  const byAk1Lower = getQuizById("ak1");
  const byQuizAk1 = getQuizById("quiz_AK1");
  const byStartAk1 = getQuizById("start_ak1");

  assert.ok(byAk1 && byAk1.id === "AK1");
  assert.ok(byAk1Lower && byAk1Lower.id === "AK1");
  assert.ok(byQuizAk1 && byQuizAk1.id === "AK1");
  assert.ok(byStartAk1 && byStartAk1.id === "AK1");

  // Mavjud /quiz_amino_acids quizi o'zgarmaganligi tekshiruvi
  assert.strictEqual(aminoAcidsQuiz.id, "amino_acids");
  assert.strictEqual(aminoAcidsQuiz.questions.length, 21);
  const byAmino = getQuizById("amino_acids");
  assert.ok(byAmino && byAmino.id === "amino_acids");
  console.log("  ✅ AK1 quizi ro'yxatga olindi va mavjud amino_acids buzilmadi");

  // -----------------------------------------------------------------
  // 2. 21 ta Rasm, Savollar va Variantlarning Butunligi
  // -----------------------------------------------------------------
  console.log("\n2. 21 ta rasm, savollar, variantlar va to'g'ri javoblar tekshiruvi...");

  const expectedSubstances = [
    { num: 1, name: "Glitsin", file: "ak_1.png" },
    { num: 2, name: "Alanin", file: "ak_2.png" },
    { num: 3, name: "Valin", file: "ak_3.png" },
    { num: 4, name: "Leysin", file: "ak_4.png" },
    { num: 5, name: "Izoleysin", file: "ak_5.png" },
    { num: 6, name: "Asparagin kislota", file: "ak_6.png" },
    { num: 7, name: "Glutamin kislota", file: "ak_7.png" },
    { num: 8, name: "Ornitin", file: "ak_8.png" },
    { num: 9, name: "Lizin", file: "ak_9.png" },
    { num: 10, name: "Serin", file: "ak_10.png" },
    { num: 11, name: "Treonin", file: "ak_11.png" },
    { num: 12, name: "Sistein", file: "ak_12.png" },
    { num: 13, name: "Sistin", file: "ak_13.png" },
    { num: 14, name: "Metionin", file: "ak_14.png" },
    { num: 15, name: "Fenilalanin", file: "ak_15.png" },
    { num: 16, name: "Tirozin", file: "ak_16.png" },
    { num: 17, name: "Triptofan", file: "ak_17.png" },
    { num: 18, name: "Prolin", file: "ak_18.png" },
    { num: 19, name: "Oksiprolin", file: "ak_19.png" },
    { num: 20, name: "Gistidin", file: "ak_20.png" },
    { num: 21, name: "Arginin", file: "ak_21.png" },
  ];

  for (let i = 0; i < ak1Quiz.questions.length; i++) {
    const q = ak1Quiz.questions[i];
    const exp = expectedSubstances[i];

    assert.strictEqual(q.question, "Rasmdagi aminokislota qaysi?");
    assert.strictEqual(q.timeLimitSeconds, 30, "Har bir pollga aynan 30 soniya berilishi shart");
    assert.strictEqual(q.options.length, 4, "Har savolda 4 ta variant bo'lishi shart");
    assert.ok(q.correctOptionId >= 0 && q.correctOptionId < 4);

    const correctName = q.options[q.correctOptionId];
    assert.strictEqual(correctName, exp.name, `${i + 1}-savolning to'g'ri javobi ${exp.name} bo'lishi shart`);

    // Rasm mavjudligi va o'lchami tekshiruvi
    assert.ok(q.imagePath, `${i + 1}-savolda imagePath bo'lishi shart`);
    assert.ok(fs.existsSync(q.imagePath), `Rasm fayli diskda mavjud bo'lishi shart: ${q.imagePath}`);
    const stats = fs.statSync(q.imagePath);
    assert.ok(stats.size > 1000, `Rasm fayli bo'sh bo'lmasligi shart (hajmi: ${stats.size} bayt)`);
    assert.ok(q.imagePath.endsWith(exp.file));
  }
  console.log("  ✅ 21 ta savol, variantlar, javob indekslari va rasm fayllari mavjudligi tekshirildi");

  // -----------------------------------------------------------------
  // 3. O'xshash Juftliklar Bog'lanishi va Adashmaslik Sinovi
  // -----------------------------------------------------------------
  console.log("\n3. Nozik juftliklar (leysin/izoleysin, sistein/sistin, asparagin/glutamin, prolin/oksiprolin, ornitin/lizin)...");

  // 3.1. Leysin vs Izoleysin
  const qLeysin = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Leysin")!;
  const qIzoleysin = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Izoleysin")!;
  assert.ok(qLeysin.options.includes("Izoleysin"), "Leysin variantlarida Izoleysin bo'lishi kerak");
  assert.ok(qIzoleysin.options.includes("Leysin"), "Izoleysin variantlarida Leysin bo'lishi kerak");
  assert.notStrictEqual(qLeysin.imagePath, qIzoleysin.imagePath);

  // 3.2. Sistein vs Sistin
  const qSistein = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Sistein")!;
  const qSistin = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Sistin")!;
  assert.ok(qSistein.options.includes("Sistin"), "Sistein variantlarida Sistin bo'lishi kerak");
  assert.ok(qSistin.options.includes("Sistein"), "Sistin variantlarida Sistein bo'lishi kerak");
  assert.notStrictEqual(qSistein.imagePath, qSistin.imagePath);

  // 3.3. Asparagin kislota vs Glutamin kislota
  const qAsp = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Asparagin kislota")!;
  const qGlu = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Glutamin kislota")!;
  assert.ok(qAsp.options.includes("Glutamin kislota"));
  assert.ok(qGlu.options.includes("Asparagin kislota"));
  assert.notStrictEqual(qAsp.imagePath, qGlu.imagePath);

  // 3.4. Prolin vs Oksiprolin
  const qPro = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Prolin")!;
  const qOxi = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Oksiprolin")!;
  assert.ok(qPro.options.includes("Oksiprolin"));
  assert.ok(qOxi.options.includes("Prolin"));
  assert.notStrictEqual(qPro.imagePath, qOxi.imagePath);

  // 3.5. Ornitin vs Lizin
  const qOrn = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Ornitin")!;
  const qLiz = ak1Quiz.questions.find((q) => q.options[q.correctOptionId] === "Lizin")!;
  assert.ok(qOrn.options.includes("Lizin"));
  assert.ok(qLiz.options.includes("Ornitin"));
  assert.notStrictEqual(qOrn.imagePath, qLiz.imagePath);

  console.log("  ✅ Nozik juftliklar variantlarda bor va alohida rasm fayllariga bog'langan");

  // -----------------------------------------------------------------
  // 4. Variantlar va Savollar Aralashuvi (Fisher-Yates) Sinovi
  // -----------------------------------------------------------------
  console.log("\n4. Savollar va variantlar har sessiyada aralashishi...");

  const prepared = prepareSessionQuiz(ak1Quiz);
  assert.strictEqual(prepared.questions.length, 21);
  assert.notStrictEqual(prepared, ak1Quiz, "Asl ak1Quiz o'zgarmas (immutable) bo'lishi shart");

  // Har bir savolning to'g'ri javob matni saqlanganligini tekshirish
  for (const prepQ of prepared.questions) {
    const origQ = ak1Quiz.questions.find((q) => q.id === prepQ.id)!;
    const origCorrectText = origQ.options[origQ.correctOptionId];
    const newCorrectText = prepQ.options[prepQ.correctOptionId];
    assert.strictEqual(newCorrectText, origCorrectText, "Variantlar aralashganda to'g'ri javob matni saqlanishi shart");
  }
  console.log("  ✅ Savollar va javob variantlari to'g'ri indekslar bilan xavfsiz aralashdi");

  // -----------------------------------------------------------------
  // 5. QuizManager: Avval Rasm, So'ng Poll Chiqishi va Taymer Tartibi
  // -----------------------------------------------------------------
  console.log("\n5. QuizManager: Avval [1/21] rasm, so'ng poll va 30s taymer...");

  const sentEvents: Array<{ type: "photo" | "poll" | "message"; data: any }> = [];
  let pollIdCounter = 1;

  const mockApi: TelegramApiSender = {
    async sendPhoto(chatId, photo, other) {
      sentEvents.push({ type: "photo", data: { chatId, photo, other } });
      return { message_id: 1000 + sentEvents.length };
    },
    async sendPoll(chatId, question, options, other) {
      sentEvents.push({ type: "poll", data: { chatId, question, options, other } });
      return { message_id: 2000 + sentEvents.length, poll: { id: `mock_ak1_poll_${pollIdCounter++}` } };
    },
    async stopPoll(chatId, messageId) {
      return {};
    },
    async sendMessage(chatId, text, other) {
      sentEvents.push({ type: "message", data: { chatId, text, other } });
      return { message_id: 3000 + sentEvents.length };
    },
  };

  const tempStoragePath = path.resolve(process.cwd(), "data", `test_ak1_${Date.now()}.json`);
  const storage = new JsonFileSessionStorage(tempStoragePath);
  const manager = new QuizManager(storage);
  const testChatId = -100998877;

  try {
    // Quizni boshlaymiz (aralashmasdan ketma-ket chiqishini ko'rish uchun no-shuffle qilib sinaymiz)
    const unshuffledAk1 = { ...ak1Quiz, shuffle: false };
    const startRes = await manager.startQuiz(testChatId, unshuffledAk1, mockApi);
    assert.strictEqual(startRes.success, true);
    assert.strictEqual(sentEvents[0].type, "message", "Start e'loni yuborilishi shart");

    // 1-savolni darhol yuboramiz (taymerni kutmasdan)
    await manager.sendNextQuestion(testChatId, mockApi);

    // Birinchi savol yuborildi:
    // 1-hodisa (index 1): sendPhoto bo'lishi shart
    // 2-hodisa (index 2): sendPoll bo'lishi shart
    assert.strictEqual(sentEvents.length, 3);
    assert.strictEqual(sentEvents[1].type, "photo");
    assert.strictEqual(sentEvents[1].data.other?.caption, "[1/21]");
    const photo1Path = (sentEvents[1].data.photo.fileData || sentEvents[1].data.photo).toString();
    assert.ok(photo1Path.includes("ak_1.png"));

    assert.strictEqual(sentEvents[2].type, "poll");
    assert.strictEqual(sentEvents[2].data.question, "[1/21] Rasmdagi aminokislota qaysi?");
    assert.strictEqual(sentEvents[2].data.other?.open_period, 30);

    const session = manager.getSession(testChatId)!;
    assert.strictEqual(session.currentQuestionIndex, 0);
    assert.strictEqual(session.quiz.questions[0].timeLimitSeconds, 30);
    console.log("  ✅ Avval [1/21] rasm, darhol ortidan 30s lik poll muvaffaqiyatli chiqdi");

    // -----------------------------------------------------------------
    // 6. Rasm Yuborishda Xatolik Yuz Berganda Xavfsiz Pauza va Resume
    // -----------------------------------------------------------------
    console.log("\n6. Rasm yuborishda xatolik: pollga o'tmasdan pauzaga o'tish va retry...");

    // Keyingi savolda sendPhoto xato beradigan API simulyatsiyasi
    let failPhotoOnce = true;
    const failPhotoApi: TelegramApiSender = {
      async sendPhoto(chatId, photo, other) {
        if (failPhotoOnce) {
          failPhotoOnce = false;
          throw new Error("Telegram API 500: Photo upload failed (Simulated)");
        }
        sentEvents.push({ type: "photo", data: { chatId, photo, other } });
        return { message_id: 1050 };
      },
      async sendPoll(chatId, question, options, other) {
        sentEvents.push({ type: "poll", data: { chatId, question, options, other } });
        return { message_id: 2050, poll: { id: `poll_after_resume_${pollIdCounter++}` } };
      },
      async stopPoll() {
        return {};
      },
      async sendMessage(chatId, text, other) {
        sentEvents.push({ type: "message", data: { chatId, text, other } });
        return { message_id: 3050 };
      },
    };

    // 2-savolga o'tamiz, ammo rasmda xato beradi!
    const eventsCountBefore = sentEvents.length;
    await manager.sendNextQuestion(testChatId, failPhotoApi);

    // Holatni tekshiramiz:
    const pausedSession = manager.getSession(testChatId)!;
    assert.strictEqual(pausedSession.status, "paused", "Rasm xatosidan so'ng sessiya pauza holatiga o'tishi shart");
    // Indeks orqaga qaytarilgan bo'lishi shart (1 ga oshib, keyin 0 ga qaytgan)
    assert.strictEqual(pausedSession.currentQuestionIndex, 0);

    // Hech qanday poll yuborilmagan bo'lishi shart!
    const newEvents = sentEvents.slice(eventsCountBefore);
    const pollEvent = newEvents.find((e) => e.type === "poll");
    assert.strictEqual(pollEvent, undefined, "Rasm xato bersa, keyingi poll aslo yuborilmasligi shart");

    // Xatolik xabari va resume tugmasi yuborilgan bo'lishi shart
    const errMsgEvent = newEvents.find((e) => e.type === "message");
    assert.ok(errMsgEvent);
    assert.ok(errMsgEvent.data.text.includes("Savol rasmini yuborishda vaqtinchalik xatolik yuz berdi"));
    assert.ok(errMsgEvent.data.other?.reply_markup?.inline_keyboard);
    console.log("  ✅ Rasm xato berganda poll ochilmay, sessiya xavfsiz pauzaga qo'yildi");

    // API da sendPhoto bo'lmasa ham rasm talab qiluvchi savol rasmsiz ochilmasin.
    const noPhotoApi: TelegramApiSender = {
      sendPoll: failPhotoApi.sendPoll,
      stopPoll: failPhotoApi.stopPoll,
      sendMessage: failPhotoApi.sendMessage,
    };
    const noPhotoResume = await manager.resumeQuiz(testChatId, noPhotoApi);
    assert.strictEqual(noPhotoResume.success, true);
    const eventsBeforeMissingPhoto = sentEvents.length;
    await manager.sendNextQuestion(testChatId, noPhotoApi);
    assert.strictEqual(manager.getSession(testChatId)?.status, "paused");
    assert.strictEqual(manager.getSession(testChatId)?.currentQuestionIndex, 0);
    assert.ok(!sentEvents.slice(eventsBeforeMissingPhoto).some((e) => e.type === "poll"));

    // Endi pauzadan davom ettiramiz: aynan shu 2-savol va uning rasmi qayta yuborilishi kerak!
    const resumeRes = await manager.resumeQuiz(testChatId, failPhotoApi);
    assert.strictEqual(resumeRes.success, true);

    // Resume taymeri o'tgach sendNextQuestion chaqiriladi:
    await manager.sendNextQuestion(testChatId, failPhotoApi);

    const resumedSession = manager.getSession(testChatId)!;
    assert.strictEqual(resumedSession.currentQuestionIndex, 1, "Aynan 2-savol (index 1) ga o'tgan bo'lishi kerak");
    const lastPhoto = sentEvents[sentEvents.length - 2];
    const lastPoll = sentEvents[sentEvents.length - 1];

    assert.strictEqual(lastPhoto.type, "photo");
    assert.strictEqual(lastPhoto.data.other?.caption, "[2/21]");
    const photo2Path = (lastPhoto.data.photo.fileData || lastPhoto.data.photo).toString();
    assert.ok(photo2Path.includes("ak_2.png"), "Aynan 2-savol rasmi (ak_2.png) yuborilishi shart");

    assert.strictEqual(lastPoll.type, "poll");
    assert.strictEqual(lastPoll.data.question, "[2/21] Rasmdagi aminokislota qaysi?");
    console.log("  ✅ Pauzadan davom ettirilganda aynan kerakli rasm ([2/21]) va savol chiqdi");

    // -----------------------------------------------------------------
    // 7. Yakuniy Reyting Formatlash Sinovi (Muallif va Manba)
    // -----------------------------------------------------------------
    console.log("\n7. Yakuniy reyting xabari formati va muallif...");
    const leaderboardMsgs = manager.formatLeaderboardMessages(session, [
      { userId: 101, firstName: "Kimyogar", score: 20, totalTimeMs: 15400, answersCount: 21 },
    ]);
    assert.strictEqual(leaderboardMsgs.length, 1);
    assert.ok(leaderboardMsgs[0].includes("@diyorbek_jabborov"), "Muallif @diyorbek_jabborov ko'rinishi shart");
    assert.ok(leaderboardMsgs[0].includes("329–330-betlardagi 17-jadval"), "Manba ko'rinishi shart");
    console.log("  ✅ Yakuniy reyting xabarida muallif @diyorbek_jabborov va manba to'g'ri chiqdi");

  } finally {
    manager.stopQuiz(testChatId);
    if (fs.existsSync(tempStoragePath)) {
      try {
        fs.unlinkSync(tempStoragePath);
      } catch {}
    }
  }

  console.log("\n==================================================================");
  console.log("🎉 AK1 KOD TESTLARI MUVAFFAQIYATLI O'TDI (KIMYOVIY CHIZMALAR ALOHIDA KO'RIB CHIQILADI)");
  console.log("==================================================================");
}

runAk1Tests().catch((err) => {
  console.error("❌ AK1 testlarida xatolik:", err);
  process.exit(1);
});
