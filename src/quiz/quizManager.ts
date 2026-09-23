import { Quiz, QuizSession, ParticipantScore } from "./types.js";

export function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

export interface TelegramApiSender {
  sendPoll(
    chatId: number | string,
    question: string,
    options: string[],
    other?: Record<string, any>
  ): Promise<{ message_id: number; poll: { id: string } }>;
  stopPoll(chatId: number | string, messageId: number): Promise<any>;
  sendMessage(chatId: number | string, text: string, other?: Record<string, any>): Promise<any>;
}

export interface PollAnswerData {
  pollId: string;
  user: {
    id: number;
    first_name: string;
    last_name?: string;
    username?: string;
  };
  optionIds: number[];
}

export class QuizManager {
  // Har bir chat_id uchun alohida faol sessiya
  private sessions = new Map<number, QuizSession>();

  // poll_id orqali qaysi guruh va qaysi savolga tegishli ekanini tezkor topish xaritasi
  private pollToSession = new Map<
    string,
    {
      chatId: number;
      questionIndex: number;
      correctOptionId: number;
      startTime: number;
      isClosed: boolean;
    }
  >();

  /**
   * Guruhda quiz ishlayotganligini tekshirish
   */
  public isQuizRunning(chatId: number): boolean {
    const session = this.sessions.get(chatId);
    return session !== undefined && session.status === "running";
  }

  /**
   * Guruhdagi faol sessiyani olish
   */
  public getSession(chatId: number): QuizSession | undefined {
    return this.sessions.get(chatId);
  }

  /**
   * Yangi quizni boshlash
   */
  public async startQuiz(
    chatId: number,
    quiz: Quiz,
    api: TelegramApiSender
  ): Promise<{ success: boolean; message: string }> {
    if (this.isQuizRunning(chatId)) {
      return {
        success: false,
        message: "⚠️ Bu guruhda hozirda faol quiz davom etmoqda. Iltimos, u yakunlanishini kuting yoki /stopquiz buyrug'ini bering.",
      };
    }

    const session: QuizSession = {
      chatId,
      quiz,
      status: "running",
      currentQuestionIndex: -1,
      currentPollId: null,
      currentPollMessageId: null,
      questionStartTime: 0,
      timer: null,
      answeredUsers: new Set<string>(),
      participants: new Map<number, ParticipantScore>(),
    };

    this.sessions.set(chatId, session);

    // Guruhga e'lon xabari
    await api.sendMessage(
      chatId,
      `🧪 <b>«${escapeHtml(quiz.title)}» boshlandi!</b>\n\n` +
        `📝 ${escapeHtml(quiz.description)}\n` +
        `❓ Savollar soni: <b>${quiz.questions.length} ta</b>\n` +
        `⏱ Har bir savolga: <b>15 soniya</b>\n\n` +
        `<i>Tayyor turing, 1-savol 3 soniyadan so'ng yuboriladi...</i>`,
      { parse_mode: "HTML" }
    );

    console.log(
      `[Quiz] Guruhda yangi quiz boshlandi (chatId: ${chatId}, savollar soni: ${quiz.questions.length})`
    );

    // 3 soniyadan keyin 1-savol yuboriladi
    session.timer = setTimeout(async () => {
      await this.sendNextQuestion(chatId, api);
    }, 3000);

    return { success: true, message: "Quiz muvaffaqiyatli boshlandi!" };
  }

  /**
   * Keyingi savolni yuborish
   */
  public async sendNextQuestion(chatId: number, api: TelegramApiSender): Promise<void> {
    const session = this.sessions.get(chatId);
    if (!session || session.status !== "running") return;

    session.currentQuestionIndex += 1;

    // Agar savollar tugagan bo'lsa, quizni yakunlash
    if (session.currentQuestionIndex >= session.quiz.questions.length) {
      await this.finishQuiz(chatId, api);
      return;
    }

    const q = session.quiz.questions[session.currentQuestionIndex];
    const totalQuestions = session.quiz.questions.length;
    const questionNumber = session.currentQuestionIndex + 1;

    const questionText = `[${questionNumber}/${totalQuestions}] ${q.question}`;

    try {
      // Joriy Bot API bo'yicha faqat correct_option_ids uzatiladi
      const message = await api.sendPoll(chatId, questionText, q.options, {
        type: "quiz",
        correct_option_ids: [q.correctOptionId],
        is_anonymous: false, // Foydalanuvchilarni aniqlash uchun noanonim poll
        explanation: q.explanation,
        open_period: q.timeLimitSeconds, // Telegramning rasmiy taymeri
      });

      console.log(
        `[Quiz] ${questionNumber}/${totalQuestions}-savol yuborildi (chatId: ${chatId}, pollId: ${message.poll.id}, vaqt: ${q.timeLimitSeconds}s)`
      );

      session.currentPollId = message.poll.id;
      session.currentPollMessageId = message.message_id;
      session.questionStartTime = Date.now();

      // poll_id xaritasiga saqlaymiz (isClosed: false)
      this.pollToSession.set(message.poll.id, {
        chatId,
        questionIndex: session.currentQuestionIndex,
        correctOptionId: q.correctOptionId,
        startTime: session.questionStartTime,
        isClosed: false,
      });

      // Vaqt tugagach savolni yopish va keyingisiga o'tish taymeri
      session.timer = setTimeout(async () => {
        await this.handleQuestionTimeout(chatId, api);
      }, (q.timeLimitSeconds + 1) * 1000);
    } catch (error) {
      console.error(`[QuizManager] Savol yuborishda xatolik (chat: ${chatId}):`, error);
      await api.sendMessage(
        chatId,
        `⚠️ Savolni yuborishda xatolik yuz berdi. Bot guruhda so'rovnoma yuborish huquqiga ega ekanini tekshiring.`
      );
      await this.stopQuiz(chatId);
    }
  }

  /**
   * Savol vaqti tugaganda ishga tushuvchi mantiq
   */
  private async handleQuestionTimeout(chatId: number, api: TelegramApiSender): Promise<void> {
    const session = this.sessions.get(chatId);
    if (!session || session.status !== "running") return;

    // Ushbu savolni yopilgan deb belgilaymiz (kech kelgan javoblar hisoblanmasligi uchun)
    if (session.currentPollId) {
      const pollInfo = this.pollToSession.get(session.currentPollId);
      if (pollInfo) {
        pollInfo.isClosed = true;
      }
    }

    if (session.currentPollMessageId) {
      try {
        await api.stopPoll(chatId, session.currentPollMessageId);
      } catch (err) {
        // Telegram tomonidan allaqachon yopilgan bo'lsa
      }
    }

    // 2 soniya pauza (foydalanuvchilar to'g'ri javob va izohni ko'rib olishlari uchun)
    session.timer = setTimeout(async () => {
      await this.sendNextQuestion(chatId, api);
    }, 2000);
  }

  /**
   * Foydalanuvchi poll'da ovoz berganda (poll_answer hodisasi)
   */
  public handlePollAnswer(answer: PollAnswerData): boolean {
    const pollInfo = this.pollToSession.get(answer.pollId);
    if (!pollInfo) {
      return false;
    }

    // ESKI YOKI YOPILGAN SAVOLLARDAN KECH KELGAN JAVOBLARNI RAD ETISH
    if (pollInfo.isClosed) {
      return false;
    }

    const session = this.sessions.get(pollInfo.chatId);
    if (!session || session.status !== "running") {
      return false;
    }

    // Faqat ayni paytdagi faol savol bo'lsa
    if (session.currentPollId !== answer.pollId) {
      return false;
    }

    // TAKRORIY JAVOBLARNI ELASH (Deduplication)
    const dedupKey = `${answer.pollId}_${answer.user.id}`;
    if (session.answeredUsers.has(dedupKey)) {
      return false;
    }
    session.answeredUsers.add(dedupKey);

    // Javob berish vaqti
    const responseTimeMs = Math.max(0, Date.now() - pollInfo.startTime);

    // To'g'riligini tekshirish
    const isCorrect = answer.optionIds.includes(pollInfo.correctOptionId);

    // Ishtirokchi ma'lumotlarini yangilash
    let participant = session.participants.get(answer.user.id);
    if (!participant) {
      participant = {
        userId: answer.user.id,
        firstName: answer.user.first_name || "Ishtirokchi",
        lastName: answer.user.last_name,
        username: answer.user.username,
        score: 0,
        totalTimeMs: 0,
        answersCount: 0,
      };
      session.participants.set(answer.user.id, participant);
    }

    participant.answersCount += 1;
    if (isCorrect) {
      participant.score += 1;
    }
    participant.totalTimeMs += responseTimeMs;

    const userDisplay = answer.user.username ? `@${answer.user.username}` : answer.user.first_name;
    console.log(
      `[Quiz] Javob qabul qilindi: ${userDisplay} (chatId: ${pollInfo.chatId}, savol: ${pollInfo.questionIndex + 1}, to'g'ri: ${isCorrect}, vaqt: ${(responseTimeMs / 1000).toFixed(1)}s)`
    );

    return true;
  }

  /**
   * Saralangan yakuniy reyting jadvalini olish
   */
  public getLeaderboard(chatId: number): ParticipantScore[] {
    const session = this.sessions.get(chatId);
    if (!session) return [];

    const list = Array.from(session.participants.values());

    // Qoida: To'g'ri javoblar soni ko'plar yuqorida; teng ball bo'lsa, qisqaroq umumiy vaqt ustun
    list.sort((a, b) => {
      if (b.score !== a.score) {
        return b.score - a.score;
      }
      return a.totalTimeMs - b.totalTimeMs;
    });

    return list;
  }

  /**
   * Quizni muvaffaqiyatli yakunlash va natijalarni e'lon qilish
   */
  public async finishQuiz(chatId: number, api: TelegramApiSender): Promise<void> {
    const session = this.sessions.get(chatId);
    if (!session) return;

    this.clearSessionTimer(session);
    session.status = "completed";

    // Barcha savollarni yopilgan deb belgilaymiz
    if (session.currentPollId) {
      const pollInfo = this.pollToSession.get(session.currentPollId);
      if (pollInfo) {
        pollInfo.isClosed = true;
      }
    }

    const leaderboard = this.getLeaderboard(chatId);
    const totalQuestions = session.quiz.questions.length;

    console.log(
      `[Quiz] Quiz yakunlandi (chatId: ${chatId}). Ishtirokchilar soni: ${leaderboard.length}`
    );

    let text = `🏁 <b>«${escapeHtml(session.quiz.title)}» yakunlandi!</b>\n\n`;

    if (leaderboard.length === 0) {
      text += `Afsuski, hech bir ishtirokchi savollarga javob bermadi. 😴\nKeyingi safar faolroq bo'ling!`;
    } else {
      text += `📊 <b>Yakuniy Natijalar va Reyting:</b>\n\n`;

      const medals = ["🥇", "🥈", "🥉"];

      leaderboard.forEach((p, index) => {
        const medal = index < 3 ? `${medals[index]} ` : `${index + 1}. `;
        const timeSec = (p.totalTimeMs / 1000).toFixed(1);
        const rawName = p.username ? `@${p.username}` : (p.firstName + (p.lastName ? ` ${p.lastName}` : ""));
        const safeName = escapeHtml(rawName);

        text += `${medal}<b>${safeName}</b>: ${p.score}/${totalQuestions} ball (jami javob vaqti: ${timeSec}s)\n`;
      });

      text += `\nBarcha ishtirokchilarga qatnashganlari uchun tashakkur! 👏`;
    }

    await api.sendMessage(chatId, text, { parse_mode: "HTML" });

    // Sessiyani tozalash
    this.sessions.delete(chatId);
  }

  /**
   * Quizni majburiy to'xtatish (/stopquiz)
   */
  public async stopQuiz(chatId: number, api?: TelegramApiSender): Promise<boolean> {
    const session = this.sessions.get(chatId);
    if (!session) return false;

    this.clearSessionTimer(session);

    if (session.currentPollId) {
      const pollInfo = this.pollToSession.get(session.currentPollId);
      if (pollInfo) {
        pollInfo.isClosed = true;
      }
    }

    if (session.currentPollMessageId && api) {
      try {
        await api.stopPoll(chatId, session.currentPollMessageId);
      } catch (e) {
        // e'tiborsiz qoldiramiz
      }
    }

    if (api) {
      await api.sendMessage(chatId, "🛑 <b>Quiz to'xtatildi.</b>", { parse_mode: "HTML" });
    }

    session.status = "stopped";
    this.sessions.delete(chatId);
    return true;
  }

  private clearSessionTimer(session: QuizSession): void {
    if (session.timer) {
      clearTimeout(session.timer);
      session.timer = null;
    }
  }
}

// Global Singleton QuizManager
export const quizManager = new QuizManager();
