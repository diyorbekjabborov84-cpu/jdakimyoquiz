import { Context } from "grammy";
import { escapeHtml } from "../../quiz/quizManager.js";
import {
  formatKursQuizId,
  getActiveKursLessons,
  getKursLessonByNumber,
} from "../../kurs/kursRepository.js";
import {
  resolveShell,
  replyGroupDisabledOnce,
  replyPrivateNotParticipant,
} from "../../shell/shell.js";
import { getBotSettings } from "../../settings/botSettings.js";
import { startQuizById } from "./quiz.js";

export interface MenuMessagePayload {
  text: string;
  reply_markup: {
    inline_keyboard: Array<Array<{ text: string; callback_data: string }>>;
  };
}

const PAGE_SIZE = 8;

export function buildKursMenuPayload(page = 0, greetingPrefix = ""): MenuMessagePayload {
  const lessons = getActiveKursLessons();
  const totalPages = Math.max(1, Math.ceil(lessons.length / PAGE_SIZE));
  const safePage = Math.min(Math.max(0, page), totalPages - 1);
  const slice = lessons.slice(safePage * PAGE_SIZE, (safePage + 1) * PAGE_SIZE);

  const keyboard: Array<Array<{ text: string; callback_data: string }>> = [];
  for (const l of slice) {
    const label = `${l.dars}-dars: ${l.mavzu}`;
    keyboard.push([
      {
        text: label.length > 60 ? `${label.slice(0, 57)}...` : label,
        callback_data: `m:k:d:${l.dars}`,
      },
    ]);
  }

  if (totalPages > 1) {
    const navRow: Array<{ text: string; callback_data: string }> = [];
    if (safePage > 0) {
      navRow.push({ text: "⬅️ Oldingi", callback_data: `m:k:p:${safePage - 1}` });
    }
    if (safePage < totalPages - 1) {
      navRow.push({ text: "Keyingi ➡️", callback_data: `m:k:p:${safePage + 1}` });
    }
    if (navRow.length > 0) {
      keyboard.push(navRow);
    }
  }

  const bodyText =
    lessons.length === 0
      ? `📚 <b>«Kimyo 0 dan» — testlar</b>\n\nHozircha dars testlari yuklanmagan.`
      : `📚 <b>«Kimyo 0 dan» — testlar</b>\n\nKerakli darsni tanlang:`;

  return {
    text: greetingPrefix ? `${greetingPrefix}\n\n${bodyText}` : bodyText,
    reply_markup: { inline_keyboard: keyboard },
  };
}

export function buildKursConfirmPayload(
  darsNum: number,
  timeLimitSeconds?: number
): MenuMessagePayload | null {
  const lesson = getKursLessonByNumber(darsNum);
  if (!lesson || !lesson.quiz || lesson.testlarSoni === 0) {
    return null;
  }

  const timeSec = timeLimitSeconds ?? lesson.quiz.questions[0]?.timeLimitSeconds ?? 25;
  const text =
    `📚 <b>${lesson.dars}-dars: ${escapeHtml(lesson.mavzu)}</b>\n\n` +
    `🧪 ${lesson.dars}-dars bo‘yicha test: ${lesson.testlarSoni} savol, har biriga ${timeSec} soniya`;

  return {
    text,
    reply_markup: {
      inline_keyboard: [
        [
          { text: "▶️ Boshlash", callback_data: `m:k:go:${lesson.dars}` },
          { text: "⬅️ Orqaga", callback_data: "m:k:list" },
        ],
      ],
    },
  };
}

export const quizCodesButton = { text: "📢 Test kodlari", url: "https://t.me/jdaquizkod" };

export function buildQuizCodesPayload(greetingPrefix = "") {
  const text = "Test kodlarini @jdaquizkod kanalidan oling.";
  return {
    text: greetingPrefix ? `${greetingPrefix}\n\n${text}` : text,
    reply_markup: { inline_keyboard: [[quizCodesButton]] },
  };
}

async function editOrReplyMenu(ctx: Context, payload: MenuMessagePayload | ReturnType<typeof buildQuizCodesPayload>): Promise<void> {
  if (typeof (ctx as any).editMessageText === "function") {
    try {
      await ctx.editMessageText(payload.text, {
        parse_mode: "HTML",
        reply_markup: payload.reply_markup,
      });
      await ctx.answerCallbackQuery().catch(() => {});
      return;
    } catch (err: any) {
      const desc = String(err?.description || err?.message || "");
      if (desc.includes("message is not modified")) {
        await ctx.answerCallbackQuery().catch(() => {});
        return;
      }
      // Fallback to reply if editMessageText is not supported in mock or message cannot be edited
    }
  }

  await ctx.answerCallbackQuery().catch(() => {});
  await ctx.reply(payload.text, {
    parse_mode: "HTML",
    reply_markup: payload.reply_markup,
  });
}

export async function handleMenuCallback(ctx: Context): Promise<void> {
  const data = ctx.callbackQuery?.data || "";
  if (!data.startsWith("m:")) return;

  const chatId = ctx.chat?.id;
  if (!chatId) {
    await ctx.answerCallbackQuery().catch(() => {});
    return;
  }

  // Har callback kelganda qobiqni qayta tekshiramiz!
  const shell = await resolveShell(ctx);
  if (shell.shell === "yopiq") {
    if (shell.reason === "group_disabled") {
      await replyGroupDisabledOnce(ctx);
    } else {
      await replyPrivateNotParticipant(ctx, shell.reason);
    }
    return;
  }

  // Kurs menyusi callbacklari: m:k:...
  if (data.startsWith("m:k:")) {
    if (shell.shell !== "kurs") {
      await ctx.answerCallbackQuery({
        text: "⚠️ Bu menyu faqat «Kimyo 0 dan» kursi uchun.",
        show_alert: true,
      });
      return;
    }

    if (data === "m:k:list") {
      await editOrReplyMenu(ctx, buildKursMenuPayload(0));
      return;
    }

    if (data.startsWith("m:k:p:")) {
      const page = Number(data.slice("m:k:p:".length)) || 0;
      await editOrReplyMenu(ctx, buildKursMenuPayload(page));
      return;
    }

    if (data.startsWith("m:k:d:")) {
      const darsNum = Number(data.slice("m:k:d:".length));
      const settings = await getBotSettings();
      const payload = buildKursConfirmPayload(darsNum, settings.kursQuestionTimeSeconds);
      if (!payload) {
        await ctx.answerCallbackQuery({
          text: "⚠️ Ushbu dars testi topilmadi.",
          show_alert: true,
        });
        return;
      }
      await editOrReplyMenu(ctx, payload);
      return;
    }

    if (data.startsWith("m:k:go:")) {
      const darsNum = Number(data.slice("m:k:go:".length));
      const quizId = formatKursQuizId(darsNum);
      await startQuizById(ctx, quizId, { fromCallback: true });
      return;
    }
  }

  // Avval yuborilgan asosiy menyu tugmalari kanal havolasini ochishga yo‘naltiradi.
  if (data.startsWith("m:a:")) {
    if (shell.shell === "asosiy") {
      await editOrReplyMenu(ctx, buildQuizCodesPayload());
    } else {
      await ctx.answerCallbackQuery({ text: "Kurs testlarini darslar ro‘yxatidan tanlang." });
    }
  }
}
