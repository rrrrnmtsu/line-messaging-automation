---
title: "Webhook設定確認ガイド"
type: setup-guide
status: active
created: "2025-10-09"
updated: "2025-10-09"
tags:
  - "project/line-chat-logger"
  - "documentation/setup"
  - "setup/configuration"
  - "integration/webhook"
---

# Webhook設定確認ガイド

## 1. LINE Developers Console 設定確認

### アクセス先
https://developers.line.biz/console/

### 確認手順

#### ステップ1: チャネル選択
1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. プロバイダーを選択
3. チャネル「2008253035」を選択

#### ステップ2: Messaging API設定
1. 「Messaging API」タブを開く
2. 以下を確認:

**Webhook URL:**
```
https://line-message-logger.vercel.app/webhook
```

**Webhook使用:**
- ✅ **有効にする（オン）**

**応答メッセージ:**
- 無効（オフ）推奨

#### ステップ3: Webhook検証
1. 「検証」ボタンをクリック
2. 成功メッセージが表示されればOK
3. エラーが出る場合:
   - `401 Unauthorized` → 署名検証の問題
   - `500 Internal Server Error` → サーバー側のエラー
   - `404 Not Found` → URLが間違っている

## 2. トラブルシューティング

### Case 1: Webhook検証で401エラー
**原因**: 署名検証が厳しすぎる可能性

**対処法**: 一時的に署名検証をスキップしてテスト

1. `/Users/remma/line-chat-logger/api/webhook.js` を編集:
```javascript
// 署名検証を一時的にコメントアウト
/*
const hash = crypto
  .createHmac('SHA256', config.channelSecret)
  .update(body)
  .digest('base64');

if (signature !== hash) {
  console.error('Invalid signature:', { expected: hash, received: signature });
  return res.status(401).json({ error: 'Invalid signature' });
}
*/
```

2. Git push してデプロイ
3. 再度「検証」ボタンをクリック

### Case 2: メッセージが届かない
**確認項目**:
- Webhookが「有効」になっているか
- Webhook URLが正しいか（末尾に`/webhook`）
- LINEアプリで「友だち追加」しているか

### Case 3: ログが表示されない
**確認方法**:
1. Vercel Dashboard → Deployments → 最新デプロイ
2. 「View Function Logs」をクリック
3. リアルタイムログを表示

## 3. テスト手順

### 基本テスト
1. LINEでbotに「テスト」と送信
2. Vercelログで以下を確認:
   ```
   TOKEN LENGTH: 172
   TOKEN START: ZA+vXHlt4P
   MESSAGE SAVED: {...}
   ```

### AI分析テスト
1. 「認証機能を実装します」と送信
2. Vercelログで以下を確認:
   ```
   ACTION ITEMS DETECTED: { tasks: 1, risks: 0, priority: 'low' }
   ```

### ダッシュボード確認
```bash
curl https://line-message-logger.vercel.app/dashboard
```

期待される結果（データがある場合）:
```json
{
  "success": true,
  "actionItems": [...],
  "dashboard": {
    "total_messages": "5",
    "action_items_count": "2",
    ...
  },
  "groups": [...]
}
```

## 4. デバッグコマンド

### Neon SQLでデータ確認
```sql
-- メッセージ数確認
SELECT COUNT(*) FROM line_messages;

-- 最新メッセージ
SELECT timestamp, user_name, content FROM line_messages ORDER BY timestamp DESC LIMIT 5;
```

### Vercelログリアルタイム確認
```bash
# Vercel CLIをインストール（初回のみ）
npm install -g vercel

# ログをリアルタイム表示
vercel logs --follow
```

## 5. 次のステップ

1. ✅ LINE Developers ConsoleでWebhook URL確認
2. ✅ 「検証」ボタンをクリック
3. ✅ テストメッセージ送信
4. ✅ Vercelログ確認
5. ✅ データベース確認（Neon SQL）

エラーが出た場合は、具体的なエラーメッセージを共有してください。

---

## 関連ドキュメント

- [[LINE_SETUP_CHECKLIST]]
- [[README]]

