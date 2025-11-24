-- データ確認クエリ

-- 1. テーブル一覧
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- 2. line_messagesのレコード数
SELECT COUNT(*) as message_count FROM line_messages;

-- 3. 最新メッセージ（もしあれば）
SELECT * FROM line_messages ORDER BY timestamp DESC LIMIT 5;

-- 4. project_analysisのレコード数
SELECT COUNT(*) as analysis_count FROM project_analysis;

-- 5. 最新分析（もしあれば）
SELECT * FROM project_analysis ORDER BY timestamp DESC LIMIT 5;
