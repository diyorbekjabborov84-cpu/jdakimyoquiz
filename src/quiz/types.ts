export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctOptionId: number; // 0-based index
  explanation?: string;
  timeLimitSeconds: number;
}

export interface Quiz {
  id: string;
  title: string;
  description: string;
  questions: QuizQuestion[];
  groupOnly?: boolean; // Faqat Telegram guruhlarida o'tkazilishi shart bo'lsa
  shuffle?: boolean; // Savollar va variantlar har sessiyada aralashtirilishi kerak bo'lsa
  source?: string; // Savollar manbasi (masalan: "Bahora Nayimova slaydlaridan")
}

export interface ParticipantScore {
  userId: number;
  firstName: string;
  lastName?: string;
  username?: string;
  score: number; // to'g'ri javoblar soni
  totalTimeMs: number; // umumiy javob berishga ketgan vaqt (millisekundda)
  answersCount: number; // berilgan umumiy javoblar soni
}

export interface QuizSession {
  sessionId: string; // Sessiyaning takrorlanmas identifikatori (eski pauza tugmalarini filtrlash uchun)
  chatId: number;
  quiz: Quiz;
  status: "idle" | "running" | "completed" | "stopped" | "paused" | "finishing";
  currentQuestionIndex: number;
  currentPollId: string | null;
  currentPollMessageId: number | null;
  questionStartTime: number;
  timer: NodeJS.Timeout | null;
  answeredUsers: Set<string>; // `${pollId}_${userId}` takroriy javoblarni elash
  participants: Map<number, ParticipantScore>;
  consecutiveUnansweredCount: number; // Ketma-ket javobsiz qolgan savollar soni
  currentQuestionAnswered: boolean; // Joriy savolga kamida 1 kishi javob berdimi
  version: number; // Sessiya holati versiyasi (per-chat tartibli yozuv va poyga holatlarini oldini olish uchun)
  finalMessageSent?: boolean; // Yakuniy natija xabari to'liq yuborilganligini tekshirish
  sentChunksCount?: number; // Yakuniy natija xabaridan necha bo'lak muvaffaqiyatli yuborilganligi progressi (retry/restart davom ettirishi uchun)
}
