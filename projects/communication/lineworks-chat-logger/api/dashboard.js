import { sql } from './lib/db.js';

export default async function handler(req, res) {
  try {
    const { days = 7 } = req.query;

    // 基本統計
    const statsResult = await sql`
      SELECT
        COUNT(*) as total_messages,
        COUNT(DISTINCT user_id) as unique_users,
        COUNT(DISTINCT room_id) as total_rooms,
        COUNT(CASE WHEN source_type = 'room' THEN 1 END) as room_messages,
        COUNT(CASE WHEN source_type = 'user' THEN 1 END) as direct_messages
      FROM lineworks_messages
      WHERE timestamp >= NOW() - make_interval(days := ${parseInt(days)})
    `;

    // ルーム別メッセージ数
    const roomsResult = await sql`
      SELECT
        COALESCE(room_name, 'Direct Messages') as room_name,
        room_id,
        COUNT(*) as message_count,
        MAX(timestamp) as last_message_at
      FROM lineworks_messages
      WHERE timestamp >= NOW() - make_interval(days := ${parseInt(days)})
      GROUP BY room_id, room_name
      ORDER BY message_count DESC
    `;

    res.status(200).json({
      success: true,
      stats: statsResult[0],
      rooms: roomsResult,
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
