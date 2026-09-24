import { CommandContext, Context } from "grammy";

export async function handleHelp(ctx: CommandContext<Context>): Promise<void> {
  const text =
    `📖 <b>JDA Kimyo Quiz Boti — Qo'llanma</b>\n\n` +
    `Ushbu bot Telegram guruhlarida va shaxsiy chatda kimyo fanidan ko'p quizli interaktiv test tizimini taqdim etadi.\n\n` +
    `🔹 <b>Mavjud buyruqlar:</b>\n` +
    `• /start — Botni ishga tushirish yoki shaxsiy havola orqali quizni ochish\n` +
    `• /help — Botdan foydalanish yo'riqnomasi va buyruqlar\n` +
    `• /quiz — Test kodlarini olish uchun @jdaquizkod kanaliga havola\n` +
    `• /quiz_&lt;ID&gt; — Tanlangan quizni boshlash (masalan: /quiz_amino_acids)\n` +
    `• /stop yoki /stopquiz — Faol quizni to'xtatish\n\n` +
    `🔹 <b>Foydalanish tartibi:</b>\n` +
    `1. <b>Guruhda:</b> Quizni faqat guruh admini /quiz_&lt;ID&gt; orqali boshlashi yoki /stop bilan to'xtatishi mumkin.\n` +
    `2. <b>Shaxsiy chatda:</b> Foydalanuvchi /quiz orqali kodlar kanaliga o'tadi, kanallarga a'zo bo'lgach /quiz_&lt;ID&gt; bilan testni boshlaydi.\n` +
    `3. <b>Shaxsiy havolalar:</b> Har bir quizning maxsus havolasi mavjud (masalan: <code>https://t.me/&lt;bot_username&gt;?start=quiz_&lt;ID&gt;</code>).\n` +
    `4. Savollar rasmiy Telegram <b>Quiz Poll</b> shaklida beriladi, har biriga 20 soniya vaqt ajratiladi.\n` +
    `5. To'xtatilgan quizning yakuniy natijasi hisoblanmaydi; muvaffaqiyatli yakunlanganda umumiy reyting e'lon qilinadi.\n\n` +
    `⚠️ <i>Eslatma: Bitta chatda bir vaqtning o'zida faqat bitta faol quiz o'tkazilishi mumkin. Boshqa chatlarning o'yini va natijalari mutlaqo mustaqildir.</i>`;

  await ctx.reply(text, { parse_mode: "HTML" });
}
