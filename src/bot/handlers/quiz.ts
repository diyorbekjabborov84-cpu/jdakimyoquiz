import { CommandContext, Context } from "grammy";
import { isGroupAdmin } from "../guards/adminGuard.js";
import { quizManager, escapeHtml } from "../../quiz/quizManager.js";
import { getAllQuizzes, getQuizById } from "../../quiz/questions.js";

/**
 * Quizni ID bo'yicha boshlashning umumiy yordamchi funksiyasi
 */
export async function startQuizById(ctx: Context, rawId: string): Promise<void> {
  const quizId = rawId.trim();
  const quiz = getQuizById(quizId);

  if (!quiz) {
    await ctx.reply(
      `❌ <b>Bunday IDga ega quiz topilmadi:</b> <code>${escapeHtml(quizId)}</code>\n\n` +
        `Mavjud quizlar ro'yxatini ko'rish uchun /quiz buyrug'ini yuboring.`,
      { parse_mode: "HTML" }
    );
    return;
  }

  const isGroup = ctx.chat?.type === "group" || ctx.chat?.type === "supergroup";

  // Guruhda faqat guruh admini boshlashi mumkin
  if (isGroup) {
    const isAdmin = await isGroupAdmin(ctx);
    if (!isAdmin) {
      await ctx.reply(
        "⚠️ <b>Kechirasiz!</b> Guruhda quizni faqat guruh adminlari boshlashi mumkin.",
        { parse_mode: "HTML" }
      );
      return;
    }
  }

  // Bitta chatda faol quiz turganda ikkinchisini boshlashga yo'l qo'ymaslik
  if (ctx.chat && quizManager.isQuizRunning(ctx.chat.id)) {
    await ctx.reply(
      "⚠️ <b>Bu chatda allaqachon faol quiz davom etmoqda.</b>\n\n" +
        "Iltimos, avval joriy quiz yakunlanishini kuting yoki uni /stop buyrug'i bilan to'xtating.",
      { parse_mode: "HTML" }
    );
    return;
  }

  if (ctx.chat) {
    await quizManager.startQuiz(ctx.chat.id, quiz, ctx.api);
  }
}

/**
 * /quiz buyrug'i:
 * - Argumentsiz yoki 'list': mavjud barcha quizlar ro'yxatini ko'rsatadi
 * - Argument berilgan bo'lsa (masalan, /quiz amino_acids): shu quizni boshlaydi
 */
export async function handleQuizCommand(ctx: CommandContext<Context>): Promise<void> {
  const matchArg = ctx.match?.trim();

  // Agar ID berilgan bo'lsa va u "list" bo'lmasa, o'sha quizni boshlash
  if (matchArg && matchArg.toLowerCase() !== "list") {
    await startQuizById(ctx, matchArg);
    return;
  }

  // Aks holda mavjud quizlar ro'yxatini ko'rsatish
  const quizzes = getAllQuizzes();
  const botUsername = ctx.me?.username || process.env.BOT_USERNAME || "jdakimyoquizbot";

  let text = `📋 <b>Mavjud quizlar ro‘yxati:</b>\n\n`;

  quizzes.forEach((q, index) => {
    const timeLimit = q.questions[0]?.timeLimitSeconds || 20;
    text += `${index + 1}. <b>«${escapeHtml(q.title)}»</b>\n`;
    text += `   📝 ${escapeHtml(q.description)}\n`;
    text += `   ❓ Savollar soni: <b>${q.questions.length} ta</b> (har biriga ${timeLimit}s)\n`;
    text += `   🚀 Boshlash: /quiz_${q.id}\n`;
    text += `   🔗 Shaxsiy havola: https://t.me/${botUsername}?start=quiz_${q.id}\n\n`;
  });

  text += `💡 <i>Guruhda quizni faqat admin boshlashi mumkin. Shaxsiy chatda esa istalgan payt o'zingiz boshlay olasiz!</i>`;

  await ctx.reply(text, { parse_mode: "HTML" });
}

/**
 * /quiz_<ID> buyrug'i orqali tanlangan quizni boshlash
 */
export async function handleQuizByIdCommand(ctx: Context): Promise<void> {
  const match = (ctx as any).match;
  const quizId = Array.isArray(match) ? match[1] : match;

  if (quizId) {
    await startQuizById(ctx, quizId);
  } else {
    await handleQuizCommand(ctx as any);
  }
}

/**
 * /stop va /stopquiz buyrug'i - faol quizni to'xtatish
 * - Guruhda: faqat guruh admini to'xtata oladi
 * - Shaxsiy chatda: foydalanuvchining o'zi to'xtata oladi
 */
export async function handleStopQuizCommand(ctx: CommandContext<Context>): Promise<void> {
  const isGroup = ctx.chat.type === "group" || ctx.chat.type === "supergroup";

  // Guruhda admin huquqini tekshirish
  if (isGroup) {
    const isAdmin = await isGroupAdmin(ctx);
    if (!isAdmin) {
      await ctx.reply(
        "⚠️ <b>Kechirasiz!</b> Guruhda quizni to'xtatish huquqi faqat guruh adminlariga berilgan.",
        { parse_mode: "HTML" }
      );
      return;
    }
  }

  if (!quizManager.isQuizRunning(ctx.chat.id)) {
    await ctx.reply("ℹ️ Ushbu chatda ayni paytda faol quiz mavjud emas.");
    return;
  }

  await quizManager.stopQuiz(ctx.chat.id, ctx.api);
}
