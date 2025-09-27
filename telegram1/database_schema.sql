-- Supabase 数据库表结构
-- 在 Supabase SQL 编辑器中执行以下 SQL 语句

-- 创建用户表（简化版，只保存用户ID）
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 创建分数表（可选）
CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    game_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);
CREATE INDEX IF NOT EXISTS idx_scores_user_id ON scores(user_id);
CREATE INDEX IF NOT EXISTS idx_scores_created_at ON scores(created_at);

-- 设置 RLS (Row Level Security) 策略
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;

-- 允许匿名用户插入和查询数据
CREATE POLICY "Allow anonymous insert" ON users FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow anonymous select" ON users FOR SELECT TO anon USING (true);
CREATE POLICY "Allow anonymous update" ON users FOR UPDATE TO anon USING (true);

CREATE POLICY "Allow anonymous insert scores" ON scores FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow anonymous select scores" ON scores FOR SELECT TO anon USING (true);
