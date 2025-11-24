import { neon } from '@neondatabase/serverless';

// 環境変数から接続文字列を取得
const connectionString = process.env.DATABASE_URL || process.env.POSTGRES_URL;

if (!connectionString) {
  console.error('DATABASE_URL or POSTGRES_URL not found');
  console.error('Available env vars:', Object.keys(process.env).filter(k => k.includes('DATA') || k.includes('POSTGRES')));
  throw new Error('Database connection string not configured');
}

console.log('Using connection string:', connectionString.substring(0, 60) + '...');
const sql = neon(connectionString);

/**
 * データベース初期化
 */
export async function initDB() {
  try {
    // lineworks_messagesテーブル作成
    const result = await sql`
      CREATE TABLE IF NOT EXISTS lineworks_messages (
        id SERIAL PRIMARY KEY,
        message_id VARCHAR(100) UNIQUE NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        user_id VARCHAR(100),
        user_name VARCHAR(100),
        message_type VARCHAR(20),
        content TEXT,
        source_type VARCHAR(20),
        room_id VARCHAR(100),
        room_name VARCHAR(200),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `;

    // インデックス作成
    await sql`CREATE INDEX IF NOT EXISTS idx_lineworks_timestamp ON lineworks_messages(timestamp DESC)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_lineworks_room_id ON lineworks_messages(room_id)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_lineworks_user_id ON lineworks_messages(user_id)`;

    console.log('Database initialized successfully');
    return { success: true };
  } catch (error) {
    console.error('Database initialization error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * メッセージを保存
 */
export async function saveMessage(messageData) {
  try {
    await sql`
      INSERT INTO lineworks_messages (
        message_id,
        timestamp,
        user_id,
        user_name,
        message_type,
        content,
        source_type,
        room_id,
        room_name
      ) VALUES (
        ${messageData.messageId},
        ${messageData.timestamp},
        ${messageData.userId},
        ${messageData.userName},
        ${messageData.messageType},
        ${messageData.content},
        ${messageData.sourceType},
        ${messageData.roomId},
        ${messageData.roomName}
      )
      ON CONFLICT (message_id) DO NOTHING
    `;

    return { success: true };
  } catch (error) {
    console.error('メッセージ保存エラー:', error);
    return { success: false, error: error.message };
  }
}

export { sql };
