-- JDA Kimyo Quiz Database Schema
-- Moslik: PostgreSQL 14+, Render Postgres, Supabase, Neon, Vercel Postgres

-- 1. Faol va pauzadagi quiz sessiyalari jadvali (Render restartidan keyin saqlash uchun)
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

-- 2. Telegram Guruhlari jadvali (Admin panel va statistika uchun)
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

-- 3. Nashr qilingan va dinamik testlar jadvali (Admin panel tahrirlashi uchun)
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

-- 4. Quiz natijalari va ishtirokchilar reytingi tarixi jadvali
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT uq_quiz_results_session_user UNIQUE (session_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_quiz_results_quiz_id ON quiz_results(quiz_id);
CREATE INDEX IF NOT EXISTS idx_quiz_results_chat_id ON quiz_results(chat_id);
CREATE INDEX IF NOT EXISTS idx_quiz_results_user_id ON quiz_results(user_id);

-- 5. Foydalanuvchilar va bloklash holati jadvali (Admin panel uchun)
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
