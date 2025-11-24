import { sql } from './lib/db.js';

export default async function handler(req, res) {
  try {
    const { room } = req.query;

    let query;
    let params = [];

    if (room && room !== 'all') {
      // 特定ルームのログ取得
      query = `
        SELECT timestamp, user_name, content, message_type, room_name
        FROM lineworks_messages
        WHERE room_id = $1 OR room_name = $1
        ORDER BY timestamp ASC
      `;
      params = [room];
    } else {
      // 全てのログ取得
      query = `
        SELECT timestamp, user_name, content, message_type, source_type, room_name
        FROM lineworks_messages
        ORDER BY timestamp ASC
      `;
    }

    const result = await sql.query(query, params);
    const messages = result.rows;

    // テキスト形式に変換
    let textContent = '';

    if (room && room !== 'all') {
      const roomName = messages[0]?.room_name || room;
      textContent += `===========================================\n`;
      textContent += `LINE WORKS Chat Log - ${roomName}\n`;
      textContent += `Generated: ${new Date().toLocaleString('ja-JP')}\n`;
      textContent += `Total Messages: ${messages.length}\n`;
      textContent += `===========================================\n\n`;
    } else {
      textContent += `===========================================\n`;
      textContent += `LINE WORKS Chat Log - All Messages\n`;
      textContent += `Generated: ${new Date().toLocaleString('ja-JP')}\n`;
      textContent += `Total Messages: ${messages.length}\n`;
      textContent += `===========================================\n\n`;
    }

    // ルームごとに整理
    const groupedMessages = {};
    messages.forEach(msg => {
      const roomKey = msg.room_name || 'Direct Messages';
      if (!groupedMessages[roomKey]) {
        groupedMessages[roomKey] = [];
      }
      groupedMessages[roomKey].push(msg);
    });

    // ルームごとに出力
    for (const [roomName, msgs] of Object.entries(groupedMessages)) {
      if (room === 'all') {
        textContent += `\n--- ${roomName} (${msgs.length} messages) ---\n\n`;
      }

      msgs.forEach(msg => {
        const timestamp = new Date(msg.timestamp).toLocaleString('ja-JP');
        const userName = msg.user_name || 'Unknown';
        const content = msg.content || `[${msg.message_type}]`;

        textContent += `[${timestamp}] ${userName}\n${content}\n\n`;
      });
    }

    // ファイル名生成
    const filename = room && room !== 'all'
      ? `lineworks_log_${room}_${Date.now()}.txt`
      : `lineworks_log_all_${Date.now()}.txt`;

    // レスポンスヘッダー設定
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);

    res.status(200).send(textContent);

  } catch (error) {
    console.error('ログダウンロードエラー:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
