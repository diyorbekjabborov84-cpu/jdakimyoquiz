import { Context } from "grammy";
import { quizManager } from "../../quiz/quizManager.js";
import { trackUserEvent } from "../../tracking/tracker.js";

/**
 * Telegram'dan kelgan poll_answer update'ini qayta ishlash
 */
export async function handlePollAnswer(ctx: Context): Promise<void> {
  const answer = ctx.pollAnswer;
  if (!answer) return;

  const { poll_id, user, option_ids } = answer;
  if (!user) return;

  // Foydalanuvchi faolligini asinxron (non-blocking) tarzda yozish
  trackUserEvent(user.id, {
    firstName: user.first_name,
    lastName: user.last_name,
    username: user.username,
  }).catch(() => {});

  await quizManager.handlePollAnswer({
    pollId: poll_id,
    user: {
      id: user.id,
      first_name: user.first_name,
      last_name: user.last_name,
      username: user.username,
    },
    optionIds: option_ids,
  });
}
