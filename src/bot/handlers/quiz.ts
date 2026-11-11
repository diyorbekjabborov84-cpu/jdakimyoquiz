import { Context } from "grammy";
import { getQuizById } from "../../quiz/questions.js";
import { quizManager } from "../../quiz/quizManager.js";
import { isGroupAdmin } from "../guards/adminGuard.js";
import { checkGroupSize } from "../guards/groupSizeGuard.js";
import { trackGroupEvent } from "../../tracking/tracker.js";
import {
  resolveShell,
  replyGroupDisabledOnce,
  replyPrivateNotParticipant,
} from "../../shell/shell.js";
import { getKursQuizById, isKursQuizId } from "../../kurs/kursRepository.js";
import { getBotSettings } from "../../settings/botSettings.js";
import { buildAsosiyMenuPayload, buildKursMenuPayload } from "./menu.js";

/**
 * /quiz buyrug'i uchun handler:
 * - Argumentsiz (/quiz) yuborilsa: joriy qobiqqa mos inline menyuni ochadi
 * - Argument bilan (/quiz <id>) yuborilsa: o'sha quizni boshlaydi
 */
export async function handleQuizCommand(ctx: Context): Promise<void> {
  const shell = await resolveShell(ctx);
  if (shell.shell === "yopiq") {
    if (shell.reason === "group_disabled") {
      await replyGroupDisabledOnce(ctx);
    } else {
      await replyPrivateNotParticipant(ctx, shell.reason);
    }
    return;
  }

  const matchText = typeof ctx.match === "string" ? ctx.match.trim() : "";
  const messageText = ctx.message?.text || "";
  const parts = messageText.trim().split(/\s+/);
  const arg = matchText || (parts.length > 1 ? parts[1] : "");

  if (arg) {
    await startQuizById(ctx, arg);
    return;
  }

  if (shell.shell === "kurs") {
    const menu = buildKursMenuPayload(0);
    await ctx.reply(menu.text, {
      parse_mode: "HTML",
      reply_markup: menu.reply_markup,
    });
    return;
  }

  const menu = buildAsosiyMenuPayload();
  await ctx.reply(menu.text, {
    parse_mode: "HTML",
    reply_markup: menu.reply_markup,
  });
}

/**
 * /quiz_<ID> yoki /start_<ID> buyruqlari uchun handler
 */
export async function handleQuizByIdCommand(ctx: Context): Promise<void> {
  const match = ctx.match;
  let quizId = "";
  if (Array.isArray(match) && typeof match[1] === "string") {
    quizId = match[1].trim();
  } else if (typeof match === "string" && match.trim()) {
    quizId = match.trim().replace(/^\/?(quiz_|start_)/i, "");
  } else {
    const text = ctx.message?.text || "";
    const command = text.trim().split(/\s+/)[0] || "";
    const withoutBotName = command.split("@")[0];
    quizId = withoutBotName.replace(/^\/(quiz_|start_)/i, "");
  }

  await startQuizById(ctx, quizId);
}

/**
 * Berilgan quizId bo'yicha quizni boshlash yordamchi funksiyasi.
 * Qobiq izolatsiyasi (asosiy vs kurs) va guruh hajmi (faqat asosiy guruhda >= 12) tekshiriladi.
 */
export async function startQuizById(
  ctx: Context,
  quizId: string,
  options?: { fromCallback?: boolean; callbackSuccessText?: string }
): Promise<void> {
  const chatType = ctx.chat?.type;
  const chatId = ctx.chat?.id;
  const isCallback = Boolean(options?.fromCallback || ctx.callbackQuery);

  if (!chatId) return;

  if (chatType === "group" || chatType === "supergroup") {
    void trackGroupEvent(chatId, {
      title: (ctx.chat as any)?.title || "Guruh",
      type: chatType,
      status: "active",
    });
  }

  const shell = await resolveShell(ctx);
  if (shell.shell === "yopiq") {
    if (shell.reason === "group_disabled") {
      await replyGroupDisabledOnce(ctx);
    } else {
      await replyPrivateNotParticipant(ctx, shell.reason);
    }
    return;
  }

  const sendFeedback = async (msg: string, alert = true) => {
    if (isCallback) {
      await ctx.answerCallbackQuery({ text: msg, show_alert: alert }).catch(() => {});
    } else {
      await ctx.reply(msg);
    }
  };

  // Qobiq bo'yicha qat'iy izolatsiya va quizni topish
  let quiz;
  if (shell.shell === "kurs") {
    if (!isKursQuizId(quizId)) {
      await sendFeedback("⚠️ Bu chatda faqat «Kimyo 0 dan» kursi testlari ishlaydi.");
      return;
    }
    const baseKursQuiz = getKursQuizById(quizId);
    if (!baseKursQuiz) {
      await sendFeedback(`❌ Bunday kurs testi topilmadi: «${quizId}»`);
      return;
    }
    const settings = await getBotSettings();
    const kursTimeSec = settings.kursQuestionTimeSeconds || 25;
    quiz = {
      ...baseKursQuiz,
      questions: baseKursQuiz.questions.map((q) => ({
        ...q,
        timeLimitSeconds: kursTimeSec,
      })),
    };
  } else {
    // shell.shell === "asosiy"
    if (isKursQuizId(quizId)) {
      await sendFeedback(
        "❌ Bu test faqat «Kimyo 0 dan» kursi guruhlari va ishtirokchilari uchun mo‘ljallangan."
      );
      return;
    }
    quiz = getQuizById(quizId);
    if (!quiz) {
      await sendFeedback(
        `❌ Bunday IDga ega quiz topilmadi: «${quizId}»\n\nMavjud quizlarni ko'rish uchun /quiz buyrug'ini yuboring.`
      );
      return;
    }

    // Guruh hajmi (>= 12 kishi) FAQAT asosiy guruhlarga tatbiq etiladi (Q5)
    const groupSize = await checkGroupSize(ctx);
    if (!groupSize.allowed) {
      await sendFeedback(groupSize.message);
      return;
    }
  }

  if (quizManager.isQuizActive(chatId)) {
    const isPaused = quizManager.isQuizPaused(chatId);
    const activeMsg = isPaused
      ? "⚠️ Bu chatda pauza qilingan quiz mavjud. Iltimos, uni «▶️ Qolgan joyidan davom ettirish» tugmasi yoki /resume buyrug'i bilan davom ettiring, yoki /stop buyrug'i bilan to'xtating."
      : "⚠️ Bu chatda allaqachon faol quiz davom etmoqda. Iltimos, u yakunlanishini kuting yoki /stop buyrug'i bilan to'xtating.";
    await sendFeedback(activeMsg);
    return;
  }

  const result = await quizManager.startQuiz(chatId, quiz, ctx.api as any);
  if (!result.success) {
    await sendFeedback(result.message);
    return;
  }

  if (isCallback) {
    await ctx
      .answerCallbackQuery({ text: options?.callbackSuccessText || "▶️ Test boshlanmoqda!" })
      .catch(() => {});
  }
}

/**
 * Eski «✅ A’zo bo‘ldim — tekshirish» inline tugmasi uchun handler (3.1):
 * Eski xabarlardagi tugmalar xato bermasligi uchun saqlanadi.
 */
export async function handleCheckSubscriptionCallback(ctx: Context): Promise<void> {
  await ctx.answerCallbackQuery({
    text: "Obuna endi talab qilinmaydi",
  });
}

/**
 * «🔄 Qayta yechish» inline tugmasi bosilganda (callback_data: restart_quiz_<quizId>)
 */
export async function handleRestartQuizCallback(ctx: Context): Promise<void> {
  const data = ctx.callbackQuery?.data || "";
  const quizId = data.replace(/^restart_quiz_/, "");
  await startQuizById(ctx, quizId, {
    fromCallback: true,
    callbackSuccessText: "🔄 Quiz qayta boshlanmoqda!",
  });
}

/**
 * /resume buyrug'i — Pauzadagi quizni qolgan joyidan davom ettirish.
 */
export async function handleResumeQuizCommand(ctx: Context): Promise<void> {
  const chatId = ctx.chat?.id;
  if (!chatId) return;

  const shell = await resolveShell(ctx);
  if (shell.shell === "yopiq") {
    if (shell.reason === "group_disabled") {
      await replyGroupDisabledOnce(ctx);
    } else {
      await replyPrivateNotParticipant(ctx, shell.reason);
    }
    return;
  }

  if (!quizManager.isQuizPaused(chatId)) {
    await ctx.reply("ℹ️ Hozirda pauza qilingan quiz mavjud emas.");
    return;
  }

  const session = quizManager.getSession(chatId);
  if (session) {
    const isSessionKurs = isKursQuizId(session.quiz.id);
    if (shell.shell === "kurs" && !isSessionKurs) {
      await ctx.reply("⚠️ Bu chatda faqat «Kimyo 0 dan» kursi testlari ishlaydi.");
      return;
    }
    if (shell.shell === "asosiy" && isSessionKurs) {
      await ctx.reply("⚠️ Kurs testini asosiy guruhda davom ettirib bo'lmaydi.");
      return;
    }
  }

  if (shell.shell === "asosiy") {
    const groupSize = await checkGroupSize(ctx);
    if (!groupSize.allowed) {
      await ctx.reply(groupSize.message);
      return;
    }
  }

  const res = await quizManager.resumeQuiz(chatId, ctx.api as any);
  if (!res.success) {
    await ctx.reply(res.message);
  }
}

export const handleResumeCommand = handleResumeQuizCommand;

/**
 * «▶️ Qolgan joyidan davom ettirish» inline tugmasi bosilganda
 * Format: resume_quiz_<chatId>_<sessionId>
 */
export async function handleResumeQuizCallback(ctx: Context): Promise<void> {
  const chatId = ctx.chat?.id;
  if (!chatId) {
    await ctx.answerCallbackQuery({
      text: "⚠️ Bu tugma faqat tegishli chatda ishlaydi.",
      show_alert: true,
    });
    return;
  }

  const data = ctx.callbackQuery?.data || "";
  const match = data.match(/^resume_quiz_(-?\d+)_(.+)$/);
  if (!match) {
    await ctx.answerCallbackQuery({
      text: "⚠️ Ushbu tugma eski yoki yaroqsiz sessiyaga tegishli.",
      show_alert: true,
    });
    return;
  }

  const targetChatId = Number(match[1]);
  const expectedSessionId = match[2];

  if (targetChatId !== chatId) {
    await ctx.answerCallbackQuery({
      text: "⚠️ Bu tugma boshqa chatdagi quizga tegishli.",
      show_alert: true,
    });
    return;
  }

  const shell = await resolveShell(ctx);
  if (shell.shell === "yopiq") {
    if (shell.reason === "group_disabled") {
      await replyGroupDisabledOnce(ctx);
    } else {
      await replyPrivateNotParticipant(ctx, shell.reason);
    }
    return;
  }

  const session = quizManager.getSession(chatId);
  if (session) {
    const isSessionKurs = isKursQuizId(session.quiz.id);
    if (shell.shell === "kurs" && !isSessionKurs) {
      await ctx.answerCallbackQuery({
        text: "⚠️ Bu chatda faqat «Kimyo 0 dan» kursi testlari ishlaydi.",
        show_alert: true,
      });
      return;
    }
    if (shell.shell === "asosiy" && isSessionKurs) {
      await ctx.answerCallbackQuery({
        text: "⚠️ Kurs testini asosiy guruhda davom ettirib bo'lmaydi.",
        show_alert: true,
      });
      return;
    }
  }

  if (shell.shell === "asosiy") {
    const groupSize = await checkGroupSize(ctx);
    if (!groupSize.allowed) {
      await ctx.answerCallbackQuery({
        text: groupSize.message,
        show_alert: true,
      });
      return;
    }
  }

  const res = await quizManager.resumeQuiz(chatId, ctx.api as any, expectedSessionId);
  if (!res.success) {
    await ctx.answerCallbackQuery({
      text: res.message,
      show_alert: true,
    });
    return;
  }

  await ctx.answerCallbackQuery({
    text: "▶️ Quiz davom ettirilmoqda!",
  });
}

/**
 * /stop va /stopquiz buyrug'i uchun handler.
 * Guruhda: faqat guruh administratorlari to'xtata oladi.
 * Shaxsiy chatda (Q6): foydalanuvchi o'z quizini admin tekshiruvisiz to'xtata oladi.
 */
export async function handleStopQuizCommand(ctx: Context): Promise<void> {
  const chatType = ctx.chat?.type;
  const chatId = ctx.chat?.id;

  if (!chatId) return;

  if (chatType === "private") {
    if (!quizManager.isQuizActive(chatId)) {
      const shell = await resolveShell(ctx);
      if (shell.shell === "yopiq") {
        if (shell.reason === "group_disabled") {
          await replyGroupDisabledOnce(ctx);
        } else {
          await replyPrivateNotParticipant(ctx, shell.reason);
        }
        return;
      }
      await ctx.reply("ℹ️ Hozirda faol quiz yo'q.");
      return;
    }
    await quizManager.stopQuiz(chatId, ctx.api as any);
    return;
  }

  if (chatType !== "group" && chatType !== "supergroup") {
    return;
  }

  if (!quizManager.isQuizActive(chatId)) {
    const shell = await resolveShell(ctx);
    if (shell.shell === "yopiq") {
      await replyGroupDisabledOnce(ctx);
      return;
    }
  }

  const admin = await isGroupAdmin(ctx);
  if (!admin) {
    await ctx.reply("⛔ Quizni to'xtatish huquqi faqat guruh adminlariga berilgan!");
    return;
  }

  if (!quizManager.isQuizActive(chatId)) {
    await ctx.reply("ℹ️ Hozir bu guruhda faol quiz mavjud emas.");
    return;
  }

  await quizManager.stopQuiz(chatId, ctx.api as any);
}
