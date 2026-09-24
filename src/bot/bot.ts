import { Bot } from "grammy";
import { handleStart } from "./handlers/start.js";
import { handleHelp } from "./handlers/help.js";
import {
  handleQuizCommand,
  handleQuizByIdCommand,
  handleStopQuizCommand,
  handleCheckSubscriptionCallback,
  handleRestartQuizCallback,
} from "./handlers/quiz.js";
import { handlePollAnswer } from "./handlers/pollAnswer.js";

export function createBot(token: string): Bot {
  const bot = new Bot(token);

  // Buyruqlarni ro'yxatdan o'tkazish
  bot.command("start", handleStart);
  bot.command("help", handleHelp);

  // /quiz_<ID> dinamik buyrug'i (masalan: /quiz_amino_acids)
  bot.hears(/^\/quiz_([a-zA-Z0-9_]+)(?:@\w+)?(?:\s.*)?$/i, handleQuizByIdCommand);

  // /quiz (Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz xabari yoki ID bilan boshlash)
  bot.command("quiz", handleQuizCommand);

  // /stop va /stopquiz (faol quizni to'xtatish)
  bot.command(["stop", "stopquiz"], handleStopQuizCommand);

  // Obunani qayta tekshirish («✅ A’zo bo‘ldim — tekshirish» callback query)
  bot.callbackQuery(/^check_sub_(.+)$/, handleCheckSubscriptionCallback);

  // Quizni qayta boshlash («🔄 Qayta yechish» callback query)
  bot.callbackQuery(/^restart_quiz_(.+)$/, handleRestartQuizCallback);

  // Telegram Quiz Poll javoblarini eshitish
  bot.on("poll_answer", handlePollAnswer);

  // Xatoliklarni tutish (error handling)
  bot.catch((err) => {
    const ctx = err.ctx;
    console.error(`[Bot Error] Update ${ctx.update.update_id} bajarilishida xatolik:`, err.error);
  });

  return bot;
}
