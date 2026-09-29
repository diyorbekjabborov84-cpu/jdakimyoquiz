import { Context } from "grammy";

export const MIN_GROUP_PEOPLE = 12;

export type GroupSizeResult =
  | { allowed: true; peopleCount: number }
  | { allowed: false; message: string; peopleCount?: number };

/** Telegram sanog'idan guruhdagi quiz botining o'zini chiqaramiz. */
export async function checkGroupSize(ctx: Context): Promise<GroupSizeResult> {
  if (!ctx.chat || (ctx.chat.type !== "group" && ctx.chat.type !== "supergroup")) {
    return { allowed: false, message: "Quiz faqat guruhda ishlaydi." };
  }

  try {
    const memberCount = await ctx.api.getChatMemberCount(ctx.chat.id);
    if (!Number.isInteger(memberCount) || memberCount < 1) {
      throw new Error("Invalid member count");
    }
    const peopleCount = Math.max(0, memberCount - 1);
    if (peopleCount < MIN_GROUP_PEOPLE) {
      return {
        allowed: false,
        peopleCount,
        message: `Quiz boshlash uchun guruhda kamida ${MIN_GROUP_PEOPLE} kishi bo'lishi kerak. Hozir ${peopleCount} kishi bor.`,
      };
    }
    return { allowed: true, peopleCount };
  } catch (error) {
    console.error(`[GroupSizeGuard] A'zolar sonini aniqlab bo'lmadi (chatId: ${ctx.chat.id}):`, error);
    return {
      allowed: false,
      message: "Guruh a'zolari sonini hozir tekshirib bo'lmadi. Birozdan so'ng qayta urinib ko'ring.",
    };
  }
}
