import { CommandContext, Context } from "grammy";
import { isGroupAdmin } from "../guards/adminGuard.js";
import { checkChannelSubscriptions } from "../guards/subscriptionGuard.js";
import { checkGroupSize } from "../guards/groupSizeGuard.js";
import { quizManager, escapeHtml } from "../../quiz/quizManager.js";
import { getQuizById } from "../../quiz/questions.js";
import { trackGroupEvent, trackUserEvent } from "../../tracking/tracker.js";

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

  // Shaxsiy chatda hech qanday quiz boshlanmasin: Barcha quizlar faqat Telegram guruhlari uchun!
  if (!isGroup) {
    const botUsername = ctx.me?.username || process.env.BOT_USERNAME || "jdakimyoquizbot";
    const groupLink = `https://t.me/${botUsername}?startgroup=quiz_${quiz.id}`;
    await ctx.reply(
      `ℹ️ <b>«${escapeHtml(quiz.title)}» faqat Telegram guruhlarida o'tkaziladi.</b>\n\n` +
        `Ushbu test jamoaviy musobaqa formatida tuzilgan bo'lib, uni faqat guruhlarda o'ynash mumkin.\n\n` +
        `Botni o'z guruhingizga qo'shing va guruhda <code>/quiz_${quiz.id}</code> buyrug'ini yuborib boshlang:`,
      {
        parse_mode: "HTML",
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: "➕ Guruhga qo'shish va boshlash",
                url: groupLink,
              },
            ],
          ],
        },
      }
    );
    return;
  }

  // Guruhda: istalgan a'zo boshlashi mumkin, kanal obunasi talab qilinmaydi!
  if (isGroup) {
    // Guruh va foydalanuvchi faolligini qayd etish
    if (ctx.chat) {
      trackGroupEvent(ctx.chat.id, {
        title: (ctx.chat as any).title,
        type: ctx.chat.type,
        status: "active",
      }).catch(() => {});
    }
    if (ctx.from) {
      trackUserEvent(ctx.from.id, {
        firstName: ctx.from.first_name,
        lastName: ctx.from.last_name,
        username: ctx.from.username,
      }).catch(() => {});
    }

    // Guruhda faol yoki pauzadagi quiz tekshiruvi
    if (ctx.chat && quizManager.isQuizActive(ctx.chat.id)) {
      const isPaused = quizManager.isQuizPaused(ctx.chat.id);
      await ctx.reply(
        isPaused
          ? "⚠️ <b>Bu chatda pauza qilingan quiz mavjud.</b>\n\nIltimos, avval uni «▶️ Qolgan joyidan davom ettirish» tugmasi bilan davom ettiring yoki /stop buyrug'i bilan to'xtating."
          : "⚠️ <b>Bu chatda allaqachon faol quiz davom etmoqda.</b>\n\nIltimos, avval joriy quiz yakunlanishini kuting yoki uni /stop buyrug'i bilan to'xtating.",
        { parse_mode: "HTML" }
      );
      return;
    }

    const size = await checkGroupSize(ctx);
    if (!size.allowed) {
      await ctx.reply(`⚠️ ${size.message}`);
      return;
    }
    trackGroupEvent(ctx.chat!.id, { memberCount: size.peopleCount + 1 }).catch(() => {});
    await quizManager.startQuiz(ctx.chat!.id, quiz, ctx.api);
    return;
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

  // Shaxsiy chatda hech qanday quiz boshlanmaydi: Barcha quizlar faqat guruhlar uchun!
  const botUsername = ctx.me?.username || process.env.BOT_USERNAME || "jdakimyoquizbot";
  const groupLink = `https://t.me/${botUsername}?startgroup=quiz_${quiz.id}`;
  await ctx.reply(
    `ℹ️ <b>«${escapeHtml(quiz.title)}» faqat Telegram guruhlarida o'tkaziladi.</b>\n\n` +
      `Ushbu test jamoaviy musobaqa formatida tuzilgan bo'lib, uni faqat guruhlarda o'ynash mumkin.\n\n` +
      `Botni o'z guruhingizga qo'shing va guruhda <code>/quiz_${quiz.id}</code> buyrug'ini yuborib boshlang:`,
    {
      parse_mode: "HTML",
      reply_markup: {
        inline_keyboard: [
          [
            {
              text: "➕ Guruhga qo'shish va boshlash",
              url: groupLink,
            },
          ],
        ],
      },
    }
  );
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

  if (!quizManager.isQuizActive(ctx.chat.id)) {
    await ctx.reply("ℹ️ Ushbu chatda ayni paytda faol quiz mavjud emas.");
    return;
  }

  await quizManager.stopQuiz(ctx.chat.id, ctx.api);
}

/**
 * «🔄 Qayta yechish» callback query hodisasi
 * - Guruhning istalgan a'zosi bosa oladi (adminlik talab qilinmaydi)
 * - Faol yoki pauzadagi quiz davom etayotgan bo'lsa yangisi boshlanmaydi
 * - Guruhda kanal obunasi talab qilinmaydi
 * - Savollar va variantlar qayta aralashtiriladi
 */
export async function handleRestartQuizCallback(ctx: Context): Promise<void> {
  const data = ctx.callbackQuery?.data;
  if (!data || !data.startsWith("restart_quiz_")) return;

  const quizId = data.replace(/^restart_quiz_/, "").trim();
  const quiz = getQuizById(quizId);

  if (!quiz) {
    await ctx.answerCallbackQuery({
      text: "❌ Bunday quiz topilmadi.",
      show_alert: true,
    });
    return;
  }

  const isGroup = ctx.chat?.type === "group" || ctx.chat?.type === "supergroup";

  // Shaxsiy chatda hech qanday quiz qayta boshlanmaydi!
  if (!isGroup || !ctx.chat) {
    await ctx.answerCallbackQuery({
      text: "ℹ️ Quizlar faqat Telegram guruhlarida o'tkaziladi.",
      show_alert: true,
    });
    return;
  }

  // Boshqa quiz davom etayotgan yoki pauzada bo'lsa, yangisini boshlamasin
  if (quizManager.isQuizActive(ctx.chat.id)) {
    const isPaused = quizManager.isQuizPaused(ctx.chat.id);
    await ctx.answerCallbackQuery({
      text: isPaused
        ? "⚠️ Bu chatda pauza qilingan quiz mavjud."
        : "⚠️ Bu chatda allaqachon faol quiz davom etmoqda.",
      show_alert: true,
    });
    return;
  }

  const size = await checkGroupSize(ctx);
  if (!size.allowed) {
    await ctx.answerCallbackQuery({ text: size.message, show_alert: true });
    return;
  }

  const startResult = await quizManager.startQuiz(ctx.chat.id, quiz, ctx.api);
  if (!startResult.success) {
    await ctx.answerCallbackQuery({
      text: startResult.message,
      show_alert: true,
    });
    return;
  }

  await ctx.answerCallbackQuery({
    text: "🔄 Quiz qayta boshlanmoqda...",
  });
}

/**
 * «▶️ Qolgan joyidan davom ettirish» callback query hodisasi
 * - Guruhning istalgan a'zosi bosa oladi (adminlik talab qilinmaydi)
 * - Takror bosilgan tugma (allaqachon running yoki to'xtatilgan) uchun alert beradi
 * - Sessiya identifikatori (sessionId) mosligini tekshiradi (eski tugmalar yangi sessiyani buzmasligi uchun)
 * - Aynan keyingi savoldan boshlaydi, tartib va ballarni saqlaydi
 */
export async function handleResumeQuizCallback(ctx: Context): Promise<void> {
  const isGroup = ctx.chat?.type === "group" || ctx.chat?.type === "supergroup";
  if (!isGroup || !ctx.chat) {
    await ctx.answerCallbackQuery({
      text: "ℹ️ Quizlar faqat Telegram guruhlarida o'tkaziladi.",
      show_alert: true,
    });
    return;
  }

  const data = ctx.callbackQuery?.data || "";
  const match = data.match(/^resume_quiz_(-?\d+)_([a-zA-Z0-9_-]+)$/);
  if (!match || Number(match[1]) !== ctx.chat.id) {
    await ctx.answerCallbackQuery({
      text: "⚠️ Ushbu tugma bu guruhdagi joriy quizga tegishli emas.",
      show_alert: true,
    });
    return;
  }

  const size = await checkGroupSize(ctx);
  if (!size.allowed) {
    await ctx.answerCallbackQuery({ text: size.message, show_alert: true });
    return;
  }

  const resumeResult = await quizManager.resumeQuiz(ctx.chat.id, ctx.api, match[2]);

  if (!resumeResult.success) {
    await ctx.answerCallbackQuery({
      text: resumeResult.message,
      show_alert: true,
    });
    return;
  }

  await ctx.answerCallbackQuery({ text: "▶️ Quiz davom ettirilmoqda!" });
}

/**
 * /resume buyrug'i:
 * - Guruhning istalgan a'zosi yubora oladi (adminlik talab qilinmaydi)
 * - Server qayta tushgandan so'ng yoki aqlli pauzadagi quizni qolgan joyidan davom ettiradi
 * - Eski tugma yo'qolgan yoki xabar yuqorida qolib ketgan holatlarda ham sessiya osilib qolishini oldini oladi
 */
export async function handleResumeCommand(ctx: CommandContext<Context>): Promise<void> {
  const isGroup = ctx.chat.type === "group" || ctx.chat.type === "supergroup";

  if (!isGroup) {
    await ctx.reply(
      "ℹ️ Quizlar faqat Telegram guruhlarida o'tkaziladi. Iltimos, botni guruhga qo'shing va u yerda /resume buyrug'idan foydalaning."
    );
    return;
  }

  if (quizManager.isQuizRunning(ctx.chat.id)) {
    await ctx.reply("⚠️ Ushbu guruhda quiz allaqachon faol davom etmoqda.");
    return;
  }

  if (!quizManager.isQuizPaused(ctx.chat.id)) {
    await ctx.reply(
      "ℹ️ Ushbu guruhda hozirda to‘xtatilgan (pauzadagi) quiz mavjud emas. Yangi quiz boshlash uchun /quiz buyrug'i yoki quiz kodini yuboring."
    );
    return;
  }

  const size = await checkGroupSize(ctx);
  if (!size.allowed) {
    await ctx.reply(`⚠️ ${size.message}`);
    return;
  }

  const resumeResult = await quizManager.resumeQuiz(ctx.chat.id, ctx.api);
  if (!resumeResult.success) {
    await ctx.reply(resumeResult.message);
  }
}
