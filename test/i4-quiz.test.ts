import assert from "node:assert";
import fs from "node:fs";
import {
  getAllQuizzes,
  getQuizById,
  i4Quiz1,
  i4Quiz2,
  i4Quiz3,
} from "../src/quiz/questions.js";
import {
  prepareSessionQuiz,
  quizManager,
  QuizManager,
  TelegramApiSender,
} from "../src/quiz/quizManager.js";

async function runI4Tests() {
  console.log("\n==================================================================");
  console.log("🧪 SLAYD-I-4 (ALKENLAR VA RASMLI SAVOLLAR) QUIZ TESTLARI");
  console.log("==================================================================");

  // 1. Quizzalar mavjudligi va metadata
  console.log("\nTest 1: I4 quizzalari mavjudligi va metadata tekshiruvi...");
  const quizzes = [i4Quiz1, i4Quiz2, i4Quiz3];
  assert.strictEqual(quizzes.length, 3);

  for (let i = 0; i < quizzes.length; i++) {
    const q = quizzes[i];
    assert.strictEqual(q.id, `I4_${i + 1}`);
    assert.strictEqual(q.groupOnly, true);
    assert.strictEqual(q.shuffle, true);
    assert.strictEqual(q.source, "Abdusalom Saidov slaydlaridan");
  }
  assert.strictEqual(i4Quiz1.questions.length, 20);
  assert.strictEqual(i4Quiz2.questions.length, 20);
  assert.strictEqual(i4Quiz3.questions.length, 16);
  console.log("✅ Test 1 muvaffaqiyatli o'tdi (3 ta quiz: 20+20+16 = 56 ta savol).");

  // 2. Jami 56 ta savolning butunligi va variantlari
  console.log("\nTest 2: Jami 56 ta savolning variantlari va to'g'ri javoblari tekshiruvi...");
  const allQuestions = quizzes.flatMap((q) => q.questions);
  assert.strictEqual(allQuestions.length, 56);

  const ids = new Set<string>();
  for (const q of allQuestions) {
    assert.ok(!ids.has(q.id), `Takrorlangan ID: ${q.id}`);
    ids.add(q.id);
    assert.ok(q.question.length > 0, "Savol matni bo'sh bo'lmasligi kerak");
    assert.strictEqual(q.options.length, 4, `Savol ${q.id} da 4 ta variant bo'lishi kerak`);
    assert.ok(
      q.correctOptionId >= 0 && q.correctOptionId <= 3,
      `Savol ${q.id} da to'g'ri javob indeksi 0..3 oralig'ida bo'lishi kerak`
    );
    assert.strictEqual(q.timeLimitSeconds, 20, "Har bir savolga 20 soniya berilishi kerak");
    assert.ok(q.explanation && q.explanation.length > 0, "Izoh mavjud bo'lishi kerak");
  }
  console.log("✅ Test 2 muvaffaqiyatli o'tdi (56 ta savol, 4 tadan variant, to'g'ri indekslar).");

  // 3. I4_3 dagi 8 ta rasmli savol (49-56) va rasm fayllari
  console.log("\nTest 3: I4_3 dagi 8 ta rasmli savol va rasm fayllari tekshiruvi...");
  const imageQuestions = i4Quiz3.questions.filter((q) => q.imagePath);
  assert.strictEqual(imageQuestions.length, 8, "I4_3 da aynan 8 ta rasmli savol bo'lishi kerak");

  for (const q of imageQuestions) {
    assert.ok(q.imagePath, `imagePath mavjud emas: ${q.id}`);
    assert.ok(fs.existsSync(q.imagePath), `Rasm fayli diskda topilmadi: ${q.imagePath}`);
    const stat = fs.statSync(q.imagePath);
    assert.ok(stat.size > 1000, `Rasm fayli hajmi juda kichik: ${q.imagePath}`);
  }
  console.log("✅ Test 3 muvaffaqiyatli o'tdi (8 ta rasm fayli diskda mavjud va to'liq).");

  // 4. getQuizById va sinonimlar
  console.log("\nTest 4: getQuizById va turli formatdagi IDlar tekshiruvi...");
  assert.strictEqual(getQuizById("I4_1"), i4Quiz1);
  assert.strictEqual(getQuizById("i4_1"), i4Quiz1);
  assert.strictEqual(getQuizById("quiz_I4_1"), i4Quiz1);
  assert.strictEqual(getQuizById("start_i4_1"), i4Quiz1);
  assert.strictEqual(getQuizById("i4-1"), i4Quiz1);
  assert.strictEqual(getQuizById("i41"), i4Quiz1);

  assert.strictEqual(getQuizById("I4_3"), i4Quiz3);
  assert.strictEqual(getQuizById("i4_3"), i4Quiz3);
  assert.strictEqual(getQuizById("quiz_I4_3"), i4Quiz3);
  assert.strictEqual(getQuizById("i4-3"), i4Quiz3);
  console.log("✅ Test 4 muvaffaqiyatli o'tdi (Barcha sinonim va prefikslar ishlaydi).");

  // 5. Savollar va variantlar aralashishi (Fisher-Yates) hamda rasm saqlanishi
  console.log("\nTest 5: Savollar va javob variantlari aralashishi tekshiruvi...");
  const prepared = prepareSessionQuiz(i4Quiz3);
  assert.strictEqual(prepared.questions.length, 16);

  let verifiedQuestions = 0;
  for (const q of prepared.questions) {
    const orig = i4Quiz3.questions.find((x) => x.id === q.id);
    assert.ok(orig, `Asl savol topilmadi: ${q.id}`);
    const correctTextInOriginal = orig.options[orig.correctOptionId];
    const correctTextInPrepared = q.options[q.correctOptionId];
    assert.strictEqual(
      correctTextInPrepared,
      correctTextInOriginal,
      `To'g'ri javob matni saqlanmadi (${q.id})`
    );
    if (orig.imagePath) {
      assert.strictEqual(q.imagePath, orig.imagePath, `imagePath yo'qoldi (${q.id})`);
    }
    verifiedQuestions++;
  }
  assert.strictEqual(verifiedQuestions, 16);
  console.log("✅ Test 5 muvaffaqiyatli o'tdi (Savollar, rasmlar va javoblar to'g'ri re-map qilindi).");

  console.log("\n==================================================================");
  console.log("🎉 BARCHA I4 ALKENLAR TESTLARI MUVAFFAQIYATLI O'TDI!");
  console.log("==================================================================");
}

runI4Tests().catch((err) => {
  console.error("❌ Testlarda xatolik:", err);
  process.exit(1);
});
