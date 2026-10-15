import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";
import { allQuizzes, getQuizById } from "../quiz/questions.js";

export interface QuizSessionItem {
  sessionId: string;
  chatId: number;
  groupTitle?: string;
  quizId: string;
  quizTitle: string;
  totalQuestions: number;
  participantsCount: number;
  winner?: {
    name: string;
    username: string | null;
    score: number;
  } | null;
  status: string;
  createdAt: string;
}

export interface LeaderboardEntry {
  rank: number;
  userId: number;
  name: string;
  username: string | null;
  score: number;
  totalQuestions: number;
  totalTimeSeconds: number;
  accuracy: number;
}

export interface ResultsListResult {
  sessions: QuizSessionItem[];
  total: number;
  quizzes: Array<{ id: string; title: string }>;
}

/**
 * Guruhlar kesimida o'tkazilgan barcha quiz sessiyalari ro'yxatini olish
 */
export async function getQuizResultsList(options: {
  quizId?: string;
  chatId?: number;
  limit?: number;
}): Promise<ResultsListResult> {
  const db = getFirestoreDb();
  const limitCount = options.limit || 50;

  // Mavjud barcha quizlar ro'yxati (filtrlash dropdowni uchun)
  const availableQuizzes = allQuizzes.map((q) => ({ id: q.id, title: q.title }));

  if (!db) {
    return {
      sessions: [],
      total: 0,
      quizzes: availableQuizzes,
    };
  }

  try {
    // Guruh nomlarini tezkor topish uchun guruhlar keshi
    const groupTitles = new Map<number, string>();
    try {
      const groupSnap = await db.collection(FIRESTORE_COLLECTIONS.GROUPS).select("chatId", "title").limit(100).get();
      for (const gDoc of groupSnap.docs) {
        const gData = gDoc.data();
        if (gData.chatId) groupTitles.set(Number(gData.chatId), gData.title || `Guruh ${gData.chatId}`);
      }
    } catch {
      // Guruhlar to'plami yo'q bo'lsa davom etadi
    }

    // 1. Faol yoki davom etayotgan sessiyalarni olish (SESSIONS to'plamidan)
    const activeSessions: QuizSessionItem[] = [];
    try {
      let queryRef: any = db.collection(FIRESTORE_COLLECTIONS.SESSIONS);
      if (options.chatId) {
        queryRef = queryRef.where("chatId", "==", Number(options.chatId));
      }

      const snap = await queryRef.limit(50).get();

      for (const doc of snap.docs) {
        const data = doc.data();
        const currentQuizId = data.quizData?.id || data.quiz?.id || data.quizId || "unknown";

        if (options.quizId && options.quizId !== "all" && currentQuizId !== options.quizId) {
          continue;
        }

        const chatId = Number(data.chatId);
        const groupTitle = groupTitles.get(chatId) || `Guruh ${chatId}`;
        const quizInfo = getQuizById(currentQuizId);
        const quizTitle = data.quizData?.title || data.quiz?.title || quizInfo?.title || currentQuizId;
        const totalQ = data.quizData?.questions?.length || data.quiz?.questions?.length || quizInfo?.questions?.length || 20;

        let participantsCount = 0;
        let winner: { name: string; username: string | null; score: number } | null = null;

        if (Array.isArray(data.participants) && data.participants.length > 0) {
          participantsCount = data.participants.length;
          const flatList = data.participants.map((p: any) => (Array.isArray(p) ? p[1] : p)).filter(Boolean);
          const sorted = [...flatList].sort((a: any, b: any) => (b.score || 0) - (a.score || 0));
          if (sorted[0]) {
            winner = {
              name: sorted[0].firstName || "Ishtirokchi",
              username: sorted[0].username || null,
              score: sorted[0].score || 0,
            };
          }
        } else if (data.participants && typeof data.participants === "object") {
          const vals = Object.values(data.participants) as any[];
          participantsCount = vals.length;
          if (vals.length > 0) {
            const sorted = [...vals].sort((a: any, b: any) => (b.score || 0) - (a.score || 0));
            if (sorted[0] && (sorted[0].firstName || sorted[0].score !== undefined)) {
              winner = {
                name: sorted[0].firstName || "Ishtirokchi",
                username: sorted[0].username || null,
                score: sorted[0].score || 0,
              };
            }
          }
        }

        const createdAt = data.savedAt || data.updatedAt || data.createdAt || new Date().toISOString();

        activeSessions.push({
          sessionId: data.sessionId || doc.id,
          chatId,
          groupTitle,
          quizId: currentQuizId,
          quizTitle,
          totalQuestions: totalQ,
          participantsCount,
          winner,
          status: data.status || "running",
          createdAt: typeof createdAt === "number" ? new Date(createdAt).toISOString() : String(createdAt),
        });
      }
    } catch (e: any) {
      console.warn("[ResultsService] SESSIONS to'plamini o'qishda ogohlantirish:", e?.message || e);
    }

    // 2. Tugallangan quizlar natijalarini olish (RESULTS to'plamidan)
    const finishedSessionsMap = new Map<
      string,
      {
        sessionId: string;
        chatId: number;
        quizId: string;
        totalQuestions: number;
        createdAt: string;
        results: any[];
      }
    >();

    try {
      let resultsQuery: any = db.collection(FIRESTORE_COLLECTIONS.RESULTS);
      if (options.chatId) {
        resultsQuery = resultsQuery.where("chatId", "==", Number(options.chatId));
      }
      const resultsSnap = await resultsQuery.limit(300).get();

      for (const doc of resultsSnap.docs) {
        const d = doc.data();
        const sId = d.sessionId;
        if (!sId) continue;

        if (options.quizId && options.quizId !== "all" && d.quizId !== options.quizId) {
          continue;
        }

        if (!finishedSessionsMap.has(sId)) {
          finishedSessionsMap.set(sId, {
            sessionId: sId,
            chatId: Number(d.chatId),
            quizId: d.quizId || "unknown",
            totalQuestions: Number(d.totalQuestions) || 20,
            createdAt: d.createdAt || new Date().toISOString(),
            results: [],
          });
        }
        finishedSessionsMap.get(sId)!.results.push(d);
      }
    } catch (e: any) {
      console.warn("[ResultsService] RESULTS to'plamini o'qishda ogohlantirish:", e?.message || e);
    }

    // Tugallangan sessiyalarni QuizSessionItem shakliga keltirish
    const finishedSessions: QuizSessionItem[] = [];
    for (const [sId, item] of finishedSessionsMap.entries()) {
      const existing = activeSessions.find((s) => s.sessionId === sId);
      if (existing) {
        if (!existing.winner && item.results.length > 0) {
          const sorted = [...item.results].sort((a, b) => (b.score || 0) - (a.score || 0));
          existing.winner = {
            name: sorted[0].firstName || "Ishtirokchi",
            username: sorted[0].username || null,
            score: sorted[0].score || 0,
          };
          existing.participantsCount = item.results.length;
        }
        continue;
      }

      const sorted = [...item.results].sort((a, b) => (b.score || 0) - (a.score || 0));
      const quizInfo = getQuizById(item.quizId);
      const quizTitle = quizInfo?.title || item.quizId;
      const winner = sorted[0]
        ? {
            name: sorted[0].firstName || "Ishtirokchi",
            username: sorted[0].username || null,
            score: sorted[0].score || 0,
          }
        : null;

      finishedSessions.push({
        sessionId: sId,
        chatId: item.chatId,
        groupTitle: groupTitles.get(item.chatId) || `Guruh ${item.chatId}`,
        quizId: item.quizId,
        quizTitle,
        totalQuestions: item.totalQuestions,
        participantsCount: item.results.length,
        winner,
        status: "finished",
        createdAt: item.createdAt,
      });
    }

    const allSessions = [...activeSessions, ...finishedSessions];

    // Sana bo'yicha eng yangilarini yuqoriga qo'yish
    allSessions.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());

    const finalSessions = allSessions.slice(0, limitCount);

    return {
      sessions: finalSessions,
      total: allSessions.length,
      quizzes: availableQuizzes,
    };
  } catch (err: any) {
    console.error("[ResultsService] Sessiyalar ro'yxatini olishda xatolik:", err?.message || err);
    return {
      sessions: [],
      total: 0,
      quizzes: availableQuizzes,
    };
  }
}

/**
 * Muayyan sessiya bo'yicha to'liq ishtirokchilar reytingini (Leaderboard) olish
 */
export async function getSessionLeaderboard(sessionId: string): Promise<{
  sessionInfo: Partial<QuizSessionItem> | null;
  leaderboard: LeaderboardEntry[];
}> {
  const db = getFirestoreDb();
  if (!db) {
    return { sessionInfo: null, leaderboard: [] };
  }

  try {
    // 1. Natijalarni RESULTS to'plamidan olish
    const resultsSnap = await db
      .collection(FIRESTORE_COLLECTIONS.RESULTS)
      .where("sessionId", "==", sessionId)
      .get();

    let rawList: any[] = [];
    if (!resultsSnap.empty) {
      rawList = resultsSnap.docs.map((d) => d.data());
    }

    // 2. Agar RESULTS da bo'lmasa, faol SESSIONS to'plamidan qidirish
    let sData: any = null;
    if (rawList.length === 0) {
      const sessionDoc = await db.collection(FIRESTORE_COLLECTIONS.SESSIONS).doc(sessionId).get();
      if (sessionDoc.exists) {
        sData = sessionDoc.data();
      } else {
        const activeSnap = await db
          .collection(FIRESTORE_COLLECTIONS.SESSIONS)
          .where("sessionId", "==", sessionId)
          .limit(1)
          .get();
        if (!activeSnap.empty) {
          sData = activeSnap.docs[0].data();
        }
      }

      if (sData?.participants) {
        if (Array.isArray(sData.participants)) {
          rawList = sData.participants.map((p: any) => (Array.isArray(p) ? p[1] : p)).filter(Boolean);
        } else if (typeof sData.participants === "object") {
          rawList = Object.values(sData.participants);
        }
      }
    }

    if (rawList.length === 0) {
      return { sessionInfo: null, leaderboard: [] };
    }

    // Saralash: ball kamayish tartibida, teng bo'lsa vaqt o'sish tartibida
    rawList.sort((a, b) => {
      if ((b.score || 0) !== (a.score || 0)) {
        return (b.score || 0) - (a.score || 0);
      }
      return (a.totalTimeMs || 0) - (b.totalTimeMs || 0);
    });

    const sample = rawList[0] || {};
    const quizId = sample.quizId || sData?.quizData?.id || sData?.quiz?.id || "unknown";
    const quizInfo = getQuizById(quizId);
    const quizTitle = sample.quizTitle || quizInfo?.title || sData?.quizData?.title || sData?.quiz?.title || quizId;
    const totalQ = Number(sample.totalQuestions) || quizInfo?.questions?.length || 20;
    const chatId = Number(sample.chatId || sData?.chatId || 0);

    const sessionInfo: Partial<QuizSessionItem> = {
      sessionId,
      chatId,
      quizId,
      quizTitle,
      totalQuestions: totalQ,
      createdAt: sample.createdAt || sData?.savedAt || sData?.createdAt || new Date().toISOString(),
    };

    const leaderboard: LeaderboardEntry[] = rawList.map((item, index) => {
      const score = item.score || 0;
      const totalTimeMs = item.totalTimeMs || 0;
      const accuracy = totalQ > 0 ? Math.round((score / totalQ) * 100) : 0;

      return {
        rank: index + 1,
        userId: Number(item.userId || index + 1),
        name: item.firstName || "Ishtirokchi",
        username: item.username || null,
        score,
        totalQuestions: totalQ,
        totalTimeSeconds: parseFloat((totalTimeMs / 1000).toFixed(1)),
        accuracy,
      };
    });

    return { sessionInfo, leaderboard };
  } catch (err: any) {
    console.error(`[ResultsService] Sessiya reytingini olishda xatolik (${sessionId}):`, err?.message || err);
    return { sessionInfo: null, leaderboard: [] };
  }
}
