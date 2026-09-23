import { CommandContext, Context } from "grammy";
import { isGroupAdmin } from "../guards/adminGuard.js";
import { quizManager } from "../../quiz/quizManager.js";
import { sampleChemistryQuiz } from "../../quiz/questions.js";

/**
 * /quiz buyrug'i - guruhda yangi quizni boshlash
 */
export async function handleQuizCommand(ctx: CommandContext<Context>): Promise<void> {
  const isGroup = ctx.chat.type === "group" || ctx.chat.type === "supergroup";

  if (!isGroup) {
    await ctx.reply(
      "ℹ️ <b>Quiz faqat Telegram guruhlarida o'tkaziladi.</b>\n\n" +
        "Botni o'z guruhingizga qo'shing va u yerda /quiz buyrug'ini yuboring.",
      { parse_mode: "HTML" }
    );
    return;
  }

  // Admin huquqini tekshirish
  const isAdmin = await isGroupAdmin(ctx);
  if (!isAdmin) {
    await ctx.reply(
      "⚠️ <b>Kechirasiz!</b> Quizni faqat ushbu guruh adminlari boshlashi mumkin.",
      { parse_mode: "HTML" }
    );
    return;
  }

  // Quiz allaqachon ishlayotgan bo'lsa
  if (quizManager.isQuizRunning(ctx.chat.id)) {
    await ctx.reply(
      "⚠️ Bu guruhda hozirda faol quiz davom etmoqda. Iltimos, u tugashini kuting yoki /stopquiz buyrug'ini bering."
    );
    return;
  }

  // Quizni boshlash
  await quizManager.startQuiz(ctx.chat.id, sampleChemistryQuiz, ctx.api);
}

/**
 * /stopquiz buyrug'i - faol quizni to'xtatish
 */
export async function handleStopQuizCommand(ctx: CommandContext<Context>): Promise<void> {
  const isGroup = ctx.chat.type === "group" || ctx.chat.type === "supergroup";

  if (!isGroup) {
    await ctx.reply("ℹ️ Ushbu buyruq faqat guruhlarda ishlaydi.");
    return;
  }

  // Admin huquqini tekshirish
  const isAdmin = await isGroupAdmin(ctx);
  if (!isAdmin) {
    await ctx.reply(
      "⚠️ <b>Kechirasiz!</b> Quizni to'xtatish huquqi faqat guruh adminlariga berilgan.",
      { parse_mode: "HTML" }
    );
    return;
  }

  if (!quizManager.isQuizRunning(ctx.chat.id)) {
    await ctx.reply("ℹ️ Ushbu guruhda ayni paytda faol quiz mavjud emas.");
    return;
  }

  await quizManager.stopQuiz(ctx.chat.id, ctx.api);
}
