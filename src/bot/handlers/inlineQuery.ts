import { Context } from "grammy";
import { allQuizzes } from "../../quiz/questions.js";
import { Quiz } from "../../quiz/types.js";
import {
  formatKursQuizId,
  getActiveKursLessons,
  LoadedKursLesson,
} from "../../kurs/kursRepository.js";
import { canUserAccessKursInInlineQuery } from "../../shell/shell.js";
import { getBotSettings } from "../../settings/botSettings.js";

export interface InlineCardButton {
  text: string;
  url?: string;
  switch_inline_query?: string;
}

export interface InlineQuizArticleResult {
  type: "article";
  id: string;
  title: string;
  description: string;
  input_message_content: {
    message_text: string;
  };
  reply_markup: {
    inline_keyboard: InlineCardButton[][];
  };
}

export const INLINE_QUERY_MAX_RESULTS = 50;
export const INLINE_QUERY_CACHE_TIME_SECONDS = 10;

/**
 * Telegram /start va /startgroup deep-link payload tekshiruvi:
 * 1..64 belgi va faqat [A-Za-z0-9_] bo'lishi shart.
 */
export function isValidQuizStartPayload(payload: string): boolean {
  return (
    typeof payload === "string" &&
    payload.length >= 1 &&
    payload.length <= 64 &&
    /^[A-Za-z0-9_]+$/.test(payload)
  );
}

/**
 * Quiz kartochkasi (InlineQueryResultArticle) yasash yordamchisi.
 * Kurs darslari, asosiy quizlar va kelajakdagi yangi quiz turlari uchun umumiy.
 */
export function buildQuizInlineArticle(params: {
  quizId: string;
  cardTitle: string;
  questionsCount: number;
  timeLimitSeconds: number;
  botUsername: string;
}): InlineQuizArticleResult | null {
  const quizId = params.quizId.trim();
  const startPayload = `quiz_${quizId}`;
  if (!isValidQuizStartPayload(startPayload)) {
    return null;
  }

  const cleanBotUsername =
    params.botUsername.replace(/^@/, "").trim() || "jdakimyoquizbot";
  const headline = `🎲 «${params.cardTitle}» testi`;
  const metaLine = `🖊 ${params.questionsCount} ta savol · ⏱ ${params.timeLimitSeconds} soniya`;

  return {
    type: "article",
    id: quizId,
    title: `«${params.cardTitle}» testi`,
    description: metaLine,
    input_message_content: {
      message_text: `${headline}\n\n${metaLine}`,
    },
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: "Bu testni boshlash",
            url: `https://t.me/${cleanBotUsername}?start=${startPayload}`,
          },
        ],
        [
          {
            text: "Guruhda testni boshlash",
            url: `https://t.me/${cleanBotUsername}?startgroup=${startPayload}`,
          },
        ],
        [
          {
            text: "Testni ulashish",
            switch_inline_query: quizId,
          },
        ],
      ],
    },
  };
}

export function buildKursLessonInlineArticle(
  lesson: LoadedKursLesson,
  kursQuestionTimeSeconds: number,
  botUsername: string
): InlineQuizArticleResult | null {
  const quizId = formatKursQuizId(lesson.dars);
  const cardTitle = `${lesson.dars}-dars: ${lesson.mavzu}`;
  return buildQuizInlineArticle({
    quizId,
    cardTitle,
    questionsCount: lesson.testlarSoni,
    timeLimitSeconds: kursQuestionTimeSeconds,
    botUsername,
  });
}

export function buildAsosiyQuizInlineArticle(
  quiz: Quiz,
  botUsername: string
): InlineQuizArticleResult | null {
  const timeSec = quiz.questions[0]?.timeLimitSeconds || 20;
  return buildQuizInlineArticle({
    quizId: quiz.id,
    cardTitle: quiz.title,
    questionsCount: quiz.questions.length,
    timeLimitSeconds: timeSec,
    botUsername,
  });
}

function matchesKursLessonQuery(lesson: LoadedKursLesson, rawQuery: string): boolean {
  const trimmed = rawQuery.trim();
  if (!trimmed) return true;

  const q = trimmed.toLowerCase().replace(/^(quiz_|start_)/i, "");
  if (/^\d+$/.test(q)) {
    const num = Number(q);
    return lesson.dars === num || lesson.mavzu.toLowerCase().includes(q);
  }

  const quizIdLower = formatKursQuizId(lesson.dars).toLowerCase();
  const darsPadded = `d${String(lesson.dars).padStart(2, "0")}`;
  const darsShort = `d${lesson.dars}`;
  const darsLabel = `${lesson.dars}-dars`;
  const mavzuLower = lesson.mavzu.toLowerCase();
  const titleLower = (lesson.quiz?.title || "").toLowerCase();

  return (
    quizIdLower.includes(q) ||
    darsPadded.includes(q) ||
    darsShort === q ||
    darsLabel.includes(q) ||
    mavzuLower.includes(q) ||
    titleLower.includes(q)
  );
}

function matchesAsosiyQuizQuery(quiz: Quiz, rawQuery: string): boolean {
  const trimmed = rawQuery.trim();
  if (!trimmed) return true;

  const q = trimmed.toLowerCase().replace(/^(quiz_|start_)/i, "");
  const qCompact = q.replace(/[-_\s]/g, "");
  const idLower = quiz.id.toLowerCase();
  const idCompact = idLower.replace(/[-_\s]/g, "");
  const titleLower = quiz.title.toLowerCase();
  const bolimLower = (quiz.bolim || "").toLowerCase();

  return (
    idLower.includes(q) ||
    (qCompact.length >= 2 && idCompact.includes(qCompact)) ||
    titleLower.includes(q) ||
    bolimLower.includes(q)
  );
}

/**
 * Inline query (@jdakimyoquizbot ...) uchun asosiy handler.
 */
export async function handleInlineQuery(ctx: Context): Promise<void> {
  const userId = ctx.inlineQuery?.from?.id ?? ctx.from?.id;
  const rawQuery = ctx.inlineQuery?.query ?? "";
  const botUsername =
    (ctx.me as any)?.username || process.env.BOT_USERNAME || "jdakimyoquizbot";

  // Fail-closed ruxsat tekshiruvi: xato bo'lsa false qaytadi va kurs kartochkalari ko'rinmaydi
  const canSeeKurs = await canUserAccessKursInInlineQuery(ctx, userId);

  const settings = await getBotSettings();
  const kursTimeSec = settings.kursQuestionTimeSeconds || 25;

  const results: InlineQuizArticleResult[] = [];

  if (canSeeKurs) {
    // Bo'sh so'rovda oxirgi darslar yuqorida turadi (dars raqami kamayish tartibida)
    const kursLessonsDesc = [...getActiveKursLessons()].sort((a, b) => b.dars - a.dars);
    for (const lesson of kursLessonsDesc) {
      if (!matchesKursLessonQuery(lesson, rawQuery)) continue;
      const article = buildKursLessonInlineArticle(lesson, kursTimeSec, botUsername);
      if (article) {
        results.push(article);
      }
    }

    // Agar so'rov faqat dars raqami bo'lib (masalan "3") kurs darsi topilgan bo'lsa,
    // natijani aniq dars bilan cheklaymiz; aks holda mos asosiy quizlarni ham qo'shamiz.
    const isPureLessonNumberMatch =
      /^\d+$/.test(rawQuery.trim()) && results.length > 0;

    if (!isPureLessonNumberMatch) {
      for (const quiz of allQuizzes) {
        if (results.length >= INLINE_QUERY_MAX_RESULTS) break;
        if (!matchesAsosiyQuizQuery(quiz, rawQuery)) continue;
        const article = buildAsosiyQuizInlineArticle(quiz, botUsername);
        if (article) {
          results.push(article);
        }
      }
    }
  } else {
    // Kurs ishtirokchisi bo'lmaganlar uchun faqat asosiy qobiq quizlari ko'rsatiladi
    for (const quiz of allQuizzes) {
      if (results.length >= INLINE_QUERY_MAX_RESULTS) break;
      if (!matchesAsosiyQuizQuery(quiz, rawQuery)) continue;
      const article = buildAsosiyQuizInlineArticle(quiz, botUsername);
      if (article) {
        results.push(article);
      }
    }
  }

  await ctx.answerInlineQuery(results.slice(0, INLINE_QUERY_MAX_RESULTS) as any, {
    is_personal: true,
    cache_time: INLINE_QUERY_CACHE_TIME_SECONDS,
  });
}
