---
title: "LINE Bot設定チェックリスト"
type: setup-guide
status: active
created: "2025-10-09"
updated: "2025-10-09"
tags:
  - "project/line-chat-logger"
  - "documentation/setup"
  - "setup/configuration"
---

# LINE Bot設定チェックリスト

## 1. 友だち追加確認

### QRコード取得
1. [LINE Developers Console](https://developers.line.biz/console/) にアクセス
2. チャネル「2008253035」を選択
3. 「Messaging API」タブ
4. 下にスクロールして「QRコード」を表示
5. LINEアプリでQRコードをスキャンして友だち追加

### 確認方法
- LINEアプリで該当のbotアカウントがトーク一覧に表示されているか

## 2. Webhook設定確認

### Messaging API設定
- **Webhook URL**: `https://line-message-logger.vercel.app/webhook`
- **Webhookの利用**: ✅ **有効**（オンにする）
- **応答メッセージ**: ⭕ **無効**（オフにする）

### 重要：応答メッセージ設定
⚠️ **応答メッセージが有効だとWebhookが呼ばれません**

設定場所:
1. LINE Developers Console
2. チャネル選択
3. 「Messaging API」タブ
4. 「応答メッセージ」の項目を探す
5. **オフ（無効）にする**

## 3. チャネルアクセストークン確認

現在のトークン:
```
ZA+vXHlt4PXEuhbinRdxEWFNCzJ9DKdTpmQLUjIJzZhbxQM3LexuQm6giATk19v2M0b8i9AoVS1519S/tbWXc6bhPoTY7C6WzPBtGKLqGAT1N0AQ/8DXpCPMQHblrJL0FSpK+0c609tEuQhjM4qZgwdB04t89/1O/w1cDnyilFU=
```

### 確認方法
Vercelの環境変数 `LINE_CHANNEL_ACCESS_TOKEN` が上記と一致しているか

## 4. テスト手順

### Step 1: 友だち追加
LINEアプリでbotを友だち追加

### Step 2: メッセージ送信
```
認証機能を実装します
```

### Step 3: Vercelログ確認
[Vercel Dashboard](https://vercel.com/rrrrnmtsu/line-message-logger) で以下のログを確認:
```
TOKEN LENGTH: 172
MESSAGE SAVED: ...
ACTION ITEMS DETECTED: ...
```

### Step 4: ダッシュボード確認
```bash
curl https://line-message-logger.vercel.app/dashboard
```

期待される結果:
```json
{
  "success": true,
  "dashboard": {
    "total_messages": "1",  // ← 0でない
    "action_items_count": "1"
  }
}
```

## 5. トラブルシューティング

### ケース1: ログが全く表示されない
**原因**: Webhookが呼ばれていない

**確認**:
- 応答メッセージが**無効**になっているか
- Webhookが**有効**になっているか
- 友だち追加しているか

### ケース2: 401エラー
**原因**: 署名検証エラー（現在は無効化済み）

### ケース3: 500エラー
**原因**: サーバー側のエラー

**対処**: Vercelログで詳細を確認

## 6. 現在の状態

✅ Webhook署名検証: 一時的に無効化（デバッグ用）
✅ データベース接続: 正常
✅ テストスクリプト: 成功（total_messages: 1）
❓ LINEからのメッセージ: 未確認

**次のアクション**:
1. 応答メッセージを**無効**にする
2. 友だち追加を確認
3. メッセージを送信
4. Vercelログを確認
