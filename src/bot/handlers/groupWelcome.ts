import { Context } from "grammy";
import { trackGroupEvent } from "../../tracking/tracker.js";

// Bir xil guruhga qisqa vaqt ichida takroriy yuborilishining oldini oluvchi kesh (chatId -> timestamp)
const recentlyWelcomed = new Map<number, number>();

/**
 * my_chat_member hodisasi: Bot guruhga qo'shilganda yoki huquqlari o'zgarganda chaqiriladi.
 * Qat'iy qoida: Xabar faqat bot yangi qo'shilganda chiqsin.
 * Har /startda yoki admin huquqi o'zgarganda takrorlanmasin!
 */
export async function handleMyChatMember(ctx: Context): Promise<void> {
  if (!ctx.chat || (ctx.chat.type !== "group" && ctx.chat.type !== "supergroup")) {
    return;
  }

  const myChatMember = ctx.myChatMember;
  if (!myChatMember) return;

  const oldStatus = myChatMember.old_chat_member.status;
  const newStatus = myChatMember.new_chat_member.status;

  // Guruhdan chiqarilish yoki chiqib ketish holati
  if (newStatus === "left" || newStatus === "kicked") {
    trackGroupEvent(ctx.chat.id, {
      title: (ctx.chat as any).title,
      type: ctx.chat.type,
      status: newStatus === "kicked" ? "kicked" : "left",
    }).catch(() => {});
    return;
  }

  // Bot avval guruhda bo'lmagan (left yoki kicked) va endi qo'shilgan (member yoki administrator)
  const isOldLeftOrKicked = oldStatus === "left" || oldStatus === "kicked";
  const isNewMemberOrAdmin = newStatus === "member" || newStatus === "administrator";

  if (isNewMemberOrAdmin) {
    trackGroupEvent(ctx.chat.id, {
      title: (ctx.chat as any).title,
      type: ctx.chat.type,
      status: "active",
    }).catch(() => {});
  }

  if (!isOldLeftOrKicked || !isNewMemberOrAdmin) {
    // Agar bot allaqachon a'zo bo'lib, keyin admin qilingan bo'lsa yoki boshqa status o'zgarishi bo'lsa chiqmaydi
    return;
  }

  await sendGroupWelcomeMessage(ctx, ctx.chat.id);
}

/**
 * message:new_chat_members hodisasi:
 * Foydalanuvchi botni guruhga a'zo sifatida qo'shganda keladigan servis xabari
 */
export async function handleNewChatMembers(ctx: Context): Promise<void> {
  if (!ctx.chat || (ctx.chat.type !== "group" && ctx.chat.type !== "supergroup")) {
    return;
  }

  const newMembers = ctx.message?.new_chat_members;
  if (!newMembers || newMembers.length === 0) return;

  const botId = ctx.me?.id;
  // Bot o'zi yangi qo'shilganlar ro'yxatida bormi
  const isBotAdded = botId ? newMembers.some((u) => u.id === botId) : false;

  if (!isBotAdded) {
    return;
  }

  trackGroupEvent(ctx.chat.id, {
    title: (ctx.chat as any).title,
    type: ctx.chat.type,
    status: "active",
  }).catch(() => {});

  await sendGroupWelcomeMessage(ctx, ctx.chat.id);
}

/**
 * Guruhga qo'shilgandagi yo'riqnoma xabarini yuborish
 */
export async function sendGroupWelcomeMessage(ctx: Context, chatId: number): Promise<void> {
  const now = Date.now();
  const lastSent = recentlyWelcomed.get(chatId) || 0;
  if (now - lastSent < 15000) {
    // 15 soniya ichida bu guruhga allaqachon yo'riqnoma yuborilgan (dublikatni cheklash)
    return;
  }
  recentlyWelcomed.set(chatId, now);

  const text =
    `🧪 <b>JDA QUIZ guruhga qo‘shildi!</b>\n\n` +
    `1. JDA QUIZ botini guruh administratori qiling.\n` +
    `2. Kerakli test kodlarini @jdaquizkod kanalidan oling.\n` +
    `3. Test kodini guruhga yuborib quizni boshlang. Quiz uchun guruhda botdan tashqari kamida 12 kishi bo'lishi kerak.\n\n` +
    `Muammo, taklif yoki savollar uchun: <a href="https://t.me/diyorbek_jabborov">@diyorbek_jabborov</a>`;

  await ctx.api.sendMessage(chatId, text, {
    parse_mode: "HTML",
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: "📢 Test kodlari",
            url: "https://t.me/jdaquizkod",
          },
        ],
      ],
    },
  });
}
