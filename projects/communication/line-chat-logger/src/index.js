import express from 'express';
import * as line from '@line/bot-sdk';
import dotenv from 'dotenv';
import { saveMessage } from './logger.js';
import { formatMessage } from './formatter.js';

dotenv.config();

const config = {
  channelSecret: process.env.LINE_CHANNEL_SECRET,
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN
};

const client = new line.messagingApi.MessagingApiClient({
  channelAccessToken: config.channelAccessToken
});

const app = express();

// Webhook エンドポイント
app.post('/webhook', line.middleware(config), async (req, res) => {
  try {
    const results = await Promise.all(req.body.events.map(handleEvent));
    res.json({ success: true, results });
  } catch (err) {
    console.error('Webhook処理エラー:', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

async function handleEvent(event) {
  // メッセージイベントのみ処理
  if (event.type !== 'message') {
    return null;
  }

  try {
    // ユーザープロフィール取得
    const profile = await client.getProfile(event.source.userId);

    // メッセージ情報整形
    const messageData = {
      timestamp: new Date(event.timestamp),
      userId: event.source.userId,
      userName: profile.displayName,
      messageId: event.message.id,
      messageType: event.message.type,
      content: event.message.text || event.message.type,
      replyToken: event.replyToken
    };

    // ログ保存
    await saveMessage(messageData);

    // フォーマットして表示
    console.log(formatMessage(messageData));

    return { status: 'success', messageId: event.message.id };
  } catch (err) {
    console.error('メッセージ処理エラー:', err);
    return { status: 'error', error: err.message };
  }
}

// ヘルスチェック
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`LINE Chat Logger サーバー起動: ポート ${PORT}`);
  console.log(`Webhook URL: http://localhost:${PORT}/webhook`);
});
