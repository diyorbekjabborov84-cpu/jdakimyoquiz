import { Context } from "grammy";
import { allQuizzes, getQuizById } from "../../quiz/questions.js";
import { escapeHtml, quizManager } from "../../quiz/quizManager.js";
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

export interface AsosiySectionDef {
  key: string;
  bolim: string;
  title: string;
}

export const ASOSIY_SECTIONS: AsosiySectionDef[] = [
  { key: "k8", bolim: "kimyo_8", title: "8-sinf kimyo" },
  { key: "kk", bolim: "kolloid", title: "Kolloid kimyo" },
  { key: "org", bolim: "organik", title: "Organik kimyo (I)" },
  { key: "tar", bolim: "tarix", title: "Tarix" },
  { key: "din", bolim: "dinshunoslik", title: "Dinshunoslik" },
  { key: "rus", bolim: "rus_tili", title: "Rus tili" },
  { key: "bsh", bolim: "boshqalar", title: "Boshqalar" },
];

const PAGE_SIZE = 8;

export function getSectionKeyByBolim(bolim?: string): string {
  const found = ASOSIY_SECTIONS.find((s) => s.bolim === bolim);
  return found ? found.key : "bsh";
}

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

export function buildAsosiyMenuPayload(greetingPrefix = ""): MenuMessagePayload {
  const bodyText = `🧪 <b>Testlar bo‘limlari</b>\n\nKerakli bo‘limni tanlang:`;
  return {
    text: greetingPrefix ? `${greetingPrefix}\n\n${bodyText}` : bodyText,
    reply_markup: {
      inline_keyboard: [
        [
          { text: "Kolloid kimyo", callback_data: "m:a:sec:kk" },
          { text: "Organik kimyo (I)", callback_data: "m:a:sec:org" },
        ],
        [
          { text: "Tarix", callback_data: "m:a:sec:tar" },
          { text: "Dinshunoslik", callback_data: "m:a:sec:din" },
        ],
        [
          { text: "Rus tili", callback_data: "m:a:sec:rus" },
          { text: "Boshqalar", callback_data: "m:a:sec:bsh" },
        ],
      ],
    },
  };
}

export function buildAsosiySectionPayload(secKey: string, page = 0): MenuMessagePayload | null {
  const section = ASOSIY_SECTIONS.find((s) => s.key === secKey);
  if (!section) return null;

  const quizzes = allQuizzes.filter((q) => (q.bolim || "boshqalar") === section.bolim);
  const totalPages = Math.max(1, Math.ceil(quizzes.length / PAGE_SIZE));
  const safePage = Math.min(Math.max(0, page), totalPages - 1);
  const slice = quizzes.slice(safePage * PAGE_SIZE, (safePage + 1) * PAGE_SIZE);

  const keyboard: Array<Array<{ text: string; callback_data: string }>> = [];
  for (const q of slice) {
    keyboard.push([
      {
        text: q.title.length > 60 ? `${q.title.slice(0, 57)}...` : q.title,
        callback_data: `m:a:q:${q.id}`,
      },
    ]);
  }

  if (totalPages > 1) {
    const navRow: Array<{ text: string; callback_data: string }> = [];
    if (safePage > 0) {
      navRow.push({ text: "⬅️ Oldingi", callback_data: `m:a:p:${secKey}:${safePage - 1}` });
    }
    if (safePage < totalPages - 1) {
      navRow.push({ text: "Keyingi ➡️", callback_data: `m:a:p:${secKey}:${safePage + 1}` });
    }
    if (navRow.length > 0) {
      keyboard.push(navRow);
    }
  }

  keyboard.push([{ text: "⬅️ Orqaga", callback_data: "m:a:list" }]);

  return {
    text: `📂 <b>${escapeHtml(section.title)}</b>\n\nKerakli testni tanlang:`,
    reply_markup: { inline_keyboard: keyboard },
  };
}

export function buildAsosiyConfirmPayload(quizId: string): MenuMessagePayload | null {
  const quiz = getQuizById(quizId);
  if (!quiz) return null;

  const secKey = getSectionKeyByBolim(quiz.bolim);
  const timeSec = quiz.questions[0]?.timeLimitSeconds || 20;
  const text =
    `🧪 <b>${escapeHtml(quiz.title)}</b>\n\n` +
    `📝 ${escapeHtml(quiz.description)}\n` +
    `❓ Savollar soni: <b>${quiz.questions.length} ta</b>\n` +
    `⏱ Har bir savolga: <b>${timeSec} soniya</b>`;

  return {
    text,
    reply_markup: {
      inline_keyboard: [
        [
          { text: "▶️ Boshlash", callback_data: `m:a:go:${quiz.id}` },
          { text: "⬅️ Orqaga", callback_data: `m:a:sec:${secKey}` },
        ],
      ],
    },
  };
}

async function editOrReplyMenu(ctx: Context, payload: MenuMessagePayload): Promise<void> {
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
      if (quizManager.isQuizActive(chatId)) {
        const isPaused = quizManager.isQuizPaused(chatId);
        await ctx.answerCallbackQuery({
          text: isPaused
            ? "⚠️ Bu chatda pauzadagi quiz bor. Uni /resume bilan davom ettiring yoki /stop bilan to'xtating."
            : "⚠️ Bu chatda allaqachon faol quiz davom etmoqda.",
          show_alert: true,
        });
        return;
      }
      const quizId = formatKursQuizId(darsNum);
      await startQuizById(ctx, quizId, { fromCallback: true });
      return;
    }
  }

  // Asosiy menyu callbacklari: m:a:...
  if (data.startsWith("m:a:")) {
    if (shell.shell !== "asosiy") {
      await ctx.answerCallbackQuery({
        text: "⚠️ Bu chatda faqat «Kimyo 0 dan» kursi testlari ishlaydi.",
        show_alert: true,
      });
      return;
    }

    if (data === "m:a:list") {
      await editOrReplyMenu(ctx, buildAsosiyMenuPayload());
      return;
    }

    if (data.startsWith("m:a:sec:")) {
      const secKey = data.slice("m:a:sec:".length);
      const payload = buildAsosiySectionPayload(secKey, 0);
      if (!payload) {
        await ctx.answerCallbackQuery({ text: "⚠️ Bo'lim topilmadi.", show_alert: true });
        return;
      }
      await editOrReplyMenu(ctx, payload);
      return;
    }

    if (data.startsWith("m:a:p:")) {
      const rest = data.slice("m:a:p:".length);
      const [secKey, pageStr] = rest.split(":");
      const payload = buildAsosiySectionPayload(secKey, Number(pageStr) || 0);
      if (!payload) {
        await ctx.answerCallbackQuery({ text: "⚠️ Bo'lim topilmadi.", show_alert: true });
        return;
      }
      await editOrReplyMenu(ctx, payload);
      return;
    }

    if (data.startsWith("m:a:q:")) {
      const quizId = data.slice("m:a:q:".length);
      const payload = buildAsosiyConfirmPayload(quizId);
      if (!payload) {
        await ctx.answerCallbackQuery({ text: "⚠️ Test topilmadi.", show_alert: true });
        return;
      }
      await editOrReplyMenu(ctx, payload);
      return;
    }

    if (data.startsWith("m:a:go:")) {
      const quizId = data.slice("m:a:go:".length);
      if (quizManager.isQuizActive(chatId)) {
        const isPaused = quizManager.isQuizPaused(chatId);
        await ctx.answerCallbackQuery({
          text: isPaused
            ? "⚠️ Bu guruhda pauzadagi quiz bor. Uni /resume bilan davom ettiring yoki /stop bilan to'xtating."
            : "⚠️ Bu guruhda allaqachon faol quiz davom etmoqda.",
          show_alert: true,
        });
        return;
      }
      await startQuizById(ctx, quizId, { fromCallback: true });
      return;
    }
  }
}
