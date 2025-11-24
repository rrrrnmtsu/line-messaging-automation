-- パフォーマンス改善のためのインデックス追加
-- Neon SQLエディタで実行してください

-- line_messagesテーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_line_messages_user_id ON line_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_line_messages_timestamp ON line_messages(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_line_messages_group_id ON line_messages(group_id);
CREATE INDEX IF NOT EXISTS idx_line_messages_source_type ON line_messages(source_type);
CREATE INDEX IF NOT EXISTS idx_line_messages_message_type ON line_messages(message_type);

-- project_analysisテーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_project_analysis_timestamp ON project_analysis(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_project_analysis_group_id ON project_analysis(group_id);
CREATE INDEX IF NOT EXISTS idx_project_analysis_priority ON project_analysis(priority);
CREATE INDEX IF NOT EXISTS idx_project_analysis_has_action_items ON project_analysis(has_action_items);
CREATE INDEX IF NOT EXISTS idx_project_analysis_analyzed_at ON project_analysis(analyzed_at DESC);

-- 複合インデックス（よく使われる検索条件）
CREATE INDEX IF NOT EXISTS idx_line_messages_group_timestamp
  ON line_messages(group_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_project_analysis_group_timestamp
  ON project_analysis(group_id, timestamp DESC);

-- インデックス確認
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
