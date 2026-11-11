import "dotenv/config";
import fs from "node:fs";
import path from "node:path";
import { initFirestore, getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";
import { validateKursDarslarPayload, RawKursDars } from "./kursRepository.js";

export interface KursBankFile {
  kurs?: string;
  yangilangan?: string;
  darslar: unknown[];
}

export async function uploadKursBankToFirestore(bank: KursBankFile): Promise<{
  uploadedLessons: number;
  totalQuestions: number;
  totalExercises: number;
  validated: RawKursDars[];
}> {
  if (!bank || typeof bank !== "object" || !Array.isArray(bank.darslar)) {
    throw new Error("Noto'g'ri JSON format: 'darslar' massivi topilmadi.");
  }

  const validation = validateKursDarslarPayload(bank.darslar);
  if (!validation.valid) {
    throw new Error(`Test banki validatsiyadan o'tmadi:\n- ${validation.errors.join("\n- ")}`);
  }

  const db = getFirestoreDb();
  if (!db) {
    throw new Error("Firestore bazasiga ulanib bo'lmadi. FIREBASE_SERVICE_ACCOUNT sozlamalarini tekshiring.");
  }

  const nowIso = new Date().toISOString();
  let totalQuestions = 0;
  let totalExercises = 0;

  for (const dars of validation.validated) {
    const docId = String(dars.dars);
    totalQuestions += dars.testlar.length;
    totalExercises += dars.mashqlar?.length || 0;

    await db
      .collection(FIRESTORE_COLLECTIONS.KURS_LESSONS)
      .doc(docId)
      .set(
        {
          dars: dars.dars,
          mavzu: dars.mavzu,
          papka: dars.papka || null,
          testlar: dars.testlar,
          mashqlar: dars.mashqlar || [],
          updatedAt: nowIso,
        },
        { merge: true }
      );
  }

  return {
    uploadedLessons: validation.validated.length,
    totalQuestions,
    totalExercises,
    validated: validation.validated,
  };
}

async function runCli(): Promise<void> {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const fileArg = args.find((a) => !a.startsWith("--"));
  const argPath =
    fileArg ||
    process.env.KURS_TEST_BANK_PATH ||
    "D:\\Projects\\JDA_Kimyo_Kurs\\test_bank.json";
  const resolvedPath = path.resolve(argPath);

  if (!fs.existsSync(resolvedPath)) {
    console.error(`❌ Fayl topilmadi: ${resolvedPath}`);
    process.exit(1);
  }

  const rawText = fs.readFileSync(resolvedPath, "utf8");
  const parsed = JSON.parse(rawText) as KursBankFile;

  if (dryRun) {
    const validation = validateKursDarslarPayload(parsed.darslar);
    if (!validation.valid) {
      throw new Error(`Test banki validatsiyadan o'tmadi:\n- ${validation.errors.join("\n- ")}`);
    }
    const totalQuestions = validation.validated.reduce((sum, d) => sum + d.testlar.length, 0);
    const totalExercises = validation.validated.reduce((sum, d) => sum + (d.mashqlar?.length || 0), 0);
    console.log(
      `✅ [DRY-RUN] Kurs test banki tekshiruvdan o'tdi: ${validation.validated.length} ta dars, ${totalQuestions} ta test, ${totalExercises} ta mashq.`
    );
    return;
  }

  initFirestore();
  const result = await uploadKursBankToFirestore(parsed);
  console.log(
    `✅ Kurs darslari Firestore (${FIRESTORE_COLLECTIONS.KURS_LESSONS}) ga muvaffaqiyatli yuklandi: ` +
      `${result.uploadedLessons} ta dars, ${result.totalQuestions} ta test, ${result.totalExercises} ta mashq.`
  );
}

if (process.argv[1] && /yuklaScript\.(ts|js)$/i.test(process.argv[1])) {
  runCli().catch((err) => {
    console.error("❌ Yuklashda xatolik:", err instanceof Error ? err.message : err);
    process.exit(1);
  });
}
