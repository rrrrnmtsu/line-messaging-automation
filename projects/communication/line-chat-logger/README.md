---
title: "LINE Chat Logger"
type: readme
status: active
created: "2025-10-09"
updated: "2025-10-09"
tags:
  - "project/line-chat-logger"
  - "documentation/readme"
---

# LINE Chat Logger

LINEのチャットログを自動で取得・保存し、グループごとにテキストファイルでダウンロードできるツール。

## 機能

- ✅ LINEメッセージの自動保存（Webhook）
- ✅ グループトーク・個人トークの自動分類
- ✅ チャットログのテキストダウンロード
- ✅ グループ別統計ダッシュボード

## デプロイ先

- **URL**: https://line-message-logger.vercel.app/
- **インフラ**: Vercel (Serverless Functions)
- **データベース**: Neon Postgres

## API エンドポイント

### 1. Webhook（LINE Bot用）
```
POST /webhook
```
LINEからのメッセージを受信・保存します。

### 2. ダッシュボード
```
GET /dashboard?days=7
```

**レスポンス例:**
```json
{
  "success": true,
  "stats": {
    "total_messages": "150",
    "unique_users": "5",
    "total_groups": "3",
    "group_messages": "120",
    "direct_messages": "30"
  },
  "groups": [
    {
      "group_name": "プロジェクトA",
      "group_id": "C1234...",
      "message_count": "80",
      "last_message_at": "2025-10-09T12:30:00Z"
    }
  ],
  "period_days": 7
}
```

### 3. ログダウンロード
```
GET /download?group=all
GET /download?group={group_id}
GET /download?group={group_name}
```

**使用例:**
```bash
# 全てのログをダウンロード
curl "https://line-message-logger.vercel.app/download?group=all" -o chat_log.txt

# 特定グループのログをダウンロード
curl "https://line-message-logger.vercel.app/download?group=プロジェクトA" -o project_a_log.txt
```

**ダウンロードファイル形式:**
```
===========================================
LINE Chat Log - プロジェクトA
Generated: 2025/10/09 12:00:00
Total Messages: 80
===========================================

[2025/10/08 10:30:00] 山田太郎
おはようございます

[2025/10/08 10:35:00] 佐藤花子
本日のMTGは14:00からです

...
```

## ローカル開発

### 環境変数設定
`.env` ファイルを作成:
```env
LINE_CHANNEL_SECRET=your_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_access_token
POSTGRES_URL=your_neon_postgres_url
```

### インストール
```bash
npm install
```

### ローカル実行
```bash
vercel dev
```

## データベーススキーマ

### line_messages テーブル
| カラム | 型 | 説明 |
|--------|----|----|
| id | SERIAL | プライマリキー |
| message_id | VARCHAR(100) | LINE メッセージID |
| timestamp | TIMESTAMP | メッセージ送信時刻 |
| user_id | VARCHAR(100) | ユーザーID |
| user_name | VARCHAR(100) | ユーザー表示名 |
| message_type | VARCHAR(20) | メッセージタイプ |
| content | TEXT | メッセージ内容 |
| source_type | VARCHAR(20) | ソースタイプ（user/group/room） |
| group_id | VARCHAR(100) | グループID |
| group_name | VARCHAR(200) | グループ名 |
| room_id | VARCHAR(100) | ルームID |

## LINE Bot 設定

### 1. チャネル作成
[LINE Developers Console](https://developers.line.biz/console/)

### 2. Webhook設定
- **Webhook URL**: `https://line-message-logger.vercel.app/webhook`
- **Use webhook**: ON（有効）
- **応答メッセージ**: OFF（無効）

### 3. 環境変数設定（Vercel）
- `LINE_CHANNEL_SECRET`
- `LINE_CHANNEL_ACCESS_TOKEN`
- `POSTGRES_URL`

## 使い方

### 1. Botを友だち追加
LINE Developers ConsoleのQRコードをスキャン

### 2. メッセージ送信
通常通りトークを送信すると自動保存されます

### 3. ログダウンロード
```bash
# ダッシュボードでグループ一覧を確認
curl https://line-message-logger.vercel.app/dashboard

# ログをダウンロード
curl "https://line-message-logger.vercel.app/download?group=all" -o log.txt
```

### 4. AIツールで分析
ダウンロードしたテキストファイルをChatGPT、Claude等にアップロードして分析:

**プロンプト例:**
```
このLINEチャットログを分析して以下を教えてください:
1. 進行中のタスク一覧
2. ボトルネックやリスク
3. 優先度の高いアクション
```

## ライセンス

MIT

## 技術スタック

- **Runtime**: Node.js 18
- **Framework**: Vercel Serverless Functions
- **Database**: Neon Postgres
- **LINE SDK**: @line/bot-sdk v9.3.0

---

## 関連ドキュメント

### セットアップ・設定
- [[LINE_SETUP_CHECKLIST]]
- [[WEBHOOK_SETUP_GUIDE]]

