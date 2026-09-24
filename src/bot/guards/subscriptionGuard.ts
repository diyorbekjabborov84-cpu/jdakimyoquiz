export interface RequiredChannel {
  username: string;
  url: string;
  name: string;
}

export const REQUIRED_CHANNELS: RequiredChannel[] = [
  {
    username: "@jdaquizkod",
    url: "https://t.me/jdaquizkod",
    name: "@jdaquizkod",
  },
  {
    username: "@jdakimyouz",
    url: "https://t.me/jdakimyouz",
    name: "@jdakimyouz",
  },
];

export type SubscriptionCheckResult =
  | { status: "subscribed" }
  | { status: "not_subscribed"; missingChannels: RequiredChannel[] }
  | { status: "error"; message: string };

/**
 * Foydalanuvchining talab qilinadigan kanallarga a'zoligini tekshirish
 * Telegram Bot API'ning getChatMember metodi orqali ishlaydi.
 * 
 * Agar API xatolik bersa (masalan, tarmoq xatosi, kanal topilmasa yoki bot huquqi yetmasa),
 * foydalanuvchini "a'zo emas" deb noto'g'ri belgilamaymiz, balki status: "error" qaytaramiz.
 */
export async function checkChannelSubscriptions(
  api: { getChatMember(chatId: string | number, userId: number): Promise<any> },
  userId: number
): Promise<SubscriptionCheckResult> {
  const missingChannels: RequiredChannel[] = [];

  for (const ch of REQUIRED_CHANNELS) {
    try {
      const member = await api.getChatMember(ch.username, userId);
      const isSubscribed =
        member &&
        (member.status === "creator" ||
          member.status === "administrator" ||
          member.status === "member" ||
          (member.status === "restricted" && member.is_member !== false));

      if (!isSubscribed) {
        missingChannels.push(ch);
      }
    } catch (error: any) {
      console.error(
        `[SubscriptionGuard] getChatMember xatoligi (${ch.username}, userId: ${userId}):`,
        error
      );
      // Muhim qoida: API xatosi berganda foydalanuvchini "a'zo emas" deb belgilamaslik!
      return {
        status: "error",
        message:
          "⚠️ <b>Kanal a'zoligini tekshirishda vaqtinchalik xatolik yuz berdi.</b>\n\n" +
          "Iltimos, birozdan so'ng qayta urinib ko'ring yoki bot ma'muriyatiga murojaat qiling.",
      };
    }
  }

  if (missingChannels.length > 0) {
    return {
      status: "not_subscribed",
      missingChannels,
    };
  }

  return { status: "subscribed" };
}

/**
 * Obuna talabi xabari va tugmalarini yaratish
 */
export function buildSubscriptionMessageAndKeyboard(quizId: string) {
  const text =
    `⚠️ <b>Testni boshlash uchun quyidagi kanallarga a'zo bo'ling:</b>\n\n` +
    `1. <a href="https://t.me/jdaquizkod">@jdaquizkod</a> — Quiz kodlari kanali\n` +
    `2. <a href="https://t.me/jdakimyouz">@jdakimyouz</a> — JDA Kimyo rasmiy kanali\n\n` +
    `Ikkala kanalga ham a'zo bo'lgach, quyidagi tekshirish tugmasini bosing:`;

  const reply_markup = {
    inline_keyboard: [
      [
        {
          text: "📢 @jdaquizkod ga a'zo bo'lish",
          url: "https://t.me/jdaquizkod",
        },
      ],
      [
        {
          text: "📢 @jdakimyouz ga a'zo bo'lish",
          url: "https://t.me/jdakimyouz",
        },
      ],
      [
        {
          text: "✅ A’zo bo‘ldim — tekshirish",
          callback_data: `check_sub_${quizId}`,
        },
      ],
    ],
  };

  return { text, reply_markup };
}
