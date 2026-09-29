import { InputFile } from "grammy";
import { Quiz, QuizSession, ParticipantScore } from "./types.js";
import { ISessionStorage, defaultSessionStorage, FirestoreSessionStorage, SessionStorage } from "./sessionStorage.js";
import { getDatabasePool } from "../database/db.js";
import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";

export function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Elementlarni tasodifiy aralashtirish (Fisher-Yates algoritmi)
 */
export function shuffleArray<T>(array: T[]): T[] {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/**
 * Quiz sessiyasi uchun savollar va variantlarni tayyorlash.
 * Agar quiz.shuffle bo'lsa:
 * 1. Har bir savolning 4 ta javob varianti mustaqil aralashtiriladi.
 * 2. To'g'ri javob indeksi (correctOptionId) yangi tartibga mos qayta hisoblanadi.
 * 3. Savollar tartibi ham butunlay tasodifiy aralashtiriladi.
 * 4. Asl Quiz obyekti aslo o'zgarmasdan (immutable) qoladi.
 */
export function prepareSessionQuiz(quiz: Quiz): Quiz {
  if (!quiz.shuffle) {
    return {
      ...quiz,
      questions: quiz.questions.map((q) => ({
        ...q,
        options: [...q.options],
      })),
    };
  }

  // 1. Variantlarni aralashtirish va to'g'ri indeksni qayta hisoblash
  const preparedQuestions = quiz.questions.map((q) => {
    const correctText = q.options[q.correctOptionId];
    const shuffledOptions = shuffleArray(q.options);
    const newCorrectOptionId = shuffledOptions.indexOf(correctText);

    return {
      ...q,
      options: shuffledOptions,
      correctOptionId: newCorrectOptionId,
    };
  });

  // 2. Savollar tartibini ham aralashtirish
  const shuffledQuestions = shuffleArray(preparedQuestions);

  return {
    ...quiz,
    questions: shuffledQuestions,
  };
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
  sendPhoto?(chatId: number | string, photo: any, other?: Record<string, any>): Promise<any>;
  getChatMember?(chatId: number | string, userId: number): Promise<any>;
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
  private sessionStorage: ISessionStorage;
  private chatLocks = new Set<number>();

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

  private resultsCollectionName?: string;
  private chatQueues = new Map<number, Promise<any>>();

  constructor(
    sessionStorage: ISessionStorage = defaultSessionStorage,
    resultsCollectionName?: string
  ) {
    this.sessionStorage = sessionStorage;
    this.resultsCollectionName = resultsCollectionName;
  }

  /**
   * Per-chat barcha muhim operatsiyalarni (read-modify-write) qat'iy ketma-ket navbatga qo'yish.
   */
  public enqueueChatOp<T>(chatId: number, op: () => Promise<T>): Promise<T> {
    const previous = this.chatQueues.get(chatId) || Promise.resolve();
    const next = previous
      .catch(() => {})
      .then(op);
    this.chatQueues.set(chatId, next);
    return next.finally(() => {
      if (this.chatQueues.get(chatId) === next) {
        this.chatQueues.delete(chatId);
      }
    });
  }

  public getSessionStorage(): ISessionStorage {
    return this.sessionStorage;
  }

  public setResultsCollectionName(name: string): void {
    this.resultsCollectionName = name;
  }

  /**
   * Guruhda quiz ishlayotganligini tekshirish (faqat running)
   */
  public isQuizRunning(chatId: number): boolean {
    const session = this.sessions.get(chatId);
    return session !== undefined && session.status === "running";
  }

  /**
   * Guruhda quiz pauza holatidaligini tekshirish
   */
  public isQuizPaused(chatId: number): boolean {
    const session = this.sessions.get(chatId);
    return session !== undefined && session.status === "paused";
  }

  /**
   * Guruhda faol, pauzada yoki yakunlanish (finishing) holatidagi quiz borligini tekshirish.
   * Yakunlash jarayoni to'liq tugamaguncha yangi quiz boshlanishi bloklanadi.
   */
  public isQuizActive(chatId: number): boolean {
    const session = this.sessions.get(chatId);
    return (
      session !== undefined &&
      (session.status === "running" || session.status === "paused" || session.status === "finishing")
    );
  }

  /**
   * Saqlangan sessiyalarni xotiraga tiklash (server qayta ishga tushganda).
   * Productionda faqat PostgreSQL bazasidan o'qiladi.
   */
  public async loadPersistedSessions(api?: TelegramApiSender): Promise<void> {
    try {
      const savedSessions = await this.sessionStorage.loadAllSessions();
      for (const s of savedSessions) {
        const session = this.populateSession(s);
        // Agar sessiya "finishing" holatida qolgan bo'lsa (restartdan oldin natijalar saqlashda qolgan bo'lsa)
        if (session.status === "finishing" && api) {
          if (session.finalMessageSent) {
            // Natija xabari oldinroq muvaffaqiyatli yuborilgan, faqat sessiyani bazadan va xotiradan tozalash qolgan
            session.status = "completed";
            await this.sessionStorage.deleteSession(session.chatId);
            this.sessions.delete(session.chatId);
          } else {
            // Xatolik yutilmaydi! Recovery muvaffaqiyatsiz bo'lsa, startup to'xtashi uchun xato yuqoriga chiqadi
            await this.finishQuiz(session.chatId, api);
          }
        }
      }
    } catch (e) {
      console.error("[QuizManager] Sessiyalarni saqlash tizimidan yuklashda xatolik:", e);
      throw e;
    }

    // Agar Telegram API berilgan bo'lsa, guruhlarga yangi xabar va resume tugmasini yuboramiz
    if (api) {
      for (const session of this.sessions.values()) {
        if (session.status === "paused") {
          try {
            const currentQ = session.currentQuestionIndex + 1;
            const totalQ = session.quiz.questions.length;
            await api.sendMessage(
              session.chatId,
              `🔄 <b>Bot serveri qayta ishga tushirildi va «${escapeHtml(session.quiz.title)}» sessiyasi saqlab qolindi!</b>\n\n` +
                `📊 O‘tilgan savollar: <b>${currentQ}/${totalQ}</b>\n` +
                `👥 Qatnashuvchilar: <b>${session.participants.size} ta</b>\n\n` +
                `Quizni to‘xtagan joyidan davom ettirish uchun quyidagi tugmani bosing yoki guruhda <b>/resume</b> buyrug‘ini yuboring:`,
              {
                parse_mode: "HTML",
                reply_markup: {
                  inline_keyboard: [
                    [
                      {
                        text: "▶️ Qolgan joyidan davom ettirish",
                        callback_data: `resume_quiz_${session.chatId}_${session.sessionId}`,
                      },
                    ],
                  ],
                },
              }
            );
          } catch (notifyErr) {
            console.error(`[QuizManager] Chat ${session.chatId} ga tiklanish xabarini yuborishda xatolik:`, notifyErr);
          }
        }
      }
    }
  }

  private populateSession(s: any): QuizSession {
    const sessionId = s.sessionId || `s_${s.chatId}_${s.savedAt || Date.now()}`;
    const status = s.status === "finishing" ? "finishing" : "paused";
    const session: QuizSession = {
      sessionId,
      chatId: s.chatId,
      quiz: s.quiz,
      status,
      currentQuestionIndex: s.currentQuestionIndex,
      currentPollId: null,
      currentPollMessageId: null,
      questionStartTime: 0,
      timer: null,
      answeredUsers: new Set(s.answeredUsers),
      participants: new Map(s.participants),
      consecutiveUnansweredCount: s.consecutiveUnansweredCount || 0,
      currentQuestionAnswered: false,
      version: s.version || 1,
      finalMessageSent: Boolean(s.finalMessageSent),
      sentChunksCount: Number(s.sentChunksCount || 0),
    };
    this.sessions.set(s.chatId, session);
    console.log(
      `[QuizManager] Chat ${s.chatId} uchun saqlangan ${status} sessiyasi yuklandi (${s.currentQuestionIndex + 1}/${s.quiz.questions.length})`
    );
    return session;
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
    if (this.chatLocks.has(chatId) || this.isQuizActive(chatId)) {
      const isPaused = this.isQuizPaused(chatId);
      const isFinishing = this.sessions.get(chatId)?.status === "finishing";
      return {
        success: false,
        message: isFinishing
          ? "⚠️ Bu chatda quiz yakunlanmoqda va natijalari bazaga saqlanmoqda. Yangi quiz boshlashdan oldin kuting yoki /stop buyrug'ini bering."
          : isPaused
          ? "⚠️ Bu chatda to'xtatilgan (pauza qilingan quiz mavjud). Iltimos, uni «▶️ Qolgan joyidan davom ettirish» tugmasi yoki /resume buyrug'i bilan davom ettiring, yoki /stop buyrug'i bilan to'xtating."
          : "⚠️ Bu chatda allaqachon faol quiz davom etmoqda. Iltimos, u yakunlanishini kuting yoki /stop buyrug'i bilan to'xtating.",
      };
    }

    this.chatLocks.add(chatId);
    try {
      // Sessiya uchun quizni tayyorlash (aralashtirish va indekslarni qayta hisoblash)
      const sessionQuiz = prepareSessionQuiz(quiz);
      const sessionId = `s_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 6)}`;

      const session: QuizSession = {
        sessionId,
        chatId,
        quiz: sessionQuiz,
        status: "running",
        currentQuestionIndex: -1,
        currentPollId: null,
        currentPollMessageId: null,
        questionStartTime: 0,
        timer: null,
        answeredUsers: new Set<string>(),
        participants: new Map<number, ParticipantScore>(),
        consecutiveUnansweredCount: 0,
        currentQuestionAnswered: false,
        version: 1,
        finalMessageSent: false,
      };

      this.sessions.set(chatId, session);

      // Bazaga yozishni kutamiz. Agar xato yuz bersa, sessiyani tozalab xatoni yuqoriga chiqaramiz
      try {
        await this.sessionStorage.saveSession(session);
      } catch (saveErr) {
        this.sessions.delete(chatId);
        console.error(`[QuizManager] startQuiz paytida sessiyani saqlashda xatolik (chatId: ${chatId}):`, saveErr);
        throw saveErr;
      }

      const timePerQuestion = quiz.questions[0]?.timeLimitSeconds || 20;

      // Chatga e'lon xabari
      await api.sendMessage(
        chatId,
        `🧪 <b>«${escapeHtml(quiz.title)}» boshlandi!</b>\n\n` +
          `📝 ${escapeHtml(quiz.description)}\n` +
          `❓ Savollar soni: <b>${quiz.questions.length} ta</b>\n` +
          `⏱ Har bir savolga: <b>${timePerQuestion} soniya</b>\n\n` +
          `<i>Tayyor turing, 1-savol 3 soniyadan so'ng yuboriladi...</i>`,
        { parse_mode: "HTML" }
      );

      console.log(
        `[Quiz] Chatda yangi quiz boshlandi (chatId: ${chatId}, savollar soni: ${quiz.questions.length})`
      );

      // 3 soniyadan keyin 1-savol yuboriladi
      session.timer = setTimeout(async () => {
        await this.sendNextQuestion(chatId, api);
      }, 3000);

      return { success: true, message: "Quiz muvaffaqiyatli boshlandi!" };
    } finally {
      this.chatLocks.delete(chatId);
    }
  }

  /**
   * Aqlli pauza: Ketma-ket 3 ta savolga hech kim javob bermasa quizni vaqtincha to'xtatish
   */
  public async pauseQuiz(chatId: number, api: TelegramApiSender): Promise<void> {
    const session = this.sessions.get(chatId);
    if (!session || session.status !== "running") return;

    this.clearSessionTimer(session);
    session.status = "paused";
    session.currentPollId = null;
    session.currentPollMessageId = null;
    session.version += 1;

    await this.sessionStorage.saveSession(session);

    const questionNumber = session.currentQuestionIndex + 1;
    const totalQuestions = session.quiz.questions.length;

    const pauseText =
      `⏸ <b>Quiz vaqtincha to‘xtatildi (Aqlli pauza)</b>\n\n` +
      `Ketma-ket 3 ta savolga hech kim javob bermagani sababli quiz to‘xtatildi.\n` +
      `O‘tilgan savollar: <b>${questionNumber}/${totalQuestions}</b>\n\n` +
      `Quizni qolgan joyidan davom ettirish uchun quyidagi tugmani bosing yoki guruhda <b>/resume</b> buyrug‘ini yuboring:`;

    await api.sendMessage(chatId, pauseText, {
      parse_mode: "HTML",
      reply_markup: {
        inline_keyboard: [
          [
            {
              text: "▶️ Qolgan joyidan davom ettirish",
              callback_data: `resume_quiz_${chatId}_${session.sessionId}`,
            },
          ],
        ],
      },
    });

    console.log(`[Quiz] Chat ${chatId} da quiz pauzalandi (${questionNumber}/${totalQuestions})`);
  }

  /**
   * Pauzadagi quizni qolgan joyidan (keyingi savoldan) davom ettirish
   */
  public async resumeQuiz(
    chatId: number,
    api: TelegramApiSender,
    expectedSessionId?: string
  ): Promise<{ success: boolean; message: string }> {
    if (this.chatLocks.has(chatId)) {
      return { success: false, message: "⚠️ Amal bajarilmoqda, iltimos kuting." };
    }
    this.chatLocks.add(chatId);

    try {
      const session = this.sessions.get(chatId);
      if (!session || session.status !== "paused") {
        return { success: false, message: "⚠️ Quiz allaqachon davom ettirilgan yoki to'xtatilgan." };
      }

      if (expectedSessionId && session.sessionId !== expectedSessionId) {
        return {
          success: false,
          message: "⚠️ Ushbu tugma eski yoki yakunlangan sessiyaga tegishli.",
        };
      }

      this.clearSessionTimer(session);
      session.status = "running";
      session.consecutiveUnansweredCount = 0;
      session.currentQuestionAnswered = false;
      session.version += 1;

      await this.sessionStorage.saveSession(session);

      const nextQuestionNumber = session.currentQuestionIndex + 2;
      const totalQuestions = session.quiz.questions.length;

      await api.sendMessage(
        chatId,
        `▶️ <b>Quiz qolgan joyidan davom ettirilmoqda!</b>\n\n` +
          `Davom etish: <b>${nextQuestionNumber}/${totalQuestions}-savol</b>\n` +
          `<i>Tayyor turing, savol 3 soniyadan so‘ng yuboriladi...</i>`,
        { parse_mode: "HTML" }
      );

      console.log(`[Quiz] Chat ${chatId} da quiz davom ettirildi (${nextQuestionNumber}/${totalQuestions})`);

      session.timer = setTimeout(async () => {
        await this.sendNextQuestion(chatId, api);
      }, 3000);

      return { success: true, message: "Quiz muvaffaqiyatli davom ettirildi!" };
    } finally {
      this.chatLocks.delete(chatId);
    }
  }

  /**
   * Keyingi savolni yuborish
   * Telegram yuborish xatosi va DB saqlash xatosi qat'iy alohida boshqariladi.
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

    // 0-BOSQICH: Agar savolda rasm bo'lsa, avval rasmni yuboramiz
    if (q.imagePath) {
      try {
        if (!api.sendPhoto) {
          throw new Error("Telegram API rasm yuborishni qo'llab-quvvatlamaydi");
        }
        const photoPayload =
          typeof q.imagePath === "string" && !q.imagePath.startsWith("http")
            ? new InputFile(q.imagePath)
            : q.imagePath;
        await api.sendPhoto(chatId, photoPayload, {
          caption: `[${questionNumber}/${totalQuestions}]`,
        });
      } catch (photoError: any) {
        console.error(`[QuizManager] Telegramga rasm yuborishda xatolik (chat: ${chatId}):`, photoError);

        // Rasm Telegramga bormadi! Savol indeksi orqaga qaytariladi va poll yuborilmaydi
        session.currentQuestionIndex = Math.max(-1, session.currentQuestionIndex - 1);
        this.clearSessionTimer(session);
        session.status = "paused";
        session.currentPollId = null;
        session.currentPollMessageId = null;
        session.version += 1;

        // Xavfsiz pauza holatini saqlashga urinamiz
        try {
          await this.sessionStorage.saveSession(session);
        } catch (dbErr) {
          console.error(
            `[QuizManager] Rasm xatoligidan so'ng pauza holatini DBga saqlashda ham xatolik (chat: ${chatId}):`,
            dbErr
          );
        }

        const errorMessage =
          photoError?.description || photoError?.message || "Telegram API rasm yuborishda vaqtinchalik xatolik";
        const totalQuestionsCount = session.quiz.questions.length;
        const currentProgress = session.currentQuestionIndex + 1;

        try {
          await api.sendMessage(
            chatId,
            `⚠️ <b>Savol rasmini yuborishda vaqtinchalik xatolik yuz berdi</b>\n\n` +
              `Xatolik sababi: <i>${escapeHtml(errorMessage)}</i>\n` +
              `O‘tilgan savollar holati: <b>${currentProgress}/${totalQuestionsCount}</b>\n` +
              `Ishtirokchilarning barcha ballari va javob vaqtlari to‘liq saqlab qolindi.\n\n` +
              `Muammo bartaraf etilgach, quyidagi tugma yoki guruhda <b>/resume</b> buyrug'i orqali quizni xavfsiz davom ettirishingiz mumkin:`,
            {
              parse_mode: "HTML",
              reply_markup: {
                inline_keyboard: [
                  [
                    {
                      text: "▶️ Qolgan joyidan davom ettirish",
                      callback_data: `resume_quiz_${chatId}_${session.sessionId}`,
                    },
                  ],
                ],
              },
            }
          );
        } catch (sendMsgErr) {
          console.error(`[QuizManager] Chat ${chatId} ga xatolik xabarini yuborishda ham xatolik:`, sendMsgErr);
        }
        return;
      }
    }

    // 1-BOSQICH: Telegramga poll yuborish
    let message;
    try {
      message = await api.sendPoll(chatId, questionText, q.options, {
        type: "quiz",
        correct_option_ids: [q.correctOptionId],
        is_anonymous: false, // Foydalanuvchilarni aniqlash uchun noanonim poll
        explanation: q.explanation,
        open_period: q.timeLimitSeconds, // Telegramning rasmiy taymeri
      });
    } catch (telegramError: any) {
      console.error(`[QuizManager] Telegramga savol yuborishda xatolik (chat: ${chatId}):`, telegramError);

      // Savol Telegramga bormadi! Faqat shu holatda savol indeksi orqaga qaytariladi
      session.currentQuestionIndex = Math.max(-1, session.currentQuestionIndex - 1);
      this.clearSessionTimer(session);
      session.status = "paused";
      session.currentPollId = null;
      session.currentPollMessageId = null;
      session.version += 1;

      // Xavfsiz pauza holatini saqlashga urinamiz (agar DB ham ishlamasa xato ushlanadi)
      try {
        await this.sessionStorage.saveSession(session);
      } catch (dbErr) {
        console.error(
          `[QuizManager] Telegram xatoligidan so'ng pauza holatini DBga saqlashda ham xatolik (chat: ${chatId}):`,
          dbErr
        );
      }

      const errorMessage = telegramError?.description || telegramError?.message || "Telegram API vaqtinchalik xatoligi";
      const totalQuestionsCount = session.quiz.questions.length;
      const currentProgress = session.currentQuestionIndex + 1;

      try {
        await api.sendMessage(
          chatId,
          `⚠️ <b>Savol yuborishda vaqtinchalik xatolik yuz berdi</b>\n\n` +
            `Xatolik sababi: <i>${escapeHtml(errorMessage)}</i>\n` +
            `O‘tilgan savollar holati: <b>${currentProgress}/${totalQuestionsCount}</b>\n` +
            `Ishtirokchilarning barcha ballari va javob vaqtlari to‘liq saqlab qolindi.\n\n` +
            `Muammo bartaraf etilgach, quyidagi tugma yoki guruhda <b>/resume</b> buyrug'i orqali quizni xavfsiz davom ettirishingiz mumkin:`,
          {
            parse_mode: "HTML",
            reply_markup: {
              inline_keyboard: [
                [
                  {
                    text: "▶️ Qolgan joyidan davom ettirish",
                    callback_data: `resume_quiz_${chatId}_${session.sessionId}`,
                  },
                ],
              ],
            },
          }
        );
      } catch (sendMsgErr) {
        console.error(`[QuizManager] Chat ${chatId} ga xatolik xabarini yuborishda ham xatolik:`, sendMsgErr);
      }
      return;
    }

    // 2-BOSQICH: Poll Telegramga muvaffaqiyatli yuborildi!
    console.log(
      `[Quiz] ${questionNumber}/${totalQuestions}-savol yuborildi (chatId: ${chatId}, pollId: ${message.poll.id}, vaqt: ${q.timeLimitSeconds}s)`
    );

    session.currentQuestionAnswered = false;
    session.currentPollId = message.poll.id;
    session.currentPollMessageId = message.message_id;
    session.questionStartTime = Date.now();
    session.version += 1;

    // poll_id xaritasiga saqlaymiz (isClosed: false)
    this.pollToSession.set(message.poll.id, {
      chatId,
      questionIndex: session.currentQuestionIndex,
      correctOptionId: q.correctOptionId,
      startTime: session.questionStartTime,
      isClosed: false,
    });

    // Vaqt tugagach savolni yopish va keyingisiga o'tish taymerini o'rnatamiz (chunki poll Telegramda faol!)
    session.timer = setTimeout(async () => {
      await this.handleQuestionTimeout(chatId, api);
    }, (q.timeLimitSeconds + 1) * 1000);

    // 3-BOSQICH: Sessiya holatini DBga saqlash
    try {
      await this.sessionStorage.saveSession(session);
    } catch (dbErr) {
      console.error(
        `[QuizManager] Poll ${message.poll.id} guruhga yuborildi, ammo sessiyani DBga saqlashda xatolik yuz berdi (chatId: ${chatId}):`,
        dbErr
      );
      // DIQQAT: Poll allaqachon Telegramda ochiq! Savol indeksini orqaga qaytarmaymiz va pollni izsiz qoldirmaymiz.
      // Savol xotirada faol qoladi, ishtirokchilar javob bera oladi.
      // Keyingi muvaffaqiyatli saveSession (javob yoki timeoutda) yangi versiya bilan DBni sinxronlashtiradi.
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

    // Savolga hech kim javob bermaganligini tekshirish
    if (!session.currentQuestionAnswered) {
      session.consecutiveUnansweredCount = (session.consecutiveUnansweredCount || 0) + 1;
      console.log(
        `[Quiz] Chat ${chatId} da ketma-ket javobsiz savol (#${session.consecutiveUnansweredCount}): ${session.currentQuestionIndex + 1}-savol`
      );
    } else {
      session.consecutiveUnansweredCount = 0;
    }

    // Sessiya holatini saqlash
    session.version += 1;
    try {
      await this.sessionStorage.saveSession(session);
    } catch (saveErr) {
      console.error(`[QuizManager] handleQuestionTimeout saqlashda xatolik (chatId: ${chatId}):`, saveErr);
    }

    // Oxirgi savoldan keyin savollar tugagan bo'lsa, pauza o'rniga yakuniy natija chiqsin
    const isLastQuestion = session.currentQuestionIndex >= session.quiz.questions.length - 1;
    if (isLastQuestion) {
      session.timer = setTimeout(async () => {
        await this.finishQuiz(chatId, api);
      }, 2000);
      return;
    }

    // Ketma-ket 3 ta savolga hech kim javob bermasa: Aqlli pauza!
    if (session.consecutiveUnansweredCount >= 3) {
      session.timer = setTimeout(async () => {
        await this.pauseQuiz(chatId, api);
      }, 2000);
      return;
    }

    // 2 soniya pauza (foydalanuvchilar to'g'ri javob va izohni ko'rib olishlari uchun)
    session.timer = setTimeout(async () => {
      await this.sendNextQuestion(chatId, api);
    }, 2000);
  }

  /**
   * Foydalanuvchi poll'da ovoz berganda (poll_answer hodisasi).
   * Muvaffaqiyatsiz save'dan keyin xotira to'liq rollback qilinadi.
   * Shunday qilib Telegram update retry qilganda javob yo'qolmaydi va takroriy hisoblanmaydi.
   */
  public async handlePollAnswer(answer: PollAnswerData): Promise<boolean> {
    const pollInfo = this.pollToSession.get(answer.pollId);
    if (!pollInfo) {
      return false;
    }

    // Per-chat BUTUN read-modify-write operatsiyasini qat'iy navbatga (serialize) qo'yamiz.
    // Bu orqali ikki parallel kelgan javob xotirani buzishi yoki bittasining rollback'i ikkinchisini yuvib ketishi 100% oldi olinadi.
    return this.enqueueChatOp(pollInfo.chatId, async () => {
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

      // XOTIRA HOLATINI SNAPSHOT QILISH (DB save xato berganda to'liq rollback qilish uchun)
      const prevConsecutiveUnanswered = session.consecutiveUnansweredCount;
      const prevCurrentQuestionAnswered = session.currentQuestionAnswered;
      const prevVersion = session.version;
      const existingParticipant = session.participants.get(answer.user.id);
      const prevParticipantSnapshot = existingParticipant ? { ...existingParticipant } : null;

      // Xotirada o'zgarishlarni qo'llaymiz
      session.answeredUsers.add(dedupKey);
      session.currentQuestionAnswered = true;
      session.consecutiveUnansweredCount = 0;

      // Javob berish vaqti
      const responseTimeMs = Math.max(0, Date.now() - pollInfo.startTime);

      // To'g'riligini tekshirish
      const isCorrect = answer.optionIds.includes(pollInfo.correctOptionId);

      let participant = existingParticipant;
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
      session.version += 1;

      try {
        // Sessiyani yangilab saqlash
        await this.sessionStorage.saveSession(session);
      } catch (saveErr) {
        // ROLLBACK: DB yozuvi xato bersa, xotira holatini to'liq avvalgi holatga qaytaramiz!
        session.answeredUsers.delete(dedupKey);
        session.consecutiveUnansweredCount = prevConsecutiveUnanswered;
        session.currentQuestionAnswered = prevCurrentQuestionAnswered;
        session.version = prevVersion;

        if (prevParticipantSnapshot) {
          session.participants.set(answer.user.id, prevParticipantSnapshot);
        } else {
          session.participants.delete(answer.user.id);
        }

        console.error(`[QuizManager] handlePollAnswer saveSession xatoligi (chat: ${pollInfo.chatId}):`, saveErr);
        throw saveErr; // Telegram Webhook retry qilishi uchun xatoni yuqoriga chiqaramiz!
      }

      const userDisplay = answer.user.username ? `@${answer.user.username}` : answer.user.first_name;
      console.log(
        `[Quiz] Javob qabul qilindi: ${userDisplay} (chatId: ${pollInfo.chatId}, savol: ${pollInfo.questionIndex + 1}, to'g'ri: ${isCorrect}, vaqt: ${(responseTimeMs / 1000).toFixed(1)}s)`
      );

      return true;
    });
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
   * Quiz natijalarini PostgreSQL bazasiga ishonchli saqlash (retry bilan).
   * session_id + user_id bo'yicha dublikatlardan himoyalangan.
   */
  public async saveQuizResultsWithRetry(
    session: QuizSession,
    leaderboard: ParticipantScore[],
    maxRetries = 3
  ): Promise<void> {
    if (leaderboard.length === 0) return;

    const usesFirestore = this.sessionStorage instanceof FirestoreSessionStorage ||
      (this.sessionStorage instanceof SessionStorage && this.sessionStorage.isUsingFirestore());
    const customDb = (this.sessionStorage as any)?.getCustomDb?.();
    const firestore = usesFirestore ? (customDb || getFirestoreDb()) : null;
    if (usesFirestore && !firestore) {
      throw new Error("[QuizManager] Firestore sessiyasi uchun natijalar bazasi mavjud emas.");
    }
    if (firestore) {
      const resultsCol = this.resultsCollectionName || FIRESTORE_COLLECTIONS.RESULTS;
      const BATCH_SIZE = 400; // Firestore limit 500 dan xavfsiz pastda bo'laklash
      for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
          for (let i = 0; i < leaderboard.length; i += BATCH_SIZE) {
            const chunk = leaderboard.slice(i, i + BATCH_SIZE);
            const batch = firestore.batch();
            for (const p of chunk) {
              // session_id + user_id orqali idempotent yagona hujjat IDsi:
              const docId = `${session.sessionId}_${p.userId}`;
              const docRef = firestore.collection(resultsCol).doc(docId);
              batch.set(
                docRef,
                {
                  sessionId: session.sessionId,
                  quizId: session.quiz.id,
                  chatId: session.chatId,
                  userId: p.userId,
                  firstName: p.firstName,
                  username: p.username || null,
                  score: p.score,
                  totalQuestions: session.quiz.questions.length,
                  totalTimeMs: p.totalTimeMs,
                  answersCount: p.answersCount,
                  createdAt: new Date().toISOString(),
                },
                { merge: true }
              );
            }
            await batch.commit();
          }
          return; // Barcha bo'laklar muvaffaqiyatli saqlandi!
        } catch (err) {
          console.error(`[QuizManager] quiz_results Firestorega saqlashda xatolik (urinish ${attempt}/${maxRetries}):`, err);
          if (attempt === maxRetries) {
            throw new Error(
              `[QuizManager] quiz_results saqlash ${maxRetries} urinishdan keyin ham muvaffaqiyatsiz bo'ldi: ${(err as Error).message}`
            );
          }
          await new Promise((r) => setTimeout(r, 100 * attempt));
        }
      }
      return;
    }

    const pool = getDatabasePool();
    if (!pool) {
      if (process.env.NODE_ENV === "production") {
        throw new Error("[QuizManager] Firestore ma'lumotlar bazasi topilmadi yoki ulanmagan!");
      }
      return;
    }

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      let client;
      try {
        client = await pool.connect();
        await client.query("BEGIN");

        for (const p of leaderboard) {
          await client.query(
            `INSERT INTO quiz_results (
              session_id, quiz_id, chat_id, user_id, first_name, username, score, total_questions, total_time_ms, answers_count
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (session_id, user_id) DO UPDATE SET
              score = EXCLUDED.score,
              total_questions = EXCLUDED.total_questions,
              total_time_ms = EXCLUDED.total_time_ms,
              answers_count = EXCLUDED.answers_count,
              first_name = EXCLUDED.first_name,
              username = EXCLUDED.username`,
            [
              session.sessionId,
              session.quiz.id,
              session.chatId,
              p.userId,
              p.firstName,
              p.username || null,
              p.score,
              session.quiz.questions.length,
              p.totalTimeMs,
              p.answersCount,
            ]
          );
        }

        await client.query("COMMIT");
        return; // Muvaffaqiyatli saqlandi
      } catch (err) {
        if (client) {
          try {
            await client.query("ROLLBACK");
          } catch {
            // rollback xatosi e'tiborsiz qoldiriladi
          }
        }
        console.error(`[QuizManager] quiz_results saqlashda xatolik (urinish ${attempt}/${maxRetries}):`, err);
        if (attempt === maxRetries) {
          throw new Error(
            `[QuizManager] quiz_results saqlash ${maxRetries} urinishdan keyin ham muvaffaqiyatsiz bo'ldi: ${(err as Error).message}`
          );
        }
        await new Promise((r) => setTimeout(r, 100 * attempt));
      } finally {
        if (client) {
          client.release();
        }
      }
    }
  }

  /**
   * Yakuniy natija xabarini ixcham shaklda (eng yuqori 8 ishtirokchi) shakllantirish.
   * Natija bitta Telegram xabari bo'lib, umumiy qatnashchilar soni, muallif, manba va tugmalarni o'z ichiga oladi.
   * Agar 4096 belgilik limitdan oshsa, 8 dan ham kamroq satr ko'rsatiladi.
   */
  public formatLeaderboardMessages(session: QuizSession, leaderboard: ParticipantScore[]): string[] {
    const totalQuestions = session.quiz.questions.length;
    let footer = `\nBarcha ishtirokchilarga qatnashganlari uchun tashakkur! 👏\n\nTest yaratuvchisi: <a href="https://t.me/diyorbek_jabborov">@diyorbek_jabborov</a>`;
    if (session.quiz.source) {
      footer += `\nSavollar manbasi: ${escapeHtml(session.quiz.source)}`;
    }

    if (leaderboard.length === 0) {
      let text = `🏁 <b>«${escapeHtml(session.quiz.title)}» yakunlandi!</b>\n\n`;
      text += `👥 Qatnashchilar soni: <b>0 ta</b>\n\n`;
      text += `Afsuski, hech bir ishtirokchi savollarga javob bermadi. 😴\nKeyingi safar faolroq bo'ling!\n\n`;
      text += `Test yaratuvchisi: <a href="https://t.me/diyorbek_jabborov">@diyorbek_jabborov</a>`;
      if (session.quiz.source) {
        text += `\nSavollar manbasi: ${escapeHtml(session.quiz.source)}`;
      }
      return [text];
    }

    const MAX_MESSAGE_LENGTH = 4000; // Telegram 4096 limitidan xavfsiz pastda
    const medals = ["🥇", "🥈", "🥉"];

    // Sarlavha va umumiy qatnashchilar soni
    let header = `🏁 <b>«${escapeHtml(session.quiz.title)}» yakunlandi!</b>\n\n`;
    header += `👥 Qatnashchilar soni: <b>${leaderboard.length} ta</b>\n\n`;
    header += `📊 <b>Yakuniy Natijalar va Reyting:</b>\n\n`;

    const maxEntries = Math.min(8, leaderboard.length);
    const candidateLines: string[] = [];

    for (let index = 0; index < maxEntries; index++) {
      const p = leaderboard[index];
      const medal = index < 3 ? `${medals[index]} ` : `${index + 1}. `;
      const timeSec = (p.totalTimeMs / 1000).toFixed(1);
      const rawName = p.username ? `@${p.username}` : p.firstName + (p.lastName ? ` ${p.lastName}` : "");
      const safeName = escapeHtml(rawName);
      candidateLines.push(`${medal}<b>${safeName}</b>: ${p.score}/${totalQuestions} ball (jami javob vaqti: ${timeSec}s)\n`);
    }

    let linesToShow: string[] = [];
    for (let i = 0; i < candidateLines.length; i++) {
      const testContent = header + [...linesToShow, candidateLines[i]].join("") + footer;
      if (testContent.length <= MAX_MESSAGE_LENGTH) {
        linesToShow.push(candidateLines[i]);
      } else {
        break; // Agar 4096 belgiga sig'masa, 8 dan ham kamroq satr ko'rsatiladi
      }
    }

    const fullMessage = (header + linesToShow.join("") + footer).trimEnd();
    return [fullMessage];
  }

  /**
   * Quizni muvaffaqiyatli yakunlash va natijalarni e'lon qilish.
   *
   * Ketma-ketlik:
   * 1. Sessiya statusi "finishing" ga o'tkaziladi va DBga saqlanadi (bu chatda yangi quiz boshlanishi bloklanadi).
   * 2. Natijalar bazaga (quiz_results) ishonchli saqlanadi (retry bilan).
   * 3. Faqat natijalar bazada kafolatlanganidan so'ng natija xabari e'lon qilinadi (bo'laklab, takroriy yuborilmaydi).
   * 4. Xabar yuborilgach `finalMessageSent=true` DBga yoziladi, so'ngra sessiya o'chiriladi.
   */
  public async finishQuiz(chatId: number, api: TelegramApiSender): Promise<void> {
    const session = this.sessions.get(chatId);
    if (!session) return;

    this.clearSessionTimer(session);
    session.status = "finishing";
    session.version += 1;

    // Barcha savollarni yopilgan deb belgilaymiz
    if (session.currentPollId) {
      const pollInfo = this.pollToSession.get(session.currentPollId);
      if (pollInfo) {
        pollInfo.isClosed = true;
      }
    }

    // Finishing holatini bazaga saqlaymiz (xatolik yutilmaydi!)
    await this.sessionStorage.saveSession(session);

    const leaderboard = this.getLeaderboard(chatId);
    console.log(
      `[Quiz] Quiz yakunlanmoqda (chatId: ${chatId}). Ishtirokchilar soni: ${leaderboard.length}`
    );

    // 1-QADAM: Avval natijalarni bazaga (quiz_results) ishonchli saqlaymiz!
    try {
      await this.saveQuizResultsWithRetry(session, leaderboard, 3);
    } catch (saveResultsErr) {
      console.error(
        `[QuizManager] Natijalar bazaga yozilmadi! Ma'lumot yo'qolmasligi uchun sessiya o'chirilmadi (chatId: ${chatId}):`,
        saveResultsErr
      );
      // Natija bazaga yozilmagan taqdirda xabar yuborilmaydi va sessiya finishing holatida qoladi
      // isQuizActive true qaytaradi, shu sababli boshqa odam yangi quiz boshlay olmaydi!
      throw saveResultsErr;
    }

    // 2-QADAM: Natijalar bazaga muvaffaqiyatli saqlangach, natija xabari e'lon qilinadi
    // Agar avval xabar yuborilgan bo'lsa (masalan qayta urinishda), xabar takrorlanmasin
    if (!session.finalMessageSent) {
      const messages = this.formatLeaderboardMessages(session, leaderboard);

      // Yakuniy xabar ostidagi tugmalar (faqat oxirgi bo'lakka biriktiriladi)
      const replyMarkup = {
        inline_keyboard: [
          [
            {
              text: "📢 Quiz kodlari",
              url: "https://t.me/jdaquizkod",
            },
            {
              text: "🔄 Qayta yechish",
              callback_data: `restart_quiz_${session.quiz.id}`,
            },
          ],
        ],
      };

      try {
        const message = messages[0];
        await api.sendMessage(chatId, message, {
          parse_mode: "HTML",
          reply_markup: replyMarkup,
        });
        session.finalMessageSent = true;
        session.sentChunksCount = 1;
        session.version += 1;
        // Xabar muvaffaqiyatli yuborilgach, restartda qayta yuborilmasligi uchun DBga saqlaymiz:
        await this.sessionStorage.saveSession(session);
      } catch (sendErr) {
        console.error(`[QuizManager] Natija xabarini yuborishda xatolik (chatId: ${chatId}):`, sendErr);
        // DIQQAT: Xabar yuborish yoki DB saqlash muvaffaqiyatsiz bo'lsa sessiyani O'CHIRMAYMIZ!
        // Sessiya finishing holatida qoladi va qayta urinish imkoniyati saqlanadi.
        throw sendErr;
      }
    }

    // 3-QADAM: Hammasi muvaffaqiyatli yakunlandi, endi sessiyani tozalaymiz
    session.status = "completed";
    await this.sessionStorage.deleteSession(chatId);
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
    session.version += 1;
    await this.sessionStorage.deleteSession(chatId);
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
