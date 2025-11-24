-- 保存されたメッセージを確認

-- 最新のメッセージ内容
SELECT
    timestamp,
    user_name,
    content,
    message_type,
    source_type,
    group_name
FROM line_messages
ORDER BY timestamp DESC
LIMIT 10;

-- プロジェクト分析結果
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
