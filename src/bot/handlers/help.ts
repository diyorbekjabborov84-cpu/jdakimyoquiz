import { CommandContext, Context } from "grammy";

export async function handleHelp(ctx: CommandContext<Context>): Promise<void> {
  const text =
    `📖 <b>JDA Kimyo Quiz Boti — Qo'llanma</b>\n\n` +
    `Ushbu bot kimyo quizlarini Telegram guruhlarida o'tkazadi. Shaxsiy chatda test kodlari va guruhga qo'shish havolasini olishingiz mumkin.\n\n` +
    `🔹 <b>Mavjud buyruqlar:</b>\n` +
    `• /start — Botni ishga tushirish yoki shaxsiy havola orqali quizni ochish\n` +
    `• /help — Botdan foydalanish yo'riqnomasi va buyruqlar\n` +
    `• /quiz — Test kodlarini olish uchun @jdaquizkod kanaliga havola\n` +
    `• /quiz_&lt;ID&gt; — Tanlangan quizni boshlash (masalan: /quiz_amino_acids)\n` +
    `• /stop yoki /stopquiz — Faol quizni to'xtatish\n\n` +
    `🔹 <b>Foydalanish tartibi:</b>\n` +
    `1. <b>Guruhda:</b> Quizni faqat guruh admini /quiz_&lt;ID&gt; orqali boshlashi yoki /stop bilan to'xtatishi mumkin.\n` +
    `2. <b>Shaxsiy chatda:</b> /quiz orqali kodlar kanalini oching. Testlar shaxsiy chatda boshlanmaydi.\n` +
    `3. <b>Guruh havolalari:</b> Har bir quiz uchun guruhga qo'shish havolasi mavjud (masalan: <code>https://t.me/&lt;bot_username&gt;?startgroup=quiz_&lt;ID&gt;</code>).\n` +
    `4. Savollar rasmiy Telegram <b>Quiz Poll</b> shaklida beriladi, har biriga 20 soniya vaqt ajratiladi.\n` +
    `5. To'xtatilgan quizning yakuniy natijasi hisoblanmaydi; muvaffaqiyatli yakunlanganda umumiy reyting e'lon qilinadi.\n\n` +
    `⚠️ <i>Eslatma: Bitta chatda bir vaqtning o'zida faqat bitta faol quiz o'tkazilishi mumkin. Boshqa chatlarning o'yini va natijalari mutlaqo mustaqildir.</i>`;

  await ctx.reply(text, { parse_mode: "HTML" });
}
