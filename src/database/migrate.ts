import dotenv from "dotenv";
import { initDatabase, closeDatabase, getDatabasePool } from "./db.js";

dotenv.config();

async function runMigration() {
  console.log("🚀 [Migrate] PostgreSQL ma'lumotlar bazasi migratsiyasi boshlandi...");

  if (!process.env.DATABASE_URL) {
    console.error("❌ [Migrate] DATABASE_URL muhit o'zgaruvchisi topilmadi!");
    console.log("ℹ️ [Migrate] Iltimos, .env faylida yoki Render Environment sozlamalarida DATABASE_URL ni belgilang.");
    process.exit(1);
  }

  const success = await initDatabase();
  if (success) {
    console.log("🎉 [Migrate] Barcha jadvallar (quiz_sessions, groups, quizzes, quiz_results, bot_users) muvaffaqiyatli tayyorlandi!");
    await closeDatabase();
    process.exit(0);
  } else {
    console.error("💥 [Migrate] Migratsiyani yakunlashda xatolik yuz berdi.");
    await closeDatabase();
    process.exit(1);
  }
}

runMigration().catch((err) => {
  console.error("💥 [Migrate] Kutilmagan xatolik:", err);
  process.exit(1);
});
