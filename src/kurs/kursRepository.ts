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

    const mavzu = typeof item.mavzu === "string" ? item.mavzu.trim() : "";
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

      const savol = typeof t.savol === "string" ? t.savol.trim() : "";
      if (!savol) {
        errors.push(`${prefix} (${testId}): savol matni bo'sh`);
        continue;
      }

      const v = t.variantlar;
      if (!v || typeof v !== "object") {
        errors.push(`${prefix} (${testId}): variantlar obyekti yo'q`);
        continue;
      }

      const optA = typeof v.A === "string" ? v.A.trim() : "";
      const optB = typeof v.B === "string" ? v.B.trim() : "";
      const optC = typeof v.C === "string" ? v.C.trim() : "";
      const optD = typeof v.D === "string" ? v.D.trim() : "";

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

    const mashqlar: RawKursMashqItem[] = Array.isArray(item.mashqlar)
      ? item.mashqlar
          .filter((m: any) => m && typeof m.id === "string" && typeof m.savol === "string")
          .map((m: any) => ({
            id: m.id.trim(),
            savol: m.savol.trim(),
            yechim: typeof m.yechim === "string" ? m.yechim : undefined,
          }))
      : [];

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

export function buildQuizFromKursDars(darsObj: RawKursDars): Quiz | null {
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
      timeLimitSeconds: 30,
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
    const quiz = buildQuizFromKursDars(d);
    nextMap.set(d.dars, {
      dars: d.dars,
      mavzu: d.mavzu,
      papka: d.papka,
      testlarSoni: quiz ? quiz.questions.length : 0,
      mashqlarSoni: Array.isArray(d.mashqlar) ? d.mashqlar.length : 0,
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
      mashqlar: Array.isArray(data.mashqlar) ? data.mashqlar : [],
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
