import { saveMessage, initDB } from './lib/db.js';
import { getCachedAccessToken } from './lib/auth.js';

// DB初期化（初回実行時）
let dbInitialized = false;

export default async function handler(req, res) {
  console.log('Webhook received:', req.method);

  // DB初期化
  if (!dbInitialized) {
    await initDB();
    dbInitialized = true;
  }

  // POSTリクエストのみ処理
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const body = req.body;
    console.log('Webhook body:', JSON.stringify(body, null, 2));

    // LINE WORKSイベント処理
    if (body.type === 'message') {
      const result = await handleMessage(body);
      return res.status(200).json({ success: true, result });
    }

    // その他のイベント
    return res.status(200).json({ success: true, type: body.type });

  } catch (err) {
    console.error('Webhook処理エラー:', err);
    res.status(500).json({ success: false, error: err.message });
  }
}

async function handleMessage(event) {
  try {
    const { content, source, createdTime } = event;

    // ユーザー情報取得
    let userName = 'Unknown User';
    let userId = source.userId;

    if (userId) {
      try {
        const accessToken = await getCachedAccessToken();
        const userInfo = await getUserInfo(accessToken, userId);
        userName = userInfo.userName || userInfo.name || 'Unknown User';
      } catch (err) {
        console.warn('ユーザー情報取得失敗:', err.message);
      }
    }

    // ルーム情報
    let roomId = source.roomId || null;
    let roomName = null;
    let sourceType = roomId ? 'room' : 'user';

    if (roomId) {
      try {
        const accessToken = await getCachedAccessToken();
        const roomInfo = await getRoomInfo(accessToken, roomId);
        roomName = roomInfo.name || `Room_${roomId}`;
      } catch (err) {
        console.warn('ルーム情報取得失敗:', err.message);
        roomName = `Room_${roomId}`;
      }
    }

    // メッセージデータ
    const messageData = {
      messageId: content.id || `msg_${Date.now()}`,
      timestamp: new Date(createdTime).toISOString(),
      userId: userId,
      userName: userName,
      messageType: content.type,
      content: content.text || content.type,
      sourceType: sourceType,
      roomId: roomId,
      roomName: roomName
    };

    // データベースに保存
    const saveResult = await saveMessage(messageData);

    if (saveResult.success) {
      console.log('MESSAGE SAVED:', {
        messageId: messageData.messageId,
        userName: messageData.userName,
        roomName: messageData.roomName || 'DM',
        contentLength: messageData.content?.length || 0
      });
    }

    return { status: 'success', messageId: messageData.messageId };

  } catch (err) {
    console.error('メッセージ処理エラー:', err);
    return { status: 'error', error: err.message };
  }
}

/**
 * ユーザー情報取得
 */
async function getUserInfo(accessToken, userId) {
  const response = await fetch(`https://www.worksapis.com/v1.0/users/${userId}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  if (!response.ok) {
    throw new Error(`Failed to get user info: ${response.status}`);
  }

  return await response.json();
}

/**
 * ルーム情報取得
 */
async function getRoomInfo(accessToken, roomId) {
  const response = await fetch(`https://www.worksapis.com/v1.0/bots/${process.env.LINEWORKS_BOT_ID}/channels/${roomId}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  if (!response.ok) {
    throw new Error(`Failed to get room info: ${response.status}`);
  }

  return await response.json();
}
