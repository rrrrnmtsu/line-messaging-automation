-- データベースマイグレーションSQL
-- Neon SQLエディタで実行してください

-- 1. line_messagesテーブルに新しいカラムを追加
ALTER TABLE line_messages ADD COLUMN IF NOT EXISTS source_type VARCHAR(20);
ALTER TABLE line_messages ADD COLUMN IF NOT EXISTS group_id VARCHAR(100);
ALTER TABLE line_messages ADD COLUMN IF NOT EXISTS group_name VARCHAR(200);
ALTER TABLE line_messages ADD COLUMN IF NOT EXISTS room_id VARCHAR(100);

-- 2. 既存データのsource_typeをデフォルト値で更新
UPDATE line_messages SET source_type = 'user' WHERE source_type IS NULL;

-- 3. source_typeをNOT NULLに変更
ALTER TABLE line_messages ALTER COLUMN source_type SET NOT NULL;

-- 4. インデックス追加
CREATE INDEX IF NOT EXISTS idx_source_type ON line_messages(source_type);
CREATE INDEX IF NOT EXISTS idx_group_id ON line_messages(group_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON line_messages(timestamp);

-- 5. project_analysisテーブル作成
CREATE TABLE IF NOT EXISTS project_analysis (
  id SERIAL PRIMARY KEY,
  message_id VARCHAR(100) UNIQUE NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  user_id VARCHAR(100),
  user_name VARCHAR(100),
  group_id VARCHAR(100),
  group_name VARCHAR(200),
  tasks JSONB,
  progress VARCHAR(50),
  bottleneck JSONB,
  risks JSONB,
  priority VARCHAR(20),
  has_action_items BOOLEAN DEFAULT FALSE,
  analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. project_analysisインデックス追加
CREATE INDEX IF NOT EXISTS idx_has_action_items ON project_analysis(has_action_items);
CREATE INDEX IF NOT EXISTS idx_priority ON project_analysis(priority);
CREATE INDEX IF NOT EXISTS idx_analysis_group ON project_analysis(group_id);
CREATE INDEX IF NOT EXISTS idx_analysis_timestamp ON project_analysis(timestamp);

-- 完了確認
SELECT 'Migration completed successfully!' as status;
