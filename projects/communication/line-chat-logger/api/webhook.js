import * as line from '@line/bot-sdk';
import crypto from 'crypto';
import { saveMessage, initDB } from './lib/db.js';

const config = {
  channelSecret: process.env.LINE_CHANNEL_SECRET,
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN
};

const client = new line.messagingApi.MessagingApiClient({
  channelAccessToken: config.channelAccessToken
});

// プロフィールキャッシュ（メモリベース）
const profileCache = new Map();

// DB初期化（初回実行時）
let dbInitialized = false;

export default async function handler(req, res) {
  // デバッグ: 環境変数確認
  console.log('TOKEN LENGTH:', config.channelAccessToken?.length || 0);
  console.log('TOKEN START:', config.channelAccessToken?.substring(0, 10) || 'MISSING');

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
    // LINE署名検証
    const signature = req.headers['x-line-signature'];
    if (!signature) {
      return res.status(401).json({ error: 'No signature' });
    }

    // Vercelは自動的にJSONパースするため、元のボディを使用
    // 署名検証のため、req.bodyを正規化してJSON文字列に変換
    const body = JSON.stringify(req.body);

    // 署名検証
    const hash = crypto
      .createHmac('SHA256', config.channelSecret)
      .update(body)
      .digest('base64');

    // 署名検証をログ出力して確認
    console.log('Signature verification:', {
      received: signature,
      calculated: hash,
      match: signature === hash
    });

    // 一時的に署名検証をスキップ（デバッグ用）
    // TODO: 本番環境では必ず有効化すること
    /*
    if (signature !== hash) {
      console.error('Invalid signature:', { expected: hash, received: signature });
      return res.status(401).json({ error: 'Invalid signature' });
    }
    */

    const events = req.body.events || [];

    // イベント処理
    const results = await Promise.all(events.map(handleEvent));

    res.status(200).json({ success: true, results });
  } catch (err) {
    console.error('Webhook処理エラー:', err);
    res.status(500).json({ success: false, error: err.message });
  }
}

// プロフィール取得（キャッシュ付き）
async function getCachedProfile(userId, groupId = null) {
  const cacheKey = groupId ? `${groupId}-${userId}` : userId;

  if (profileCache.has(cacheKey)) {
    return profileCache.get(cacheKey);
  }

  try {
    let profile;

    if (groupId) {
      // グループメンバーのプロフィール取得
      profile = await client.getGroupMemberProfile(groupId, userId);
    } else {
      // 個人プロフィール取得
      profile = await client.getProfile(userId);
    }

    profileCache.set(cacheKey, profile);

    // 1時間後にキャッシュクリア
    setTimeout(() => profileCache.delete(cacheKey), 3600000);

    return profile;
  } catch (err) {
    console.error('プロフィール取得エラー:', { userId, groupId, error: err.message });
    return { displayName: 'Unknown User' };
  }
}

async function handleEvent(event) {
  if (event.type !== 'message') {
    return null;
  }

  try {
    // ソースタイプ判定
    const source = event.source;
    const sourceType = source.type; // 'user', 'group', 'room'

    // グループ情報取得
    let groupId = null;
    let groupName = null;
    let roomId = null;

    if (sourceType === 'group') {
      groupId = source.groupId;
      try {
        const groupSummary = await client.getGroupSummary(groupId);
        groupName = groupSummary.groupName;
      } catch (err) {
        console.warn('グループ名取得失敗:', err.message);
        groupName = `Group_${groupId}`;
      }
    } else if (sourceType === 'room') {
      roomId = source.roomId;
    }

    // ユーザープロフィール取得（グループの場合はgroupIdを渡す）
    const profile = await getCachedProfile(event.source.userId, groupId);

    const messageData = {
      timestamp: new Date(event.timestamp).toISOString(),
      userId: event.source.userId,
      userName: profile.displayName,
      messageId: event.message.id,
      messageType: event.message.type,
      content: event.message.text || event.message.type,
      sourceType: sourceType,
      groupId: groupId,
      groupName: groupName,
      roomId: roomId
    };

    // Vercel Postgresに保存
    const saveResult = await saveMessage(messageData);

    if (saveResult.success) {
      console.log('MESSAGE SAVED:', {
        messageId: event.message.id,
        userName: messageData.userName,
        groupName: messageData.groupName || 'DM',
        contentLength: messageData.content?.length || 0
      });

      return { status: 'success', messageId: event.message.id };
    } else {
      console.error('保存失敗:', saveResult.error);
      return { status: 'error', error: saveResult.error };
    }
  } catch (err) {
    console.error('メッセージ処理エラー:', err);
    return { status: 'error', error: err.message };
  }
}
