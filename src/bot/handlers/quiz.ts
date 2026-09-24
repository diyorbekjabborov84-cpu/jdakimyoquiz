import { CommandContext, Context } from "grammy";
import { isGroupAdmin } from "../guards/adminGuard.js";
import {
  checkChannelSubscriptions,
  buildSubscriptionMessageAndKeyboard,
} from "../guards/subscriptionGuard.js";
import { quizManager, escapeHtml } from "../../quiz/quizManager.js";
import { getQuizById } from "../../quiz/questions.js";

/**
 * Quizni ID bo'yicha boshlashning umumiy yordamchi funksiyasi
 */
export async function startQuizById(ctx: Context, rawId: string): Promise<void> {
  const quizId = rawId.trim();
  const quiz = getQuizById(quizId);

  if (!quiz) {
    await ctx.reply(
      `❌ <b>Bunday IDga ega quiz topilmadi:</b> <code>${escapeHtml(quizId)}</code>\n\n` +
        `Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz yoki /quiz buyrug'ini yuboring.`,
      { parse_mode: "HTML" }
    );
    return;
  }

  const isGroup = ctx.chat?.type === "group" || ctx.chat?.type === "supergroup";

  // Guruhda: faqat guruh admini boshlashi mumkin, LEKIN kanal obunasi talab qilinmaydi!
  if (isGroup) {
    const isAdmin = await isGroupAdmin(ctx);
    if (!isAdmin) {
      await ctx.reply(
        "⚠️ <b>Kechirasiz!</b> Guruhda quizni faqat guruh adminlari boshlashi mumkin.",
        { parse_mode: "HTML" }
      );
      return;
    }

    // Guruhda faol quiz tekshiruvi
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
    return;
  }

  // Shaxsiy chatda: ikkala kanalga ham majburiy obunani tekshirish
  const userId = ctx.from?.id;
  if (userId) {
    const subResult = await checkChannelSubscriptions(ctx.api, userId);

    if (subResult.status === "error") {
      await ctx.reply(subResult.message, { parse_mode: "HTML" });
      return;
    }

    if (subResult.status === "not_subscribed") {
      const { text, reply_markup } = buildSubscriptionMessageAndKeyboard(quiz.id);
      await ctx.reply(text, { parse_mode: "HTML", reply_markup });
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
 * «✅ A’zo bo‘ldim — tekshirish» callback query hodisasi
 */
export async function handleCheckSubscriptionCallback(ctx: Context): Promise<void> {
  const data = ctx.callbackQuery?.data;
  if (!data || !data.startsWith("check_sub_")) return;

  // Obuna tugmasi faqat shaxsiy chat uchun: guruhga ko'chirilgan tugma admin tekshiruvini chetlab o'tmasin.
  if (ctx.chat?.type !== "private") {
    await ctx.answerCallbackQuery({
      text: "Bu tugma faqat botning shaxsiy chatida ishlaydi.",
      show_alert: true,
    });
    return;
  }

  const quizId = data.replace(/^check_sub_/, "").trim();
  const quiz = quizId === "start" ? undefined : getQuizById(quizId);
  const userId = ctx.from?.id;

  if (quizId !== "start" && !quiz) {
    await ctx.answerCallbackQuery({
      text: "❌ Bunday IDga ega quiz topilmadi.",
      show_alert: true,
    });
    return;
  }

  if (!userId) {
    await ctx.answerCallbackQuery({ text: "Foydalanuvchi aniqlanmadi." });
    return;
  }

  const subResult = await checkChannelSubscriptions(ctx.api, userId);

  if (subResult.status === "error") {
    await ctx.answerCallbackQuery({
      text: "Kanal a'zoligini tekshirishda vaqtinchalik xatolik yuz berdi.",
      show_alert: true,
    });
    await ctx.reply(subResult.message, { parse_mode: "HTML" });
    return;
  }

  if (subResult.status === "not_subscribed") {
    await ctx.answerCallbackQuery({
      text: "❌ Siz hali barcha kanallarga a'zo bo'lmadingiz. Iltimos, ikkala kanalga ham a'zo bo'ling!",
      show_alert: true,
    });
    return;
  }

  // Obuna tasdiqlandi
  await ctx.answerCallbackQuery({ text: "✅ Obuna tasdiqlandi!" });

  if (quizId === "start") {
    await ctx.reply(
      "✅ <b>Obuna tasdiqlandi!</b> Asosiy quiz kodlarini /quiz orqali @jdaquizkod kanalidan olasiz.",
      { parse_mode: "HTML" }
    );
    return;
  }

  if (!quiz) return;

  if (ctx.chat && quizManager.isQuizRunning(ctx.chat.id)) {
    await ctx.reply(
      "⚠️ <b>Bu chatda allaqachon faol quiz davom etmoqda.</b>\n\n" +
        "Iltimos, avval joriy quiz yakunlanishini kuting yoki uni /stop buyrug'i bilan to'xtating.",
      { parse_mode: "HTML" }
    );
    return;
  }

  if (ctx.chat) {
    await ctx.reply("🎉 <b>Obuna tasdiqlandi!</b> Tanlangan quiz boshlanmoqda...", {
      parse_mode: "HTML",
    });
    await quizManager.startQuiz(ctx.chat.id, quiz, ctx.api);
  }
}

/**
 * /quiz buyrug'i:
 * - Argumentsiz yoki 'list': «Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz» xabari va kanal tugmasini chiqaradi.
 *   Bu xabar guruhda ham, shaxsiy chatda ham chiqadi; guruhda hech kimdan obuna talab qilinmaydi.
 * - Argument berilgan bo'lsa (masalan: /quiz amino_acids): shu quizni boshlaydi.
 */
export async function handleQuizCommand(ctx: CommandContext<Context>): Promise<void> {
  const matchArg = ctx.match?.trim();

  // Agar aniq ID berilgan bo'lsa va u "list" bo'lmasa, o'sha quizni boshlash
  if (matchArg && matchArg.toLowerCase() !== "list") {
    await startQuizById(ctx, matchArg);
    return;
  }

  // /quiz yuborilganda kanalga yo'naltirish
  const text =
    `ℹ️ <b>Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz.</b>\n\n` +
    `Kanalga ulanib, yangi quiz kodlari, testlar va shaxsiy havolalarni kuzatib boring!`;

  await ctx.reply(text, {
    parse_mode: "HTML",
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: "📢 @jdaquizkod kanaliga o'tish",
            url: "https://t.me/jdaquizkod",
          },
        ],
      ],
    },
  });
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
