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
  chatId: number;
  quiz: Quiz;
  status: "idle" | "running" | "completed" | "stopped";
  currentQuestionIndex: number;
  currentPollId: string | null;
  currentPollMessageId: number | null;
  questionStartTime: number;
  timer: NodeJS.Timeout | null;
  answeredUsers: Set<string>; // `${pollId}_${userId}` takroriy javoblarni elash
  participants: Map<number, ParticipantScore>;
}
