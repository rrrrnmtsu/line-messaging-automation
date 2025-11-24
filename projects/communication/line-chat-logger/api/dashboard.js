import { sql } from '@vercel/postgres';

export default async function handler(req, res) {
  try {
    const { days = 7 } = req.query;

    // 基本統計
    const statsResult = await sql`
      SELECT
        COUNT(*) as total_messages,
        COUNT(DISTINCT user_id) as unique_users,
        COUNT(DISTINCT group_id) as total_groups,
        COUNT(CASE WHEN source_type = 'group' THEN 1 END) as group_messages,
        COUNT(CASE WHEN source_type = 'user' THEN 1 END) as direct_messages
      FROM line_messages
      WHERE timestamp >= NOW() - make_interval(days := ${parseInt(days)})
    `;

    // グループ別メッセージ数
    const groupsResult = await sql`
      SELECT
        COALESCE(group_name, 'Direct Messages') as group_name,
        group_id,
        COUNT(*) as message_count,
        MAX(timestamp) as last_message_at
      FROM line_messages
      WHERE timestamp >= NOW() - make_interval(days := ${parseInt(days)})
      GROUP BY group_id, group_name
      ORDER BY message_count DESC
    `;

    res.status(200).json({
      success: true,
      stats: statsResult.rows[0],
      groups: groupsResult.rows,
      period_days: parseInt(days)
    });

  } catch (error) {
    console.error('ダッシュボードエラー:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
