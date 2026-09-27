import pg from "pg";
const { Pool } = pg;

let pool: pg.Pool | null = null;
let isInitialized = false;

export function getDatabasePool(): pg.Pool | null {
  const databaseUrl = process.env.DATABASE_URL;
  if (!databaseUrl) {
    return null;
  }

  if (!pool) {
    const isProduction = process.env.NODE_ENV === "production";
    pool = new Pool({
      connectionString: databaseUrl,
      ssl: isProduction ? { rejectUnauthorized: false } : undefined,
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    });

    pool.on("error", (err) => {
      console.error("[Database] Kutilmagan PostgreSQL pool xatoligi:", err);
    });
  }

  return pool;
}

export async function initDatabase(): Promise<boolean> {
  const dbPool = getDatabasePool();
  if (!dbPool) {
    return false;
  }

  if (isInitialized) {
    return true;
  }

  const client = await dbPool.connect();
  try {
    console.log("[Database] PostgreSQL ma'lumotlar bazasiga ulanish tekshirilmoqda...");

    // 1. quiz_sessions jadvali
    await client.query(`
      CREATE TABLE IF NOT EXISTS quiz_sessions (
          session_id VARCHAR(100) PRIMARY KEY,
          chat_id BIGINT NOT NULL UNIQUE,
          quiz_id VARCHAR(100) NOT NULL,
          quiz_data JSONB NOT NULL,
          status VARCHAR(50) NOT NULL,
          current_question_index INTEGER NOT NULL DEFAULT -1,
          consecutive_unanswered_count INTEGER NOT NULL DEFAULT 0,
          participants JSONB NOT NULL DEFAULT '[]'::jsonb,
          answered_users JSONB NOT NULL DEFAULT '[]'::jsonb,
          saved_at BIGINT NOT NULL,
          version INTEGER NOT NULL DEFAULT 1,
          final_message_sent BOOLEAN DEFAULT FALSE,
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_quiz_sessions_chat_id ON quiz_sessions(chat_id);
      CREATE INDEX IF NOT EXISTS idx_quiz_sessions_status ON quiz_sessions(status);
      ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1;
      ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS final_message_sent BOOLEAN DEFAULT FALSE;
    `);

    // 2. groups jadvali
    await client.query(`
      CREATE TABLE IF NOT EXISTS groups (
          id SERIAL PRIMARY KEY,
          telegram_chat_id BIGINT UNIQUE NOT NULL,
          title VARCHAR(255),
          is_active BOOLEAN DEFAULT TRUE,
          quiz_count INTEGER DEFAULT 0,
          last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_groups_telegram_chat_id ON groups(telegram_chat_id);
    `);

    // 3. quizzes jadvali
    await client.query(`
      CREATE TABLE IF NOT EXISTS quizzes (
          id VARCHAR(100) PRIMARY KEY,
          title VARCHAR(255) NOT NULL,
          description TEXT,
          source VARCHAR(255),
          creator VARCHAR(255) DEFAULT '@diyorbek_jabborov',
          status VARCHAR(50) DEFAULT 'published',
          questions JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
    `);

    // 4. quiz_results jadvali
    await client.query(`
      CREATE TABLE IF NOT EXISTS quiz_results (
          id SERIAL PRIMARY KEY,
          session_id VARCHAR(100) NOT NULL,
          quiz_id VARCHAR(100) NOT NULL,
          chat_id BIGINT NOT NULL,
          user_id BIGINT NOT NULL,
          first_name VARCHAR(255),
          username VARCHAR(255),
          score INTEGER NOT NULL,
          total_questions INTEGER NOT NULL,
          total_time_ms BIGINT NOT NULL,
          answers_count INTEGER NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_quiz_results_quiz_id ON quiz_results(quiz_id);
      CREATE INDEX IF NOT EXISTS idx_quiz_results_chat_id ON quiz_results(chat_id);
      CREATE UNIQUE INDEX IF NOT EXISTS idx_quiz_results_session_user ON quiz_results(session_id, user_id);
    `);

    // 5. bot_users jadvali
    await client.query(`
      CREATE TABLE IF NOT EXISTS bot_users (
          id SERIAL PRIMARY KEY,
          telegram_user_id BIGINT UNIQUE NOT NULL,
          first_name VARCHAR(255),
          username VARCHAR(255),
          is_blocked BOOLEAN DEFAULT FALSE,
          blocked_reason TEXT,
          last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_bot_users_telegram_user_id ON bot_users(telegram_user_id);
    `);

    isInitialized = true;
    console.log("✅ [Database] PostgreSQL jadvallari va migratsiyalari muvaffaqiyatli tekshirildi/yaratildi.");
    return true;
  } catch (error) {
    console.error("❌ [Database] PostgreSQL migratsiyasini bajarishda xatolik:", error);
    return false;
  } finally {
    client.release();
  }
}

export async function checkDatabaseHealth(): Promise<boolean> {
  const dbPool = getDatabasePool();
  if (!dbPool) return false;
  try {
    const client = await dbPool.connect();
    try {
      await client.query("SELECT 1");
      return true;
    } finally {
      client.release();
    }
  } catch {
    return false;
  }
}

export async function closeDatabase(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
    isInitialized = false;
  }
}

export function resetDatabaseState(): void {
  if (pool) {
    try {
      pool.end();
    } catch {
      // ignore
    }
    pool = null;
  }
  isInitialized = false;
}
