import assert from "node:assert";
import dotenv from "dotenv";
dotenv.config();

import { initFirestore, checkFirestoreHealth, getFirestoreDb } from "../src/firebase/firestore.js";
import { FirestoreSessionStorage } from "../src/quiz/sessionStorage.js";
import { Quiz, QuizSession, ParticipantScore } from "../src/quiz/types.js";
import { QuizManager } from "../src/quiz/quizManager.js";

// Alohida izolyatsiyalangan test kolleksiyalari (haqiqiy ma'lumotlarga aslo aralashmaydi)
const TEST_SESSIONS_COLLECTION = "test_quiz_sessions";
const TEST_RESULTS_COLLECTION = "test_quiz_results";

function createSampleQuiz(id = "chem_test_quiz"): Quiz {
  return {
    id,
    title: "Kimyo Test Quizi",
    description: "Cloud Firestore integratsiya testi",
    questions: [
      {
        id: "q1",
        question: "Suvning formulasi qanday?",
        options: ["H2O", "CO2", "NaCl", "CH4"],
        correctOptionId: 0,
        timeLimitSeconds: 20,
      },
      {
        id: "q2",
        question: "Osh tuzining formulasi qanday?",
        options: ["HCl", "NaOH", "NaCl", "KCl"],
        correctOptionId: 2,
        timeLimitSeconds: 20,
      },
    ],
  };
}

async function runFirestoreIntegrationTests() {
  console.log("==================================================================");
  console.log("🔥 CLOUD FIRESTORE REAL INTEGRATSIYA TESTLARI (Frankfurt / europe-west3)");
  console.log("==================================================================");

  // 1. Ulanish va Health Check
  console.log("\n1. Cloud Firestore'ga ulanish va sog'lomlik tekshiruvi...");
  const initOk = await initFirestore();
  assert.strictEqual(initOk, true, "Firestore initsializatsiyasi muvaffaqiyatli bo'lishi shart!");

  const isHealthy = await checkFirestoreHealth();
  assert.strictEqual(isHealthy, true, "checkFirestoreHealth() true qaytarishi shart!");
  console.log("✅ 1-Test muvaffaqiyatli: Cloud Firestore ulandi va sog'lom.");

  const db = getFirestoreDb()!;
  assert.ok(db, "Firestore db obyekti mavjud bo'lishi shart");

  const storage = new FirestoreSessionStorage(db, TEST_SESSIONS_COLLECTION);
  const testChatId = -999111222;
  const testSessionId = `test_sess_${Date.now()}`;

  try {
    // 2. Sessiyani saqlash va qayta o'qish
    console.log("\n2. Sessiyani test_quiz_sessions kolleksiyasiga saqlash va o'qish...");
    const sampleQuiz = createSampleQuiz();
    const session: QuizSession = {
      sessionId: testSessionId,
      chatId: testChatId,
      quiz: sampleQuiz,
      status: "running",
      currentQuestionIndex: 0,
      currentPollId: "poll_fs_1",
      currentPollMessageId: 101,
      questionStartTime: Date.now(),
      timer: null,
      answeredUsers: new Set(["poll_fs_1_1001"]),
      participants: new Map([
        [
          1001,
          {
            userId: 1001,
            firstName: "Dilshod",
            username: "dilshod_chem",
            score: 1,
            totalTimeMs: 4500,
            answersCount: 1,
          },
        ],
      ]),
      consecutiveUnansweredCount: 0,
      currentQuestionAnswered: true,
      version: 1,
      finalMessageSent: false,
    };

    await storage.saveSession(session);

    // O'qib tekshiramiz
    const loadedSessions = await storage.loadAllSessions();
    const loaded = loadedSessions.find((s) => s.chatId === testChatId);
    assert.ok(loaded, "Saqlangan test sessiyasi Firestore'dan topilishi shart");
    assert.strictEqual(loaded.sessionId, testSessionId);
    assert.strictEqual(loaded.status, "running");
    assert.strictEqual(loaded.quiz.title, "Kimyo Test Quizi");
    assert.strictEqual(loaded.currentQuestionIndex, 0);
    assert.strictEqual(loaded.version, 1);

    const participantsMap = new Map(loaded.participants);
    assert.strictEqual(participantsMap.has(1001), true);
    assert.strictEqual(participantsMap.get(1001)?.score, 1);
    assert.strictEqual(participantsMap.get(1001)?.firstName, "Dilshod");
    console.log("✅ 2-Test muvaffaqiyatli: Sessiya Firestore'ga to'liq va aniq saqlandi hamda o'qildi.");

    // 3. Optimistik concurrency va versiyalash (eski versiyani rad etish)
    console.log("\n3. Versiyalash tekshiruvi: yangi versiyani eski versiya bosib ketmasligi...");
    session.version = 2;
    session.currentQuestionIndex = 1;
    await storage.saveSession(session);

    // Eski versiyadagi soxta sessiya
    const staleSession: any = {
      ...session,
      version: 1, // Eski versiya!
      currentQuestionIndex: 0,
    };
    await storage.saveSession(staleSession);

    // Bazadagi holat versiya 2 va currentQuestionIndex 1 bo'lib qolishi shart
    const afterStaleAttempt = (await storage.loadAllSessions()).find((s) => s.chatId === testChatId);
    assert.strictEqual(afterStaleAttempt?.version, 2, "Versiya 2 saqlanib qolishi shart");
    assert.strictEqual(afterStaleAttempt?.currentQuestionIndex, 1, "Eski versiyadagi indeks rad etilishi shart");
    console.log("✅ 3-Test muvaffaqiyatli: Eski versiyadagi kechikkan yozuv yangi holatni bosib ketmadi.");

    // 4. Sessiyani o'chirish
    console.log("\n4. Sessiyani test_quiz_sessions dan o'chirish...");
    await storage.deleteSession(testChatId);
    const afterDelete = (await storage.loadAllSessions()).find((s) => s.chatId === testChatId);
    assert.strictEqual(afterDelete, undefined, "O'chirilgan sessiya Firestore'da qolmasligi shart");
    console.log("✅ 4-Test muvaffaqiyatli: Sessiya Firestore'dan to'liq o'chirildi.");

    // 5. quiz_results saqlash va dublikatlardan himoya
    console.log("\n5. quiz_results ni test_quiz_results ga yozish va dublikatdan himoya...");
    const quizManager = new QuizManager(storage, TEST_RESULTS_COLLECTION);

    const leaderboard: ParticipantScore[] = [
      {
        userId: 2001,
        firstName: "Malika",
        username: "malika_chem",
        score: 2,
        totalTimeMs: 5000,
        answersCount: 2,
      },
      {
        userId: 2002,
        firstName: "Bobur",
        score: 1,
        totalTimeMs: 7000,
        answersCount: 2,
      },
    ];

    const resultsSession: QuizSession = {
      ...session,
      sessionId: `res_${Date.now()}`,
    };

    // 1-marta natijalarni yozamiz
    await quizManager.saveQuizResultsWithRetry(resultsSession, leaderboard);

    // Hujjatlarni tekshiramiz
    const resultsSnap1 = await db.collection(TEST_RESULTS_COLLECTION).where("sessionId", "==", resultsSession.sessionId).get();
    assert.strictEqual(resultsSnap1.docs.length, 2, "Aynan 2 ta ishtirokchi natijasi saqlanishi kerak");

    // 2-marta (takroriy retry/webhook chaqiruvida) yozamiz (yangilangan ball bilan)
    leaderboard[0].score = 3;
    await quizManager.saveQuizResultsWithRetry(resultsSession, leaderboard);

    const resultsSnap2 = await db.collection(TEST_RESULTS_COLLECTION).where("sessionId", "==", resultsSession.sessionId).get();
    assert.strictEqual(resultsSnap2.docs.length, 2, "Dublikat hujjat yaratilmasligi shart (idempotentlik)!");

    const malikaDoc = resultsSnap2.docs.find((d) => d.id === `${resultsSession.sessionId}_2001`);
    assert.ok(malikaDoc, "Malika hujjati topilishi kerak");
    assert.strictEqual(malikaDoc.data().score, 3, "Ball yangilangan bo'lishi kerak");
    console.log("✅ 5-Test muvaffaqiyatli: quiz_results idempotent saqlandi, dublikatlardan himoyalangan.");
  } finally {
    // 6. Test ma'lumotlarini tozalash (haqiqiy bazada hech qanday chiqindi qoldirmaymiz)
    console.log("\n6. Test kolleksiyalarini tozalash (Cleanup)...");
    await storage.clearAll();

    const resultsSnap = await db.collection(TEST_RESULTS_COLLECTION).get();
    const batch = db.batch();
    resultsSnap.docs.forEach((d) => batch.delete(d.ref));
    await batch.commit();

    console.log("✅ 6-Test muvaffaqiyatli: Barcha test hujjatlari to'liq tozalandi.");
  }

  console.log("\n🎉 BARCHA CLOUD FIRESTORE INTEGRATSIYA TESTLARI (6/6) 100% MUVAFFAQIYATLI O'TDI!\n");
}

runFirestoreIntegrationTests()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error("❌ Firestore integratsiya testida xatolik:", err);
    process.exit(1);
  });
