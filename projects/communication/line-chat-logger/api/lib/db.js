import { sql } from '@vercel/postgres';

// テーブル作成
export async function initDB() {
  try {
    await sql`
      CREATE TABLE IF NOT EXISTS line_messages (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        user_id VARCHAR(100) NOT NULL,
        user_name VARCHAR(100),
        message_id VARCHAR(100) UNIQUE NOT NULL,
        message_type VARCHAR(50),
        content TEXT,
        source_type VARCHAR(20) NOT NULL,
        group_id VARCHAR(100),
        group_name VARCHAR(200),
        room_id VARCHAR(100),
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `;

    // インデックス追加
    await sql`CREATE INDEX IF NOT EXISTS idx_source_type ON line_messages(source_type)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_group_id ON line_messages(group_id)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_timestamp ON line_messages(timestamp)`;

    // プロジェクト管理用テーブル
    await sql`
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
      )
    `;

    await sql`CREATE INDEX IF NOT EXISTS idx_has_action_items ON project_analysis(has_action_items)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_priority ON project_analysis(priority)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_analysis_group ON project_analysis(group_id)`;

    return { success: true };
  } catch (error) {
    console.error('DB初期化エラー:', error);
    return { success: false, error: error.message };
  }
}

// メッセージ保存
export async function saveMessage(messageData) {
  try {
    await sql`
      INSERT INTO line_messages (
        timestamp, user_id, user_name, message_id, message_type, content,
        source_type, group_id, group_name, room_id
      ) VALUES (
        ${messageData.timestamp},
        ${messageData.userId},
        ${messageData.userName},
        ${messageData.messageId},
        ${messageData.messageType},
        ${messageData.content},
        ${messageData.sourceType},
        ${messageData.groupId || null},
        ${messageData.groupName || null},
        ${messageData.roomId || null}
      )
      ON CONFLICT (message_id) DO NOTHING
    `;
    return { success: true };
  } catch (error) {
    console.error('メッセージ保存エラー:', error);
    return { success: false, error: error.message };
  }
}

// メッセージ取得（日付指定）
export async function getMessagesByDate(date) {
  try {
    const result = await sql`
      SELECT * FROM line_messages
      WHERE DATE(timestamp) = ${date}
      ORDER BY timestamp ASC
    `;
    return { success: true, data: result.rows };
  } catch (error) {
    console.error('メッセージ取得エラー:', error);
    return { success: false, error: error.message };
  }
}

// 統計取得
export async function getStats(date) {
  try {
    const result = await sql`
      SELECT
        COUNT(*) as total_messages,
        COUNT(DISTINCT user_id) as total_users,
        message_type,
        COUNT(*) as type_count
      FROM line_messages
      WHERE DATE(timestamp) = ${date}
      GROUP BY message_type
    `;
    return { success: true, data: result.rows };
  } catch (error) {
    console.error('統計取得エラー:', error);
    return { success: false, error: error.message };
  }
}

// グループ別メッセージ取得
export async function getMessagesByGroup(groupId, date = null) {
  try {
    const query = date
      ? sql`
          SELECT * FROM line_messages
          WHERE group_id = ${groupId} AND DATE(timestamp) = ${date}
          ORDER BY timestamp ASC
        `
      : sql`
          SELECT * FROM line_messages
          WHERE group_id = ${groupId}
          ORDER BY timestamp DESC
          LIMIT 100
        `;

    const result = await query;
    return { success: true, data: result.rows };
  } catch (error) {
    console.error('グループ別取得エラー:', error);
    return { success: false, error: error.message };
  }
}

// ソースタイプ別メッセージ取得
export async function getMessagesBySourceType(sourceType, date = null) {
  try {
    const query = date
      ? sql`
          SELECT * FROM line_messages
          WHERE source_type = ${sourceType} AND DATE(timestamp) = ${date}
          ORDER BY timestamp ASC
        `
      : sql`
          SELECT * FROM line_messages
          WHERE source_type = ${sourceType}
          ORDER BY timestamp DESC
          LIMIT 100
        `;

    const result = await query;
    return { success: true, data: result.rows };
  } catch (error) {
    console.error('ソースタイプ別取得エラー:', error);
    return { success: false, error: error.message };
  }
}

// グループ一覧取得
export async function getGroupList() {
  try {
    const result = await sql`
      SELECT DISTINCT
        group_id,
        group_name,
        COUNT(*) as message_count,
        MAX(timestamp) as last_message_at
      FROM line_messages
      WHERE source_type = 'group' AND group_id IS NOT NULL
      GROUP BY group_id, group_name
      ORDER BY last_message_at DESC
    `;
    return { success: true, data: result.rows };
  } catch (error) {
    console.error('グループ一覧取得エラー:', error);
    return { success: false, error: error.message };
  }
}

// プロジェクト分析結果保存
export async function saveProjectAnalysis(analysis) {
  try {
    await sql`
      INSERT INTO project_analysis (
        message_id, timestamp, user_id, user_name, group_id, group_name,
        tasks, progress, bottleneck, risks, priority, has_action_items
      ) VALUES (
        ${analysis.messageId},
        ${analysis.timestamp},
        ${analysis.userId},
        ${analysis.userName},
        ${analysis.groupId || null},
        ${analysis.groupName || null},
        ${JSON.stringify(analysis.tasks)},
        ${analysis.progress?.status || null},
        ${JSON.stringify(analysis.bottleneck)},
        ${JSON.stringify(analysis.risks)},
        ${analysis.priority},
        ${analysis.hasActionItems}
      )
      ON CONFLICT (message_id) DO NOTHING
    `;
    return { success: true };
  } catch (error) {
    console.error('分析結果保存エラー:', error);
    return { success: false, error: error.message };
  }
}

// アクションアイテム取得
export async function getActionItems(groupId = null) {
  try {
    const query = groupId
      ? sql`
          SELECT * FROM project_analysis
          WHERE has_action_items = TRUE AND group_id = ${groupId}
          ORDER BY priority DESC, timestamp DESC
          LIMIT 50
        `
      : sql`
          SELECT * FROM project_analysis
          WHERE has_action_items = TRUE
          ORDER BY priority DESC, timestamp DESC
          LIMIT 50
        `;

    const result = await query;
    return { success: true, data: result.rows };
  } catch (error) {
    console.error('アクションアイテム取得エラー:', error);
    return { success: false, error: error.message };
  }
}

// プロジェクトダッシュボード取得
export async function getProjectDashboard(groupId = null, days = 7) {
  try {
    let result;

    if (groupId) {
      result = await sql`
        SELECT
          COUNT(*) as total_messages,
          COUNT(CASE WHEN has_action_items THEN 1 END) as action_items_count,
          COUNT(CASE WHEN priority = 'critical' THEN 1 END) as critical_count,
          COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_priority_count,
          COUNT(CASE WHEN bottleneck->>'detected' = 'true' THEN 1 END) as bottleneck_count
        FROM project_analysis
        WHERE timestamp >= NOW() - make_interval(days := ${days})
          AND group_id = ${groupId}
      `;
    } else {
      result = await sql`
        SELECT
          COUNT(*) as total_messages,
          COUNT(CASE WHEN has_action_items THEN 1 END) as action_items_count,
          COUNT(CASE WHEN priority = 'critical' THEN 1 END) as critical_count,
          COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_priority_count,
          COUNT(CASE WHEN bottleneck->>'detected' = 'true' THEN 1 END) as bottleneck_count
        FROM project_analysis
        WHERE timestamp >= NOW() - make_interval(days := ${days})
      `;
    }

    return { success: true, data: result.rows[0] };
  } catch (error) {
    console.error('ダッシュボード取得エラー:', error);
    return { success: false, error: error.message };
  }
}
