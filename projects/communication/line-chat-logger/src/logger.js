import fs from 'fs/promises';
import path from 'path';

const LOG_DIR = process.env.LOG_DIR || './logs';

// ログディレクトリ初期化
async function ensureLogDir() {
  try {
    await fs.access(LOG_DIR);
  } catch {
    await fs.mkdir(LOG_DIR, { recursive: true });
  }
}

// メッセージ保存
export async function saveMessage(messageData) {
  await ensureLogDir();

  const date = messageData.timestamp.toISOString().split('T')[0];
  const logFile = path.join(LOG_DIR, `chat_${date}.jsonl`);

  const logEntry = {
    ...messageData,
    timestamp: messageData.timestamp.toISOString(),
    savedAt: new Date().toISOString()
  };

  const logLine = JSON.stringify(logEntry) + '\n';

  await fs.appendFile(logFile, logLine, 'utf8');
}

// ログ取得（日付指定）
export async function getLogsByDate(date) {
  const logFile = path.join(LOG_DIR, `chat_${date}.jsonl`);

  try {
    const content = await fs.readFile(logFile, 'utf8');
    return content
      .trim()
      .split('\n')
      .filter(line => line)
      .map(line => JSON.parse(line));
  } catch (err) {
    if (err.code === 'ENOENT') {
      return [];
    }
    throw err;
  }
}

// ユーザー別ログ取得
export async function getLogsByUser(userId, date) {
  const logs = await getLogsByDate(date);
  return logs.filter(log => log.userId === userId);
}

// ログ統計
export async function getLogStats(date) {
  const logs = await getLogsByDate(date);

  const stats = {
    totalMessages: logs.length,
    users: new Set(logs.map(l => l.userId)).size,
    messageTypes: {},
    userMessageCounts: {}
  };

  logs.forEach(log => {
    // メッセージタイプ集計
    stats.messageTypes[log.messageType] = (stats.messageTypes[log.messageType] || 0) + 1;

    // ユーザー別メッセージ数
    stats.userMessageCounts[log.userName] = (stats.userMessageCounts[log.userName] || 0) + 1;
  });

  return stats;
}
