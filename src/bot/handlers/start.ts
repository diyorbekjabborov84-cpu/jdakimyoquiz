import { CommandContext, Context } from "grammy";
import { startQuizById } from "./quiz.js";

export async function handleStart(ctx: CommandContext<Context>): Promise<void> {
  const isGroup = ctx.chat.type === "group" || ctx.chat.type === "supergroup";
  const botUsername = ctx.me?.username || process.env.BOT_USERNAME || "jdakimyoquizbot";
  const payload = ctx.match?.trim();

  // Agar havola orqali quiz ID uzatilgan bo'lsa (masalan: ?start=quiz_amino_acids)
  if (payload && payload.startsWith("quiz_")) {
    const quizId = payload.replace(/^quiz_/, "").trim();
    await startQuizById(ctx, quizId);
    return;
  }

  if (isGroup) {
    const text =
      `🧪 <b>JDA Kimyo Quiz Boti faol!</b>\n\n` +
      `Salom, guruh a'zolari! Ushbu bot guruhda kimyo fanidan ko'p savolli interaktiv quizlar o'tkazish uchun mo'ljallangan.\n\n` +
      `📌 <b>Bot imkoniyatlari:</b>\n` +
      `• Telegramning rasmiy <i>Quiz Poll</i> shaklidagi savollari\n` +
      `• Haqiqiy vaqt chegarasi (taymer) va avtomatik keyingi savolga o'tish\n` +
      `• Barcha qatnashchilar uchun avtomatik ball va vaqt hisobi\n` +
      `• Yakuniy reyting jadvali (eng to'g'ri va tez javob berganlar yuqorida)\n\n` +
      `Mavjud quizlarni ko'rish uchun /quiz buyrug'ini yuboring.\n` +
      `Batafsil ma'lumot va buyruqlar uchun /help buyrug'ini bosing.`;

    await ctx.reply(text, { parse_mode: "HTML" });
    return;
  }

  // Shaxsiy chat (Private)
  const text =
    `👋 <b>Assalomu alaykum, ${ctx.from?.first_name || "foydalanuvchi"}!</b>\n\n` +
    `Men <b>JDA Kimyo Quiz</b> botiman — kimyo fanidan interaktiv musobaqalar va testlar o'tkazib beraman.\n\n` +
    `🚀 <b>Mendan qanday foydalanish mumkin?</b>\n` +
    `1. /quiz buyrug'ini yuborib mavjud testlar ro'yxatini ko'ring va shaxsiy testni boshlang;\n` +
    `2. Meni o'z Telegram guruhingizga qo'shing va admin huquqini bering;\n` +
    `3. Guruhda /quiz buyrug'i orqali jamoaviy quiz musobaqalarini o'tkazing.\n\n` +
    `💡 <i>Savollar Telegramning rasmiy Quiz ko'rinishida beriladi va yakunda barcha ishtirokchilar reytingi e'lon qilinadi.</i>`;

  await ctx.reply(text, {
    parse_mode: "HTML",
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: "➕ Guruhga qo'shish",
            url: `https://t.me/${botUsername}?startgroup=true`,
          },
        ],
      ],
    },
  });
}
