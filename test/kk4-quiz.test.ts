import assert from "node:assert";
import {
  getAllQuizzes,
  getQuizById,
  kk4Quiz1,
  kk4Quiz2,
  kk4Quiz3,
  kk4Quiz4,
} from "../src/quiz/questions.js";
import {
  prepareSessionQuiz,
  quizManager,
} from "../src/quiz/quizManager.js";

async function runKk4Tests() {
  console.log("\n==================================================================");
  console.log("🧪 KK_M4 (ADSORBSIYA VA IZOTERMALAR) QUIZ TESTLARI");
  console.log("==================================================================");

  // 1. Quizzalar mavjudligi va metadata
  console.log("\nTest 1: KK4 quizzalari mavjudligi va metadata tekshiruvi...");
  const quizzes = [kk4Quiz1, kk4Quiz2, kk4Quiz3, kk4Quiz4];
  assert.strictEqual(quizzes.length, 4);

  for (let i = 0; i < quizzes.length; i++) {
    const q = quizzes[i];
    assert.strictEqual(q.id, `KK4_${i + 1}`);
    assert.strictEqual(q.groupOnly, true);
    assert.strictEqual(q.shuffle, true);
    assert.strictEqual(q.source, "Bahora Nayimova slaydlaridan");
    assert.strictEqual(q.questions.length, 20);
  }
  console.log("✅ Test 1 muvaffaqiyatli o'tdi (4 ta quiz, har birida 20 tadan savol).");

  // 2. Jami 80 ta savolning butunligi va variantlari
  console.log("\nTest 2: Jami 80 ta savolning variantlari va to'g'ri javoblari tekshiruvi...");
  const allQuestions = quizzes.flatMap((q) => q.questions);
  assert.strictEqual(allQuestions.length, 80);

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
  console.log("✅ Test 2 muvaffaqiyatli o'tdi (80 ta savol, 4 tadan variant, to'g'ri indekslar).");

  // 3. getQuizById va sinonimlar
  console.log("\nTest 3: getQuizById va turli formatdagi IDlar tekshiruvi...");
  assert.strictEqual(getQuizById("KK4_1"), kk4Quiz1);
  assert.strictEqual(getQuizById("kk4_1"), kk4Quiz1);
  assert.strictEqual(getQuizById("quiz_KK4_1"), kk4Quiz1);
  assert.strictEqual(getQuizById("start_kk4_1"), kk4Quiz1);
  assert.strictEqual(getQuizById("kk4-1"), kk4Quiz1);
  assert.strictEqual(getQuizById("kk41"), kk4Quiz1);

  assert.strictEqual(getQuizById("KK4_4"), kk4Quiz4);
  assert.strictEqual(getQuizById("kk4_4"), kk4Quiz4);
  assert.strictEqual(getQuizById("quiz_KK4_4"), kk4Quiz4);
  assert.strictEqual(getQuizById("kk4-4"), kk4Quiz4);
  console.log("✅ Test 3 muvaffaqiyatli o'tdi (Barcha sinonim va prefikslar ishlaydi).");

  // 4. Savollar va variantlar aralashishi (Fisher-Yates)
  console.log("\nTest 4: Savollar va javob variantlari aralashishi tekshiruvi...");
  const prepared = prepareSessionQuiz(kk4Quiz1);
  assert.strictEqual(prepared.questions.length, 20);

  let verifiedQuestions = 0;
  for (const q of prepared.questions) {
    const orig = kk4Quiz1.questions.find((x) => x.id === q.id);
    assert.ok(orig, `Asl savol topilmadi: ${q.id}`);
    const correctTextInOriginal = orig.options[orig.correctOptionId];
    const correctTextInPrepared = q.options[q.correctOptionId];
    assert.strictEqual(
      correctTextInPrepared,
      correctTextInOriginal,
      `To'g'ri javob matni saqlanmadi (${q.id})`
    );
    verifiedQuestions++;
  }
  assert.strictEqual(verifiedQuestions, 20);
  console.log("✅ Test 4 muvaffaqiyatli o'tdi (Savollar va javoblar to'g'ri re-map qilindi).");

  console.log("\n==================================================================");
  console.log("🎉 BARCHA KK4 TESTLARI MUVAFFAQIYATLI O'TDI!");
  console.log("==================================================================");
}

runKk4Tests().catch((err) => {
  console.error("❌ Testlarda xatolik:", err);
  process.exit(1);
});
