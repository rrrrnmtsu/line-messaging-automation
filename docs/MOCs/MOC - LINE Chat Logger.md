---
title: "MOC - LINE Chat Logger"
type: moc
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "project/line-chat-logger"
  - "navigation/moc"
---

# MOC - LINE Chat Logger

**プロジェクト**: LINEチャットログ自動保存システム
**目的**: LINEのチャットログを自動取得・保存し、グループごとにテキストファイルでダウンロード
**ステータス**: 本番稼働中

---

## 概要

LINE Messaging APIを使用したWebhookベースのチャットログ自動保存システム。グループトークや個人トークを自動分類し、PostgreSQLデータベースに保存。ダッシュボードでグループ別統計を確認でき、AIツールで分析可能なテキスト形式でログをダウンロード可能。

**主要機能**:
- LINEメッセージの自動保存（Webhook）
- グループトーク・個人トークの自動分類
- チャットログのテキストダウンロード
- グループ別統計ダッシュボード

---

## デプロイ情報

### 本番環境
- **URL**: https://line-message-logger.vercel.app/
- **インフラ**: Vercel (Serverless Functions)
- **データベース**: Neon Postgres
- **Runtime**: Node.js 18

---

## クイックスタート

### 基本情報
- [[README|projects/communication/line-chat-logger/README]] - プロジェクト全体概要・使用方法

### セットアップ
1. [[LINE_SETUP_CHECKLIST|projects/communication/line-chat-logger/LINE_SETUP_CHECKLIST]] - LINE Bot作成チェックリスト
2. [[WEBHOOK_SETUP_GUIDE|projects/communication/line-chat-logger/WEBHOOK_SETUP_GUIDE]] - Webhook設定ガイド

---

## API エンドポイント

### 1. Webhook（LINE Bot用）
```
POST /webhook
```
LINE Platformからのメッセージを受信・保存

**用途**: LINE Bot内部処理（ユーザーが直接使用しない）

---

### 2. ダッシュボード
```
GET /dashboard?days=7
```

**パラメータ**:
- `days`: 統計期間（デフォルト: 7日間）

**レスポンス例**:
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

---

### 3. ログダウンロード
```
GET /download?group=all
GET /download?group={group_id}
GET /download?group={group_name}
```

**パラメータ**:
- `group`: ダウンロード対象グループ
  - `all`: 全グループ
  - `{group_id}`: 特定グループID
  - `{group_name}`: グループ名（URLエンコード必要）

**使用例**:
```bash
# 全てのログをダウンロード
curl "https://line-message-logger.vercel.app/download?group=all" -o chat_log.txt

# 特定グループのログをダウンロード
curl "https://line-message-logger.vercel.app/download?group=プロジェクトA" -o project_a_log.txt
```

**ダウンロードファイル形式**:
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

---

## データベーススキーマ

### line_messages テーブル
| カラム | 型 | 説明 |
|--------|----|----|
| id | SERIAL | プライマリキー |
| message_id | VARCHAR(100) | LINE メッセージID（一意） |
| timestamp | TIMESTAMP | メッセージ送信時刻 |
| user_id | VARCHAR(100) | ユーザーID |
| user_name | VARCHAR(100) | ユーザー表示名 |
| message_type | VARCHAR(20) | メッセージタイプ（text, image等） |
| content | TEXT | メッセージ内容 |
| source_type | VARCHAR(20) | ソースタイプ（user/group/room） |
| group_id | VARCHAR(100) | グループID（NULL可） |
| group_name | VARCHAR(200) | グループ名（NULL可） |
| room_id | VARCHAR(100) | ルームID（NULL可） |

**インデックス**:
- `message_id` (UNIQUE)
- `timestamp`
- `group_id`

---

## プロジェクト構造

```
projects/communication/line-chat-logger/
├── api/
│   ├── webhook.js              # Webhook受信エンドポイント
│   ├── dashboard.js            # 統計ダッシュボード
│   └── download.js             # ログダウンロード
├── lib/
│   └── db.js                   # データベース接続
├── package.json                # 依存関係
├── vercel.json                 # Vercelデプロイ設定
└── README.md                   # ドキュメント
```

---

## 技術スタック

### フロントエンド・バックエンド
- **Runtime**: Node.js 18
- **Framework**: Vercel Serverless Functions
- **LINE SDK**: @line/bot-sdk v9.3.0

### データベース
- **Database**: Neon Postgres（Serverless PostgreSQL）
- **ORM**: Native pg client

### デプロイメント
- **Platform**: Vercel
- **CI/CD**: Gitプッシュで自動デプロイ

---

## LINE Bot 設定

### 1. チャネル作成
[LINE Developers Console](https://developers.line.biz/console/)でチャネル作成

### 2. Webhook設定
- **Webhook URL**: `https://line-message-logger.vercel.app/webhook`
- **Use webhook**: ON（有効）
- **応答メッセージ**: OFF（無効）
- **Verify**: Webhookの検証を実行

### 3. 環境変数設定（Vercel）
Vercel Dashboardで以下を設定:
- `LINE_CHANNEL_SECRET`: LINEチャネルシークレット
- `LINE_CHANNEL_ACCESS_TOKEN`: LINEチャネルアクセストークン
- `POSTGRES_URL`: Neon PostgreSQL接続URL

---

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

### ローカルWebhookテスト
ngrokを使用してローカル環境をインターネットに公開:
```bash
ngrok http 3000
```

---

## 使い方

### 1. Botを友だち追加
LINE Developers ConsoleのQRコードをスキャンして友だち追加

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

**プロンプト例**:
```
このLINEチャットログを分析して以下を教えてください:
1. 進行中のタスク一覧
2. ボトルネックやリスク
3. 優先度の高いアクション
```

---

## トラブルシューティング

### Webhookが受信されない
**症状**: LINEメッセージが保存されない
**対処**:
1. Webhook URLが正しく設定されているか確認
2. LINE Developers ConsoleでWebhook検証を実行
3. Vercelのログを確認（`vercel logs`）
4. `LINE_CHANNEL_SECRET`と`LINE_CHANNEL_ACCESS_TOKEN`が正しいか確認

### データベース接続エラー
**症状**: 500エラー、データベース接続失敗
**対処**:
1. `POSTGRES_URL`が正しいか確認
2. Neon Postgresのステータス確認
3. データベース接続数制限に達していないか確認

### ログダウンロードエラー
**症状**: ダウンロード時に空ファイルまたはエラー
**対処**:
1. グループ名が正しいか確認（URLエンコード必要）
2. データベースにメッセージが保存されているか確認
3. `group_id`を使用してダウンロードを試す

---

## セキュリティ

### 認証情報管理
- `LINE_CHANNEL_SECRET`と`LINE_CHANNEL_ACCESS_TOKEN`は環境変数で管理
- `.env`ファイルは`.gitignore`で除外
- Vercel環境変数は暗号化保存

### データ取り扱い
- チャットログには個人情報が含まれる可能性あり
- ダウンロードAPIは認証なし（URLを知っている人のみアクセス可能）
- 本番環境では認証機能の追加を検討

---

## 関連プロジェクト

### 類似プロジェクト
- [[LINE Works Chat Logger|projects/communication/lineworks-chat-logger/README]] - LINE WORKS版チャットロガー

---

## 関連MOC

- [[Home]] - Vaultホーム
- [[MOC - API Integration]] - API統合パターン
- [[MOC - Deployment]] - Vercelデプロイメント手法
- [[MOC - Troubleshooting]] - トラブルシューティング全般

---

## 次のステップ

### 機能拡張
- [ ] 認証機能追加（APIキーまたはBasic認証）
- [ ] Webhook署名検証強化
- [ ] 画像・動画メッセージの保存
- [ ] リアルタイムダッシュボード（WebSocket）

### 最適化
- [ ] データベースインデックス最適化
- [ ] ログダウンロードのページネーション
- [ ] キャッシュ機構導入

---

**開始日**: 2025年10月9日
**最終更新**: 2025-11-01
**メンテナンス**: 必要に応じて更新

---

## 関連ドキュメント

- [[Home]]
- [[MOC - API Integration]]
- [[MOC - Deployment]]
- [[README|projects/communication/line-chat-logger/README]]
- [[LINE_SETUP_CHECKLIST|projects/communication/line-chat-logger/LINE_SETUP_CHECKLIST]]
- [[WEBHOOK_SETUP_GUIDE|projects/communication/line-chat-logger/WEBHOOK_SETUP_GUIDE]]
