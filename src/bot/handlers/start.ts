import { CommandContext, Context } from "grammy";

export async function handleStart(ctx: CommandContext<Context>): Promise<void> {
  const isGroup = ctx.chat.type === "group" || ctx.chat.type === "supergroup";
  const botUsername = ctx.me.username;

  if (isGroup) {
    const text =
      `🧪 <b>JDA Kimyo Quiz Boti faol!</b>\n\n` +
      `Salom, guruh a'zolari! Ushbu bot guruhda kimyo fanidan ko'p savolli interaktiv quizlar o'tkazish uchun mo'ljallangan.\n\n` +
      `📌 <b>Bot imkoniyatlari:</b>\n` +
      `• Telegramning rasmiy <i>Quiz Poll</i> shaklidagi savollari\n` +
      `• Haqiqiy vaqt chegarasi (taymer) va avtomatik keyingi savolga o'tish\n` +
      `• Barcha qatnashchilar uchun avtomatik ball va vaqt hisobi\n` +
      `• Yakuniy reyting jadvali (eng to'g'ri va tez javob berganlar yuqorida)\n\n` +
      `Batafsil ma'lumot va buyruqlar uchun /help buyrug'ini yuboring.`;

    await ctx.reply(text, { parse_mode: "HTML" });
    return;
  }

  // Shaxsiy chat (Private)
  const text =
    `👋 <b>Assalomu alaykum, ${ctx.from?.first_name || "foydalanuvchi"}!</b>\n\n` +
    `Men <b>JDA Kimyo Quiz</b> botiman — Telegram guruhlarida kimyo fanidan interaktiv musobaqalar va testlar o'tkazib beraman.\n\n` +
    `🚀 <b>Mendan qanday foydalaniladi?</b>\n` +
    `1. Meni o'z Telegram guruhingizga qo'shing;\n` +
    `2. Guruhda savollarni (poll-larni) yubora olishim uchun menga admin huquqini bering;\n` +
    `3. Guruhda /start yoki /help buyrug'ini yozib ishga tushiring.\n\n` +
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
