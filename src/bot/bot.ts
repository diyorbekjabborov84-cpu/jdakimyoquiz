import { Bot } from "grammy";
import { handleStart } from "./handlers/start.js";
import { handleHelp } from "./handlers/help.js";
import { handleQuizCommand, handleStopQuizCommand } from "./handlers/quiz.js";
import { handlePollAnswer } from "./handlers/pollAnswer.js";

export function createBot(token: string): Bot {
  const bot = new Bot(token);

  // Buyruqlarni ro'yxatdan o'tkazish
  bot.command("start", handleStart);
  bot.command("help", handleHelp);
  bot.command("quiz", handleQuizCommand);
  bot.command("stopquiz", handleStopQuizCommand);

  // Telegram Quiz Poll javoblarini eshitish
  bot.on("poll_answer", handlePollAnswer);

  // Xatoliklarni tutish (error handling)
  bot.catch((err) => {
    const ctx = err.ctx;
    console.error(`[Bot Error] Update ${ctx.update.update_id} bajarilishida xatolik:`, err.error);
  });

  return bot;
}
