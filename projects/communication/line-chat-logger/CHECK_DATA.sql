-- データ確認用SQL
-- Neon SQLエディタで実行してください

-- 1. line_messagesテーブルのデータ確認
SELECT
    timestamp,
    user_name,
    content,
    source_type,
    group_name
FROM line_messages
ORDER BY timestamp DESC
LIMIT 10;

-- 2. project_analysisテーブルのデータ確認
SELECT
    timestamp,
    user_name,
    tasks,
    priority,
    has_action_items,
    bottleneck,
    risks
FROM project_analysis
ORDER BY timestamp DESC
LIMIT 10;

-- 3. テーブル存在確認
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- 4. カラム確認
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'line_messages'
ORDER BY ordinal_position;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'project_analysis'
ORDER BY ordinal_position;
