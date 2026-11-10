import { Context } from "grammy";
import {
  resolveShell,
  replyGroupDisabledOnce,
  replyPrivateNotParticipant,
} from "../../shell/shell.js";

/**
 * /help buyrug'i uchun handler — qobiqqa mos qo'llanmani qaytaradi
 */
export async function handleHelp(ctx: Context): Promise<void> {
  if (ctx.chat?.type) {
    const shell = await resolveShell(ctx);
    if (shell.shell === "yopiq") {
      if (shell.reason === "group_disabled") {
        await replyGroupDisabledOnce(ctx);
      } else {
        await replyPrivateNotParticipant(ctx, shell.reason);
      }
      return;
    }

    if (shell.shell === "kurs") {
      await ctx.reply(
        `📖 <b>Qo'llanma («Kimyo 0 dan» kursi):</b>\n\n` +
          `<b>Asosiy buyruqlar:</b>\n` +
          `/start yoki /quiz — Kurs darslari bo‘yicha testlar menyusi\n` +
          `/resume — To'xtagan (pauzadagi) testni davom ettirish\n` +
          `/stop — Faol testni to'xtatish\n` +
          `/help — Ushbu yordam oynasini ko'rsatish\n\n` +
          `<b>Qoidalar:</b>\n` +
          `1. Har bir dars testida savollar va variantlar tasodifiy aralashtiriladi.\n` +
          `2. Har bir savolga 30 soniya vaqt beriladi.\n` +
          `3. Shaxsiy chatda 9/12 dan past natija bo‘lsa, dars videosini qayta ko‘rish tavsiya etiladi.`,
        { parse_mode: "HTML" }
      );
      return;
    }
  }

  await ctx.reply(
    `📖 <b>Qo'llanma va Buyruqlar:</b>\n\n` +
      `<b>Asosiy buyruqlar:</b>\n` +
      `/start — Bot holatini tekshirish va testlar menyusi\n` +
      `/quiz — Testlar bo‘limlari menyusini ochish\n` +
      `/resume — To'xtagan (pauzadagi) quizni davom ettirish\n` +
      `/stop — Faol quizni majburiy to'xtatish (faqat guruh adminlari)\n` +
      `/help — Ushbu yordam oynasini ko'rsatish\n\n` +
      `<b>Qoidalar:</b>\n` +
      `1. Botni guruhingizga qo'shing va unga <b>Admin</b> huquqini bering.\n` +
      `2. Guruhda <code>/quiz</code> menyusidan yoki <code>/quiz_KOD</code> orqali testni boshlang.\n` +
      `3. Guruh a'zolari o'z vaqtida (20 soniya ichida) javob berishlari kerak.\n` +
      `4. Ketma-ket 3 ta savolga hech kim javob bermasa, quiz vaqtincha to'xtatiladi (Aqlli pauza).\n` +
      `5. Yakunda eng ko'p to'g'ri va eng tez javob bergan ishtirokchilar reytingi e'lon qilinadi!`,
    { parse_mode: "HTML" }
  );
}
