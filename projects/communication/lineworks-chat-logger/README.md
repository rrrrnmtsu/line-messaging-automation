---
title: "LINE WORKS Chat Logger"
type: readme
status: active
created: "2025-10-09"
updated: "2025-10-09"
tags:
  - "project/lineworks-chat-logger"
  - "documentation/readme"
---

# LINE WORKS Chat Logger

LINE WORKSのチャットログを自動で取得・保存し、トークルームごとにテキストファイルでダウンロードできるツール。

## 機能

- ✅ LINE WORKSメッセージの自動保存（Webhook）
- ✅ トークルーム・個人トークの自動分類
- ✅ チャットログのテキストダウンロード
- ✅ トークルーム別統計ダッシュボード

## セットアップ手順

### 1. LINE WORKS Developer Console設定

https://developers.worksmobile.com/

#### Bot作成
1. Developer Consoleにログイン
2. 「Bot」→「登録」
3. Bot情報を入力
4. 以下の情報を取得:
   - **Bot No.**
   - **Server API Consumer Key**
   - **Server List ID**
   - **Private Key** (JWT生成用)

#### Webhook設定
1. Bot設定画面で「Callback URL」を設定
2. `https://your-app.vercel.app/webhook` を入力
3. 「検証」をクリック

### 2. Neon Postgres設定

1. https://neon.tech/ でアカウント作成
2. 新しいプロジェクトを作成
3. 接続文字列を取得

### 3. Vercel設定

#### 環境変数
Vercelプロジェクトで以下を設定:

```
LINEWORKS_BOT_NO=your_bot_no
LINEWORKS_CONSUMER_KEY=your_consumer_key
LINEWORKS_SERVER_LIST_ID=your_server_list_id
LINEWORKS_PRIVATE_KEY=your_private_key_base64
POSTGRES_URL=your_neon_postgres_url
```

**注意**: Private Keyはbase64エンコードして設定してください。

```bash
cat private_key.pem | base64
```

## API エンドポイント

### 1. Webhook（LINE WORKS Bot用）
```
POST /webhook
```

### 2. ダッシュボード
```
GET /dashboard?days=7
```

### 3. ログダウンロード
```
GET /download?room=all
GET /download?room={room_id}
```

## 使い方

### 1. Botを追加
LINE WORKSアプリでBotを追加

### 2. メッセージ送信
通常通りトークを送信すると自動保存

### 3. ログダウンロード
```bash
curl "https://your-app.vercel.app/download?room=all" -o chat_log.txt
```

## LINE WORKSとLINEの違い

| 項目 | LINE | LINE WORKS |
|------|------|------------|
| 認証方式 | Channel Access Token | JWT (Server API) |
| メッセージ取得 | Webhook | Webhook |
| ユーザー情報 | getProfile() | Bot API (ユーザー情報取得) |
| グループ | Group/Room | Talk Room |

## 技術スタック

- **Runtime**: Node.js 18
- **Framework**: Vercel Serverless Functions
- **Database**: Neon Postgres
- **認証**: JWT (jsonwebtoken)

## ライセンス

MIT
# Updated Thu Oct  9 16:28:41 JST 2025
