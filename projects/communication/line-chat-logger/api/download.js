import { sql } from '@vercel/postgres';

export default async function handler(req, res) {
  try {
    const { group } = req.query;

    let query;
    let params = [];

    if (group && group !== 'all') {
      // 特定グループのログ取得
      query = `
        SELECT timestamp, user_name, content, message_type, group_name
        FROM line_messages
        WHERE group_id = $1 OR group_name = $1
        ORDER BY timestamp ASC
      `;
      params = [group];
    } else {
      // 全てのログ取得
      query = `
        SELECT timestamp, user_name, content, message_type, source_type, group_name
        FROM line_messages
        ORDER BY timestamp ASC
      `;
    }

    const result = await sql.query(query, params);
    const messages = result.rows;

    // テキスト形式に変換
    let textContent = '';

    if (group && group !== 'all') {
      const groupName = messages[0]?.group_name || group;
      textContent += `===========================================\n`;
      textContent += `LINE Chat Log - ${groupName}\n`;
      textContent += `Generated: ${new Date().toLocaleString('ja-JP')}\n`;
      textContent += `Total Messages: ${messages.length}\n`;
      textContent += `===========================================\n\n`;
    } else {
      textContent += `===========================================\n`;
      textContent += `LINE Chat Log - All Messages\n`;
      textContent += `Generated: ${new Date().toLocaleString('ja-JP')}\n`;
      textContent += `Total Messages: ${messages.length}\n`;
      textContent += `===========================================\n\n`;
    }

    // グループごとに整理
    const groupedMessages = {};
    messages.forEach(msg => {
      const groupKey = msg.group_name || 'Direct Messages';
      if (!groupedMessages[groupKey]) {
        groupedMessages[groupKey] = [];
      }
      groupedMessages[groupKey].push(msg);
    });

    // グループごとに出力
    for (const [groupName, msgs] of Object.entries(groupedMessages)) {
      if (group === 'all') {
        textContent += `\n--- ${groupName} (${msgs.length} messages) ---\n\n`;
      }

      msgs.forEach(msg => {
        const timestamp = new Date(msg.timestamp).toLocaleString('ja-JP');
        const userName = msg.user_name || 'Unknown';
        const content = msg.content || `[${msg.message_type}]`;

        textContent += `[${timestamp}] ${userName}\n${content}\n\n`;
      });
    }

    // ファイル名生成
    const filename = group && group !== 'all'
      ? `line_log_${group}_${Date.now()}.txt`
      : `line_log_all_${Date.now()}.txt`;

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
