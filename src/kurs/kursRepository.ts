import { Quiz, QuizQuestion } from "../quiz/types.js";
import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";

export interface RawKursTestItem {
  id: string;
  savol: string;
  variantlar: {
    A: string;
    B: string;
    C: string;
    D: string;
  };
  javob: "A" | "B" | "C" | "D";
  qiyinlik?: string;
}

export interface RawKursMashqItem {
  id: string;
  savol: string;
  yechim?: string;
}

export interface RawKursDars {
  dars: number;
  mavzu: string;
  papka?: string;
  testlar: RawKursTestItem[];
  mashqlar?: RawKursMashqItem[];
  updatedAt?: string;
}

export interface LoadedKursLesson {
  dars: number;
  mavzu: string;
  papka?: string;
  testlarSoni: number;
  mashqlarSoni: number;
  updatedAt: string | null;
  quiz: Quiz | null;
}

export interface KursDarsAdminMeta {
  dars: number;
  quizId: string;
  mavzu: string;
  papka: string | null;
  testlarSoni: number;
  mashqlarSoni: number;
  updatedAt: string | null;
}

const VALID_ANSWERS = ["A", "B", "C", "D"] as const;
const MAX_EXPLANATION_LENGTH = 200;

let loadedLessonsMap = new Map<number, LoadedKursLesson>();
let lastLoadedAt: string | null = null;

export function formatKursQuizId(dars: number): string {
  const padded = String(dars).padStart(2, "0");
  return `KURS_D${padded}`;
}

export function parseKursDarsNumberFromQuizId(rawId: string): number | null {
  if (!rawId) return null;
  const cleaned = rawId.trim().replace(/^(quiz_|start_)/i, "");
  const match = cleaned.match(/^kurs_d0*(\d+)$/i);
  if (!match) return null;
  const num = Number(match[1]);
  if (!Number.isInteger(num) || num <= 0) return null;
  return num;
}

export function isKursQuizId(rawId: string): boolean {
  return parseKursDarsNumberFromQuizId(rawId) !== null;
}

export function formatKursExplanation(dars: number, mavzu: string): string {
  const prefix = `📺 ${dars}-dars: `;
  const suffix = ` — videoni qayta ko‘ring.`;
  const cleanMavzu = (mavzu || "").trim();
  const full = `${prefix}${cleanMavzu}${suffix}`;
  if (full.length <= MAX_EXPLANATION_LENGTH) {
    return full;
  }
  const maxMavzuLen = Math.max(10, MAX_EXPLANATION_LENGTH - prefix.length - suffix.length - 1);
  return `${prefix}${cleanMavzu.slice(0, maxMavzuLen).trimEnd()}…${suffix}`;
}

const SUBSCRIPT_MAP: Record<string, string> = Object.fromEntries(
  [..."0123456789+-=()aehijklmnoprstuvx"].map((ch, i) => [ch, [..."₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ"][i]])
);
const SUPERSCRIPT_MAP: Record<string, string> = Object.fromEntries(
  [..."0123456789+-=()n"].map((ch, i) => [ch, [..."⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ"][i]])
);
const HTML_ENTITIES: Record<string, string> = {
  amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", minus: "−", middot: "·", rarr: "→",
};

/**
 * Qo'llanma HTML'idan kelgan matnni Telegram poll uchun toza matnga aylantiradi:
 * <sub>/<sup> → Unicode indekslar (H<sub>2</sub>O → H₂O, A<sub>r</sub> → Aᵣ),
 * qolgan teglar olib tashlanadi, HTML entity'lar ochiladi.
 * Unicode'da mos belgi bo'lmasa, harf o'zgarishsiz qoladi.
 */
export function cleanKursText(raw: string): string {
  const mapChars = (s: string, map: Record<string, string>) =>
    [...s].map((ch) => map[ch] ?? ch).join("");
  return raw
    .replace(/<sub>([\s\S]*?)<\/sub>/gi, (_, s: string) => mapChars(s, SUBSCRIPT_MAP))
    .replace(/<sup>([\s\S]*?)<\/sup>/gi, (_, s: string) => mapChars(s, SUPERSCRIPT_MAP))
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/<\/?[a-z][^>]*>/gi, "")
    .replace(/&(#\d+|#x[0-9a-f]+|[a-z]+);/gi, (m, e: string) => {
      if (e[0] === "#") {
        const code = e[1].toLowerCase() === "x" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
        return Number.isFinite(code) ? String.fromCodePoint(code) : m;
      }
      return HTML_ENTITIES[e.toLowerCase()] ?? m;
    })
    .replace(/\s{2,}/g, " ")
    .trim();
}

export function normalizeKursMashqlar(rawMashqlar: unknown, darsNum: number): RawKursMashqItem[] {
  if (!Array.isArray(rawMashqlar)) return [];
  const darsPrefix = `d${String(darsNum).padStart(2, "0")}`;
  const result: RawKursMashqItem[] = [];

  for (let idx = 0; idx < rawMashqlar.length; idx++) {
    const m = rawMashqlar[idx];
    const fallbackId = `${darsPrefix}_m${String(idx + 1).padStart(2, "0")}`;
    if (typeof m === "string") {
      const trimmed = cleanKursText(m);
      if (trimmed) {
        result.push({
          id: fallbackId,
          savol: trimmed,
        });
      }
    } else if (m && typeof m === "object") {
      const obj = m as Record<string, unknown>;
      const savol = typeof obj.savol === "string" ? cleanKursText(obj.savol) : "";
      if (!savol) continue;
      const id = typeof obj.id === "string" && obj.id.trim() ? obj.id.trim() : fallbackId;
      const yechim = typeof obj.yechim === "string" ? cleanKursText(obj.yechim) : "";
      result.push({
        id,
        savol,
        ...(yechim ? { yechim } : {}),
      });
    }
  }

  return result;
}

export function validateKursDarslarPayload(darslar: unknown[]): {
  valid: boolean;
  errors: string[];
  validated: RawKursDars[];
} {
  const errors: string[] = [];
  const validated: RawKursDars[] = [];
  const seenLessonNumbers = new Set<number>();
  const seenTestIds = new Set<string>();

  if (!Array.isArray(darslar)) {
    return { valid: false, errors: ["darslar massivi topilmadi"], validated: [] };
  }

  for (let i = 0; i < darslar.length; i++) {
    const item = darslar[i] as any;
    if (!item || typeof item !== "object") {
      errors.push(`darslar[${i}] obyekt emas`);
      continue;
    }

    const darsNum = Number(item.dars);
    if (!Number.isInteger(darsNum) || darsNum <= 0) {
      errors.push(`darslar[${i}].dars musbat butun son bo'lishi kerak`);
      continue;
    }

    if (seenLessonNumbers.has(darsNum)) {
      errors.push(`${darsNum}-dars takrorlangan`);
      continue;
    }
    seenLessonNumbers.add(darsNum);

    const mavzu = typeof item.mavzu === "string" ? cleanKursText(item.mavzu) : "";
    if (!mavzu) {
      errors.push(`${darsNum}-dars uchun mavzu bo'sh`);
      continue;
    }

    const rawTests = Array.isArray(item.testlar) ? item.testlar : [];
    const cleanTests: RawKursTestItem[] = [];

    for (let j = 0; j < rawTests.length; j++) {
      const t = rawTests[j];
      const prefix = `${darsNum}-dars testlar[${j}]`;
      if (!t || typeof t !== "object") {
        errors.push(`${prefix} obyekt emas`);
        continue;
      }

      const testId = typeof t.id === "string" ? t.id.trim() : "";
      if (!testId) {
        errors.push(`${prefix}: id bo'sh`);
        continue;
      }
      if (seenTestIds.has(testId)) {
        errors.push(`${prefix}: id '${testId}' takrorlangan`);
        continue;
      }
      seenTestIds.add(testId);

      const savol = typeof t.savol === "string" ? cleanKursText(t.savol) : "";
      if (!savol) {
        errors.push(`${prefix} (${testId}): savol matni bo'sh`);
        continue;
      }

      const v = t.variantlar;
      if (!v || typeof v !== "object") {
        errors.push(`${prefix} (${testId}): variantlar obyekti yo'q`);
        continue;
      }

      const optA = typeof v.A === "string" ? cleanKursText(v.A) : "";
      const optB = typeof v.B === "string" ? cleanKursText(v.B) : "";
      const optC = typeof v.C === "string" ? cleanKursText(v.C) : "";
      const optD = typeof v.D === "string" ? cleanKursText(v.D) : "";

      if (!optA || !optB || !optC || !optD) {
        errors.push(`${prefix} (${testId}): 4 ta variant (A, B, C, D) to'liq bo'lishi shart`);
        continue;
      }

      const javob = typeof t.javob === "string" ? t.javob.trim().toUpperCase() : "";
      if (!VALID_ANSWERS.includes(javob as any)) {
        errors.push(`${prefix} (${testId}): javob faqat A, B, C yoki D bo'lishi kerak`);
        continue;
      }

      cleanTests.push({
        id: testId,
        savol,
        variantlar: { A: optA, B: optB, C: optC, D: optD },
        javob: javob as "A" | "B" | "C" | "D",
        qiyinlik: typeof t.qiyinlik === "string" ? t.qiyinlik : undefined,
      });
    }

    const mashqlar = normalizeKursMashqlar(item.mashqlar, darsNum);

    validated.push({
      dars: darsNum,
      mavzu,
      papka: typeof item.papka === "string" ? item.papka.trim() : undefined,
      testlar: cleanTests,
      mashqlar,
      updatedAt: typeof item.updatedAt === "string" ? item.updatedAt : undefined,
    });
  }

  validated.sort((a, b) => a.dars - b.dars);
  return {
    valid: errors.length === 0,
    errors,
    validated,
  };
}

export function buildQuizFromKursDars(darsObj: RawKursDars, timeLimitSeconds = 25): Quiz | null {
  if (!Array.isArray(darsObj.testlar) || darsObj.testlar.length === 0) {
    return null;
  }

  const explanation = formatKursExplanation(darsObj.dars, darsObj.mavzu);
  const questions: QuizQuestion[] = [];

  for (const t of darsObj.testlar) {
    const answerIndex = VALID_ANSWERS.indexOf(t.javob);
    if (answerIndex === -1) continue;
    if (!t.variantlar?.A || !t.variantlar?.B || !t.variantlar?.C || !t.variantlar?.D) continue;

    questions.push({
      id: t.id,
      question: t.savol,
      options: [t.variantlar.A, t.variantlar.B, t.variantlar.C, t.variantlar.D],
      correctOptionId: answerIndex,
      explanation,
      timeLimitSeconds,
    });
  }

  if (questions.length === 0) {
    return null;
  }

  return {
    id: formatKursQuizId(darsObj.dars),
    title: `${darsObj.dars}-dars bo‘yicha test`,
    description: `📚 «Kimyo 0 dan» — ${darsObj.dars}-dars: ${darsObj.mavzu}`,
    source: "JDA Kimyo — Kimyo 0 dan",
    groupOnly: false,
    shuffle: true,
    questions,
  };
}

export function populateKursMemory(rawDarslar: RawKursDars[]): number {
  const nextMap = new Map<number, LoadedKursLesson>();
  const sorted = [...rawDarslar].sort((a, b) => a.dars - b.dars);

  for (const d of sorted) {
    const normalizedMashqlar = normalizeKursMashqlar(d.mashqlar, d.dars);
    const quiz = buildQuizFromKursDars(d);
    nextMap.set(d.dars, {
      dars: d.dars,
      mavzu: d.mavzu,
      papka: d.papka,
      testlarSoni: quiz ? quiz.questions.length : 0,
      mashqlarSoni: normalizedMashqlar.length,
      updatedAt: d.updatedAt || null,
      quiz,
    });
  }

  loadedLessonsMap = nextMap;
  lastLoadedAt = new Date().toISOString();
  return loadedLessonsMap.size;
}

export async function loadKursDarslarFromFirestore(): Promise<{
  lessonsCount: number;
  quizzesCount: number;
}> {
  const db = getFirestoreDb();
  if (!db) {
    return {
      lessonsCount: loadedLessonsMap.size,
      quizzesCount: getKursQuizzes().length,
    };
  }

  const snap = await db.collection(FIRESTORE_COLLECTIONS.KURS_LESSONS).get();
  const rawList: RawKursDars[] = [];

  for (const doc of snap.docs) {
    const data = doc.data();
    if (!data || typeof data.dars !== "number" || typeof data.mavzu !== "string") {
      continue;
    }
    rawList.push({
      dars: data.dars,
      mavzu: data.mavzu,
      papka: typeof data.papka === "string" ? data.papka : undefined,
      testlar: Array.isArray(data.testlar) ? data.testlar : [],
      mashqlar: normalizeKursMashqlar(data.mashqlar, data.dars),
      updatedAt: typeof data.updatedAt === "string" ? data.updatedAt : undefined,
    });
  }

  populateKursMemory(rawList);
  const quizzesCount = getKursQuizzes().length;
  console.log(
    `[KursRepository] Firestore'dan ${loadedLessonsMap.size} ta dars (${quizzesCount} ta faol test) xotiraga yuklandi.`
  );
  return {
    lessonsCount: loadedLessonsMap.size,
    quizzesCount,
  };
}

export async function reloadKursDarslar(): Promise<{
  lessonsCount: number;
  quizzesCount: number;
  reloadedAt: string;
}> {
  const res = await loadKursDarslarFromFirestore();
  return {
    ...res,
    reloadedAt: lastLoadedAt || new Date().toISOString(),
  };
}

export function getKursLessons(): LoadedKursLesson[] {
  return Array.from(loadedLessonsMap.values()).sort((a, b) => a.dars - b.dars);
}

export function getActiveKursLessons(): LoadedKursLesson[] {
  return getKursLessons().filter((l) => l.quiz !== null && l.testlarSoni > 0);
}

export function getKursLessonByNumber(dars: number): LoadedKursLesson | undefined {
  return loadedLessonsMap.get(dars);
}

export function getKursQuizzes(): Quiz[] {
  return getActiveKursLessons().map((l) => l.quiz!);
}

export function getKursQuizById(rawId: string): Quiz | undefined {
  const darsNum = parseKursDarsNumberFromQuizId(rawId);
  if (darsNum === null) return undefined;
  return loadedLessonsMap.get(darsNum)?.quiz || undefined;
}

/**
 * Admin API uchun darslar metama'lumoti (javob kalitlari aslo qaytarilmaydi!)
 */
export async function getKursDarslarAdminMeta(): Promise<{
  darslar: KursDarsAdminMeta[];
  lastLoadedAt: string | null;
}> {
  if (loadedLessonsMap.size === 0 && getFirestoreDb()) {
    try {
      await loadKursDarslarFromFirestore();
    } catch (err) {
      console.error("[KursRepository] Admin meta uchun yuklashda xatolik:", err);
    }
  }

  const darslar: KursDarsAdminMeta[] = getKursLessons().map((l) => ({
    dars: l.dars,
    quizId: formatKursQuizId(l.dars),
    mavzu: l.mavzu,
    papka: l.papka || null,
    testlarSoni: l.testlarSoni,
    mashqlarSoni: l.mashqlarSoni,
    updatedAt: l.updatedAt,
  }));

  return {
    darslar,
    lastLoadedAt,
  };
}

export function clearKursDarslarForTest(): void {
  loadedLessonsMap.clear();
  lastLoadedAt = null;
}
