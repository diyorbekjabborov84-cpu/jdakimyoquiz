import { Quiz } from "./types.js";

/**
 * 329–330-betlardagi 17-jadval asosida 21 ta aminokislotaning
 * suyuqlanish temperaturasi bo'yicha birinchi haqiqiy kimyo quizi.
 */
export const aminoAcidsQuiz: Quiz = {
  id: "amino_acids",
  title: "Aminokislotalar — suyuqlanish temperaturasi",
  description: "329–330-betlardagi 17-jadval asosida 21 ta aminokislotaning suyuqlanish temperaturasi bo'yicha interaktiv quiz",
  groupOnly: true,
  questions: [
    {
      id: "aa_1",
      question: "Jadvalga ko‘ra, Glitsinning suyuqlanish temperaturasi qancha?",
      options: ["284 °C", "292 °C", "297 °C", "315 °C"],
      correctOptionId: 1, // 292 °C
      explanation: "Glitsin (Gli.) ning suyuqlanish temperaturasi: 292 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_2",
      question: "Jadvalga ko‘ra, Alaninning suyuqlanish temperaturasi qancha?",
      options: ["297 °C", "275 °C", "283 °C", "292 °C"],
      correctOptionId: 0, // 297 °C
      explanation: "Alanin (Ala.) ning suyuqlanish temperaturasi: 297 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_3",
      question: "Jadvalga ko‘ra, Valinning suyuqlanish temperaturasi qancha?",
      options: ["299 °C", "315 °C", "337 °C", "344 °C"],
      correctOptionId: 1, // 315 °C
      explanation: "Valin (Val.) ning suyuqlanish temperaturasi: 315 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_4",
      question: "Jadvalga ko‘ra, Leysinning suyuqlanish temperaturasi qancha?",
      options: ["315 °C", "325 °C", "337 °C", "382 °C"],
      correctOptionId: 2, // 337 °C
      explanation: "Leysin (Ley.) ning suyuqlanish temperaturasi: 337 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_5",
      question: "Jadvalga ko‘ra, Izoleysinning suyuqlanish temperaturasi qancha?",
      options: ["270 °C", "283 °C", "284 °C", "292 °C"],
      correctOptionId: 2, // 284 °C
      explanation: "Izoleysin (Iley.) ning suyuqlanish temperaturasi: 284 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_6",
      question: "Jadvalga ko‘ra, Asparagin kislotaning suyuqlanish temperaturasi qancha?",
      options: ["249 °C", "260 °C", "270 °C", "277 °C"],
      correctOptionId: 2, // 270 °C
      explanation: "Asparagin kislota (Asp.) ning suyuqlanish temperaturasi: 270 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_7",
      question: "Jadvalga ko‘ra, Glutamin kislotaning suyuqlanish temperaturasi qancha?",
      options: ["238 °C", "249 °C", "253 °C", "270 °C"],
      correctOptionId: 1, // 249 °C
      explanation: "Glutamin kislota (Glu.) ning suyuqlanish temperaturasi: 249 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_8",
      question: "Jadvalga ko‘ra, Ornitinning suyuqlanish temperaturasi qancha?",
      options: ["140 °C", "160 °C", "178 °C", "224 °C"],
      correctOptionId: 0, // 140 °C
      explanation: "Ornitin (Ori.) ning suyuqlanish temperaturasi: 140 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_9",
      question: "Jadvalga ko‘ra, Lizinning suyuqlanish temperaturasi qancha?",
      options: ["210 °C", "224 °C", "228 °C", "238 °C"],
      correctOptionId: 1, // 224 °C
      explanation: "Lizin (Liz.) ning suyuqlanish temperaturasi: 224 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_10",
      question: "Jadvalga ko‘ra, Serinning suyuqlanish temperaturasi qancha?",
      options: ["224 °C", "228 °C", "249 °C", "260 °C"],
      correctOptionId: 1, // 228 °C
      explanation: "Serin (Ser.) ning suyuqlanish temperaturasi: 228 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_11",
      question: "Jadvalga ko‘ra, Treoninning suyuqlanish temperaturasi qancha?",
      options: ["238 °C", "249 °C", "253 °C", "275 °C"],
      correctOptionId: 2, // 253 °C
      explanation: "Treonin (Tre.) ning suyuqlanish temperaturasi: 253 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_12",
      question: "Jadvalga ko‘ra, Sisteinning suyuqlanish temperaturasi qancha?",
      options: ["140 °C", "165 °C", "178 °C", "260 °C"],
      correctOptionId: 2, // 178 °C
      explanation: "Sistein (Sis.-n) ning suyuqlanish temperaturasi: 178 °C (Sistin bilan adashtirmang).",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_13",
      question: "Jadvalga ko‘ra, Sistinning suyuqlanish temperaturasi qancha?",
      options: ["178 °C", "253 °C", "260 °C", "270 °C"],
      correctOptionId: 2, // 260 °C
      explanation: "Sistin (Sis.) ning suyuqlanish temperaturasi: 260 °C (Sistein 178 °C).",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_14",
      question: "Jadvalga ko‘ra, Metioninning suyuqlanish temperaturasi qancha?",
      options: ["275 °C", "283 °C", "284 °C", "292 °C"],
      correctOptionId: 1, // 283 °C
      explanation: "Metionin (Met.) ning suyuqlanish temperaturasi: 283 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_15",
      question: "Jadvalga ko‘ra, Fenilalaninning suyuqlanish temperaturasi qancha?",
      options: ["270 °C", "275 °C", "277 °C", "297 °C"],
      correctOptionId: 1, // 275 °C
      explanation: "Fenilalanin (Fen.) ning suyuqlanish temperaturasi: 275 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_16",
      question: "Jadvalga ko‘ra, Tirozinning suyuqlanish temperaturasi qancha?",
      options: ["315 °C", "337 °C", "344 °C", "382 °C"],
      correctOptionId: 2, // 344 °C
      explanation: "Tirozin (Tir.) ning suyuqlanish temperaturasi: 344 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_17",
      question: "Jadvalga ko‘ra, Triptofanning suyuqlanish temperaturasi qancha?",
      options: ["337 °C", "344 °C", "370 °C", "382 °C"],
      correctOptionId: 3, // 382 °C
      explanation: "Triptofan (Tri.) ning suyuqlanish temperaturasi: 382 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_18",
      question: "Jadvalga ko‘ra, Prolinning suyuqlanish temperaturasi qancha?",
      options: ["270 °C", "284 °C", "297 °C", "299 °C"],
      correctOptionId: 3, // 299 °C
      explanation: "Prolin (Pro.) ning suyuqlanish temperaturasi: 299 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_19",
      question: "Jadvalga ko‘ra, Oksiprolinning suyuqlanish temperaturasi qancha?",
      options: ["260 °C", "270 °C", "277 °C", "299 °C"],
      correctOptionId: 1, // 270 °C
      explanation: "Oksiprolin (Pro-OH) ning suyuqlanish temperaturasi: 270 °C (Asparagin kislota bilan bir xil).",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_20",
      question: "Jadvalga ko‘ra, Gistidinning suyuqlanish temperaturasi qancha?",
      options: ["270 °C", "275 °C", "277 °C", "283 °C"],
      correctOptionId: 2, // 277 °C
      explanation: "Gistidin (Gis.) ning suyuqlanish temperaturasi: 277 °C.",
      timeLimitSeconds: 20,
    },
    {
      id: "aa_21",
      question: "Jadvalga ko‘ra, Argininning suyuqlanish temperaturasi qancha?",
      options: ["224 °C", "228 °C", "238 °C", "249 °C"],
      correctOptionId: 2, // 238 °C
      explanation: "Arginin (Arg.) ning suyuqlanish temperaturasi: 238 °C.",
      timeLimitSeconds: 20,
    },
  ],
};

// Orqaga moslik uchun sampleChemistryQuiz nomi ham saqlanadi
export const sampleChemistryQuiz = aminoAcidsQuiz;

/**
 * 2-quiz: Kimyo asoslari va elementlar bo'yicha namuna quiz
 */
export const chemistryBasicsQuiz: Quiz = {
  id: "kimyo_asoslari",
  title: "Kimyo asoslari — namuna",
  description: "Elementlar, suv formulasi va asosiy kimyoviy tushunchalar bo'yicha test",
  groupOnly: true,
  questions: [
    {
      id: "chem_1",
      question: "Suvning kimyoviy formulasi qaysi?",
      options: ["H2O", "H2O2", "HO", "CO2"],
      correctOptionId: 0,
      explanation: "Suv ikki vodorod va bir kislorod atomidan iborat: H2O.",
      timeLimitSeconds: 20,
    },
    {
      id: "chem_2",
      question: "Suv molekulasida kislorodning valentligi nechaga teng?",
      options: ["I", "II", "III", "IV"],
      correctOptionId: 1,
      explanation: "H2O birikmasida kislorod II valentli, vodorod esa I valentli bo'ladi.",
      timeLimitSeconds: 20,
    },
    {
      id: "chem_3",
      question: "Eng yengil gaz qaysi?",
      options: ["Geliy (He)", "Azot (N2)", "Vodorod (H2)", "Kislorod (O2)"],
      correctOptionId: 2,
      explanation: "Eng yengil gaz vodorod (H2) bo'lib, uning molyar massasi 2 g/mol ga teng.",
      timeLimitSeconds: 20,
    },
    {
      id: "chem_4",
      question: "Kimyoviy elementlar davriy qonunini kim kashf qilgan?",
      options: ["D.I. Mendeleyev", "A. Lavuazye", "J. Dalton", "E. Rezerford"],
      correctOptionId: 0,
      explanation: "Davriy qonun 1869-yilda D.I. Mendeleyev tomonidan kashf qilingan.",
      timeLimitSeconds: 20,
    },
    {
      id: "chem_5",
      question: "Xona haroratida sof neytral eritmaning pH qiymati nechaga teng?",
      options: ["0", "7", "14", "1"],
      correctOptionId: 1,
      explanation: "Neytral muhitda pH = 7, kislotali muhitda pH < 7, ishqoriy muhitda pH > 7 bo'ladi.",
      timeLimitSeconds: 20,
    },
  ],
};

import { kk1Quiz1, kk1Quiz2, kk1Quiz3 } from "./kk1Questions.js";
export { kk1Quiz1, kk1Quiz2, kk1Quiz3 };

// Barcha mavjud quizlar ro'yxati (o'zgarmas ID lar bilan)
export const allQuizzes: Quiz[] = [
  aminoAcidsQuiz,
  chemistryBasicsQuiz,
  kk1Quiz1,
  kk1Quiz2,
  kk1Quiz3,
];

/**
 * Mavjud barcha quizlarni olish
 */
export function getAllQuizzes(): Quiz[] {
  return allQuizzes;
}

/**
 * ID bo'yicha quizni qidirib topish
 */
export function getQuizById(id: string): Quiz | undefined {
  if (!id) return undefined;
  const normalized = id.trim().toLowerCase();

  // Aniq ID bo'yicha (masalan KK1_1, kk1_1, amino_acids)
  const directMatch = allQuizzes.find((q) => q.id.toLowerCase() === normalized);
  if (directMatch) return directMatch;

  // Qulay sinonim va moslashuvchan IDlar
  if (
    normalized === "amino_acids_temp" ||
    normalized === "jda-chem-amino-acids" ||
    normalized === "aminoacids" ||
    normalized === "1"
  ) {
    return aminoAcidsQuiz;
  }

  if (
    normalized === "kimyo_namuna" ||
    normalized === "chem_basics" ||
    normalized === "sample_chemistry" ||
    normalized === "2"
  ) {
    return chemistryBasicsQuiz;
  }

  if (
    normalized === "kk1-1" ||
    normalized === "kk_1_1" ||
    normalized === "kk11"
  ) {
    return kk1Quiz1;
  }

  if (
    normalized === "kk1-2" ||
    normalized === "kk_1_2" ||
    normalized === "kk12"
  ) {
    return kk1Quiz2;
  }

  if (
    normalized === "kk1-3" ||
    normalized === "kk_1_3" ||
    normalized === "kk13"
  ) {
    return kk1Quiz3;
  }

  return undefined;
}
