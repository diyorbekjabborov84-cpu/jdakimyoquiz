import { Bot, type Context } from "grammy";
import { handleStart } from "./handlers/start.js";
import { handleHelp } from "./handlers/help.js";
import {
  handleQuizCommand,
  handleQuizByIdCommand,
  handleStopQuizCommand,
  handleStopQuizCallback,
  handleCheckSubscriptionCallback,
  handleRestartQuizCallback,
  handleResumeQuizCallback,
  handleResumeCommand,
} from "./handlers/quiz.js";
import { handleMenuCallback } from "./handlers/menu.js";
import { handleInlineQuery } from "./handlers/inlineQuery.js";
import { handlePollAnswer } from "./handlers/pollAnswer.js";
import { handleMyChatMember, handleNewChatMembers } from "./handlers/groupWelcome.js";
import { trackGroupUpdate } from "../tracking/groupRegistry.js";

export function createBot(token: string): Bot {
  const bot = new Bot(token);
  bot.use(trackGroupUpdate);

  // Bot guruhga qo'shilganda yo'riqnoma yuborish
  bot.on("my_chat_member", handleMyChatMember);
  bot.on(":new_chat_members", handleNewChatMembers);

  const cleanGroupCommand = (handler: (ctx: Context) => Promise<void>) =>
    async (ctx: Context) => {
      const recipient = ctx.message?.text?.match(/^\/\S+?@(\w+)(?=\s|$)/)?.[1];
      if (recipient && recipient.toLowerCase() !== ctx.me.username.toLowerCase()) return;

      try {
        await handler(ctx);
      } finally {
        if (ctx.chat?.type === "group" || ctx.chat?.type === "supergroup") {
          await ctx.deleteMessage().catch((err) => {
            console.warn(`[Bot] Guruhdagi buyruq xabarini o‘chirib bo‘lmadi (${ctx.chat?.id}):`, err);
          });
        }
      }
    };

  bot.command("start", cleanGroupCommand(handleStart));
  bot.command("help", cleanGroupCommand(handleHelp));
  bot.command("resume", cleanGroupCommand(handleResumeCommand));
  bot.hears(/^\/(?:quiz|start)_([a-zA-Z0-9_]+)(?:@\w+)?(?:\s.*)?$/i, cleanGroupCommand(handleQuizByIdCommand));
  bot.command("quiz", cleanGroupCommand(handleQuizCommand));
  bot.command(["stop", "stopquiz"], cleanGroupCommand(handleStopQuizCommand));
  bot.callbackQuery(/^stop_quiz_(.+)$/, handleStopQuizCallback);

  // Obunani qayta tekshirish («✅ A’zo bo‘ldim — tekshirish» callback query)
  bot.callbackQuery(/^check_sub_(.+)$/, handleCheckSubscriptionCallback);

  // Quizni qayta boshlash («🔄 Qayta yechish» callback query)
  bot.callbackQuery(/^restart_quiz_(.+)$/, handleRestartQuizCallback);

  // Aqlli pauzadan davom ettirish («▶️ Qolgan joyidan davom ettirish» callback query)
  bot.callbackQuery(/^resume_quiz(?:_|$)/, handleResumeQuizCallback);

  // Inline menyu (m:k:... va m:a:...) callback querylari
  bot.callbackQuery(/^m:(?:k|a):/, handleMenuCallback);

  // Inline query (@jdakimyoquizbot ...) kartochkalari
  bot.on("inline_query", handleInlineQuery);

  // Telegram Quiz Poll javoblarini eshitish
  bot.on("poll_answer", handlePollAnswer);

  // Xatoliklarni tutish (error handling)
  bot.catch((err) => {
    const ctx = err.ctx;
    console.error(`[Bot Error] Update ${ctx.update.update_id} bajarilishida xatolik:`, err.error);
  });

  return bot;
}
