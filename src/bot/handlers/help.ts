import { CommandContext, Context } from "grammy";

export async function handleHelp(ctx: CommandContext<Context>): Promise<void> {
  const text =
    `📖 <b>JDA Kimyo Quiz Boti — Qo'llanma</b>\n\n` +
    `Ushbu bot Telegram guruhlarida kimyo fanidan jonli va qiziqarli quiz musobaqalarini tashkil qiladi.\n\n` +
    `🔹 <b>Mavjud buyruqlar:</b>\n` +
    `• /start — Botni ishga tushirish va xush kelibsiz xabarini ko'rish\n` +
    `• /help — Botdan foydalanish yo'riqnomasi va buyruqlar ro'yxati\n` +
    `• /quiz — Guruhda kimyo quizini boshlash (faqat adminlar uchun)\n` +
    `• /stopquiz — Faol quizni to'xtatish (faqat adminlar uchun)\n\n` +
    `🔹 <b>Guruhda qanday ishlaydi?</b>\n` +
    `1. Bot guruhga qo'shiladi va unga xabarlar hamda so'rovnomalarni (poll) yuborish ruxsati beriladi.\n` +
    `2. Guruh admini /quiz buyrug'ini yuboradi va savollar ketma-ket rasmiy Telegram <b>Quiz Poll</b> shaklida chiqadi.\n` +
    `3. Har bir savol uchun vaqt belgilanadi (15 soniya). Vaqt tugagach savol yopiladi va keyingisiga o'tiladi.\n` +
    `4. Ishtirokchilar to'g'ri javobni tanlaganliklari va qanchalik tez javob berganliklariga qarab ball to'playdilar.\n` +
    `5. Quiz yakunida guruhga barcha qatnashchilarning umumiy reytingi va to'plangan natijasi chiqariladi.\n\n` +
    `⚠️ <i>Eslatma: Bir guruhda bir vaqtning o'zida faqat bitta faol quiz o'tkazilishi mumkin.</i>`;

  await ctx.reply(text, { parse_mode: "HTML" });
}
