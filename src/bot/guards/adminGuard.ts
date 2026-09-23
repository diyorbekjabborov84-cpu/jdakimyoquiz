import { Context } from "grammy";

/**
 * Foydalanuvchining guruh admini yoki egasi ekanligini tekshirish
 */
export async function isGroupAdmin(ctx: Context): Promise<boolean> {
  // Agar guruh bo'lmasa (masalan, private chat), false qaytariladi
  if (!ctx.chat || (ctx.chat.type !== "group" && ctx.chat.type !== "supergroup")) {
    return false;
  }

  const userId = ctx.from?.id;
  if (!userId) {
    return false;
  }

  try {
    const member = await ctx.getChatMember(userId);
    return member.status === "creator" || member.status === "administrator";
  } catch (error) {
    console.error(`[AdminGuard] Chat ${ctx.chat.id} da admin huquqini tekshirishda xatolik:`, error);
    return false;
  }
}
