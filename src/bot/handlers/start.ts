import { Context } from "grammy";
import { escapeHtml } from "../../quiz/quizManager.js";
import { startQuizById } from "./quiz.js";
import { trackGroupEvent, trackUserEvent } from "../../tracking/tracker.js";
import {
  resolveShell,
  replyGroupDisabledOnce,
  replyPrivateNotParticipant,
} from "../../shell/shell.js";
import { buildAsosiyMenuPayload, buildKursMenuPayload } from "./menu.js";

/**
 * /start buyrug'i uchun handler.
 * Guruhning mode qiymati va foydalanuvchining kurs a'zoligiga qarab
 * Asosiy qobiq yoki Kurs qobig'i («Kimyo 0 dan») menyusini ochadi.
 */
export async function handleStart(ctx: Context): Promise<void> {
  const firstName = ctx.from?.first_name || "foydalanuvchi";
  const chatType = ctx.chat?.type;
  const userId = ctx.from?.id;

  // Foydalanuvchi yoki guruh faolligini asinxron qayd etish
  if (chatType === "private" && userId) {
    void trackUserEvent(userId, {
      firstName: ctx.from?.first_name,
      lastName: ctx.from?.last_name ?? null,
      username: ctx.from?.username ?? null,
      privateChatActive: true,
    });
  } else if ((chatType === "group" || chatType === "supergroup") && ctx.chat?.id) {
    void trackGroupEvent(ctx.chat.id, {
      title: (ctx.chat as any).title || "Guruh",
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

  // Deep link parametrini olish (masalan: /start quiz_KK1_1 yoki /start quiz_KURS_D01)
  const rawMatch = typeof ctx.match === "string" ? ctx.match.trim() : "";
  const messageText = ctx.message?.text || "";
  const textParts = messageText.trim().split(/\s+/);
  const payload = rawMatch || (textParts.length > 1 ? textParts[1] : "");

  if (payload) {
    const quizId = payload.replace(/^(quiz_|start_)/i, "");
    await startQuizById(ctx, quizId);
    return;
  }

  if (shell.shell === "kurs") {
    const greeting =
      shell.context === "private"
        ? `👋 <b>Assalomu alaykum, ${escapeHtml(firstName)}!</b>\n«Kimyo 0 dan» kursi testlar bo‘limiga xush kelibsiz.`
        : `🧪 <b>JDA Kimyo Quiz Boti («Kimyo 0 dan» kursi) faol!</b>`;
    const menu = buildKursMenuPayload(0, greeting);
    await ctx.reply(menu.text, {
      parse_mode: "HTML",
      reply_markup: menu.reply_markup,
    });
    return;
  }

  // Asosiy guruh qobig'i
  const menu = buildAsosiyMenuPayload("🧪 <b>JDA Kimyo Quiz Boti faol!</b>");
  await ctx.reply(menu.text, {
    parse_mode: "HTML",
    reply_markup: menu.reply_markup,
  });
}
