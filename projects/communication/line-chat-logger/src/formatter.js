// メッセージフォーマッター

export function formatMessage(messageData) {
  const timestamp = new Date(messageData.timestamp).toLocaleString('ja-JP');
  const type = messageData.messageType.toUpperCase();

  return `[${timestamp}] ${messageData.userName} (${type}): ${messageData.content}`;
}

export function formatLogStats(stats) {
  const lines = [];

  lines.push('=== チャットログ統計 ===');
  lines.push(`総メッセージ数: ${stats.totalMessages}`);
  lines.push(`ユーザー数: ${stats.users}`);

  lines.push('\n--- メッセージタイプ ---');
  Object.entries(stats.messageTypes).forEach(([type, count]) => {
    lines.push(`${type}: ${count}`);
  });

  lines.push('\n--- ユーザー別メッセージ数 ---');
  Object.entries(stats.userMessageCounts)
    .sort((a, b) => b[1] - a[1])
    .forEach(([user, count]) => {
      lines.push(`${user}: ${count}`);
    });

  return lines.join('\n');
}

export function formatLogsToMarkdown(logs, title = 'チャットログ') {
  const lines = [`# ${title}\n`];

  logs.forEach(log => {
    const timestamp = new Date(log.timestamp).toLocaleString('ja-JP');
    lines.push(`**[${timestamp}]** ${log.userName}`);
    lines.push(`> ${log.content}\n`);
  });

  return lines.join('\n');
}
