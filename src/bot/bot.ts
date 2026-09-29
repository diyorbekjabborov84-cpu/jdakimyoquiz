import { Bot } from "grammy";
import { handleStart } from "./handlers/start.js";
import { handleHelp } from "./handlers/help.js";
import {
  handleQuizCommand,
  handleQuizByIdCommand,
  handleStopQuizCommand,
  handleCheckSubscriptionCallback,
  handleRestartQuizCallback,
  handleResumeQuizCallback,
  handleResumeCommand,
} from "./handlers/quiz.js";
import { handlePollAnswer } from "./handlers/pollAnswer.js";
import { handleMyChatMember, handleNewChatMembers } from "./handlers/groupWelcome.js";
import { trackGroupUpdate } from "../tracking/groupRegistry.js";

export function createBot(token: string): Bot {
  const bot = new Bot(token);
  bot.use(trackGroupUpdate);

  // Bot guruhga qo'shilganda yo'riqnoma yuborish
  bot.on("my_chat_member", handleMyChatMember);
  bot.on(":new_chat_members", handleNewChatMembers);

  // Buyruqlarni ro'yxatdan o'tkazish
  bot.command("start", handleStart);
  bot.command("help", handleHelp);
  bot.command("resume", handleResumeCommand);

  // /quiz_<ID> va /start_<ID> dinamik buyruqlari (masalan: /quiz_amino_acids, /start_R1)
  bot.hears(/^\/(?:quiz|start)_([a-zA-Z0-9_]+)(?:@\w+)?(?:\s.*)?$/i, handleQuizByIdCommand);

  // /quiz (Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz xabari yoki ID bilan boshlash)
  bot.command("quiz", handleQuizCommand);

  // /stop va /stopquiz (faol yoki pauzadagi quizni to'xtatish)
  bot.command(["stop", "stopquiz"], handleStopQuizCommand);

  // Obunani qayta tekshirish («✅ A’zo bo‘ldim — tekshirish» callback query)
  bot.callbackQuery(/^check_sub_(.+)$/, handleCheckSubscriptionCallback);

  // Quizni qayta boshlash («🔄 Qayta yechish» callback query)
  bot.callbackQuery(/^restart_quiz_(.+)$/, handleRestartQuizCallback);

  // Aqlli pauzadan davom ettirish («▶️ Qolgan joyidan davom ettirish» callback query)
  bot.callbackQuery(/^resume_quiz(?:_|$)/, handleResumeQuizCallback);

  // Telegram Quiz Poll javoblarini eshitish
  bot.on("poll_answer", handlePollAnswer);

  // Xatoliklarni tutish (error handling)
  bot.catch((err) => {
    const ctx = err.ctx;
    console.error(`[Bot Error] Update ${ctx.update.update_id} bajarilishida xatolik:`, err.error);
  });

  return bot;
}
