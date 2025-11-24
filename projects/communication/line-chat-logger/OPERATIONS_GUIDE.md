---
title: "LINE Chat Logger - 運用ガイドライン"
type: documentation
status: active
created: "2025-10-08"
updated: "2025-10-08"
tags:
  - "project/line-chat-logger"
---

# LINE Chat Logger - 運用ガイドライン

## 📋 目次
1. [システム構成](#システム構成)
2. [作業ログ](#作業ログ)
3. [日常運用](#日常運用)
4. [トラブルシューティング](#トラブルシューティング)
5. [復旧手順](#復旧手順)
6. [データベース管理](#データベース管理)

---

## システム構成

### アーキテクチャ
```
LINE Messaging API
    ↓ (Webhook)
Vercel Serverless Functions
    ↓
Neon Postgres Database
```

### 主要コンポーネント

#### 本番環境
- **Vercel プロジェクト**: line-message-logger
- **URL**: https://line-message-logger.vercel.app
- **GitHub**: https://github.com/rrrrnmtsu/line-chat-logger
- **データベース**: Neon Postgres

#### LINE設定
- **Channel ID**: 2008253035
- **Webhook URL**: https://line-message-logger.vercel.app/webhook

---

## 作業ログ

### 初期構築（2025-10-08）

#### フェーズ1: ローカル開発環境構築
```bash
# リポジトリ作成
mkdir /Users/remma/line-chat-logger
cd /Users/remma/line-chat-logger

# 初期ファイル作成
- package.json
- src/index.js (Express.js サーバー)
- src/logger.js (ログ保存機能)
- src/formatter.js (メッセージフォーマット)

# 依存パッケージインストール
npm install
```

#### フェーズ2: Vercel対応
```bash
# Serverless Functions形式に移行
- api/webhook.js 作成
- api/lib/db.js 作成（Vercel Postgres対応）
- vercel.json 設定
```

#### フェーズ3: データベース設定
- Vercel Postgres利用不可 → Neon Postgresに変更
- 環境変数 `POSTGRES_URL` 設定

#### フェーズ4: デプロイ
```bash
# GitHubリポジトリ作成・プッシュ
git init
git add .
git commit -m "Initial commit: LINE Chat Logger for Vercel"
git remote add origin https://github.com/rrrrnmtsu/line-chat-logger.git
git push -u origin main

# Vercelでインポート・デプロイ
```

#### フェーズ5: トラブルシューティング
- LINE認証エラー(401) → トークン再発行・環境変数更新
- DB接続エラー → `POSTGRES_URL`環境変数名修正
- 最終的に動作確認完了

---

## 日常運用

### メッセージログ確認

#### Neon SQLエディタで確認
```sql
-- 最新10件のメッセージ
SELECT * FROM line_messages
ORDER BY timestamp DESC
LIMIT 10;

-- 日付指定
SELECT * FROM line_messages
WHERE DATE(timestamp) = '2025-10-08'
ORDER BY timestamp ASC;

-- ユーザー別集計
SELECT user_name, COUNT(*) as message_count
FROM line_messages
GROUP BY user_name
ORDER BY message_count DESC;
```

#### Vercelログ確認
1. https://vercel.com/dashboard
2. プロジェクト「line-message-logger」選択
3. **Logs** タブでリアルタイムログ確認

### 定期メンテナンス

#### 月次作業
- Vercelデプロイ履歴確認（エラーがないか）
- Neonデータベース容量確認（無料枠: 0.5GB）
- LINE Channel Access Token有効期限確認

#### 四半期作業
- データベースバックアップ
- 古いログのアーカイブ（必要に応じて）

---

## トラブルシューティング

### 問題: メッセージが保存されない

#### 確認事項
1. **Vercelログを確認**
   - https://vercel.com/dashboard → Logs
   - エラーメッセージを確認

2. **LINE Webhook設定確認**
   - URL: https://line-message-logger.vercel.app/webhook
   - 利用: オン
   - 検証ボタンでテスト

3. **環境変数確認**
   ```
   LINE_CHANNEL_SECRET
   LINE_CHANNEL_ACCESS_TOKEN
   POSTGRES_URL
   ```

### 問題: 401 Unauthorized エラー

#### 原因
LINE Channel Access Tokenが無効

#### 解決方法
1. [LINE Developers Console](https://developers.line.biz/console/)
2. チャネル選択 → Messaging API設定
3. チャネルアクセストークン（長期）→ 再発行
4. Vercel環境変数 `LINE_CHANNEL_ACCESS_TOKEN` を更新
5. 再デプロイ

### 問題: DB接続エラー

#### 確認事項
```bash
# Neonコンソールで接続確認
https://console.neon.tech
→ プロジェクト選択
→ SQL Editor で SELECT 1;
```

#### 解決方法
1. Neon接続文字列を再取得
2. Vercel環境変数 `POSTGRES_URL` を更新
3. 再デプロイ

---

## 復旧手順

### シナリオ1: Vercelデプロイ失敗

```bash
# ローカルで動作確認
cd /Users/remma/line-chat-logger
npm install
npm start

# エラーがなければGitHubにプッシュ
git add .
git commit -m "Fix deployment issue"
git push origin main

# Vercelで自動デプロイ実行
```

### シナリオ2: GitHubリポジトリ消失

```bash
# ローカルリポジトリから復旧
cd /Users/remma/line-chat-logger

# 新しいGitHubリポジトリ作成後
git remote set-url origin https://NEW_TOKEN@github.com/rrrrnmtsu/line-chat-logger.git
git push -u origin main

# Vercelで再インポート
```

### シナリオ3: データベース消失

```sql
-- Neonで新規データベース作成後、テーブル再作成
CREATE TABLE IF NOT EXISTS line_messages (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  user_id VARCHAR(100) NOT NULL,
  user_name VARCHAR(100),
  message_id VARCHAR(100) UNIQUE NOT NULL,
  message_type VARCHAR(50),
  content TEXT,
  saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インデックス作成（パフォーマンス向上）
CREATE INDEX idx_timestamp ON line_messages(timestamp);
CREATE INDEX idx_user_id ON line_messages(user_id);
```

### シナリオ4: LINE認証情報消失

1. **Channel Secret取得**
   - LINE Developers Console → Basic settings → Channel secret

2. **Channel Access Token再発行**
   - LINE Developers Console → Messaging API設定
   - チャネルアクセストークン（長期）→ 発行

3. **Vercel環境変数更新**
   ```
   LINE_CHANNEL_SECRET=新しいSecret
   LINE_CHANNEL_ACCESS_TOKEN=新しいToken
   ```

4. **再デプロイ**

---

## データベース管理

### テーブル構造

```sql
CREATE TABLE line_messages (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  user_id VARCHAR(100) NOT NULL,
  user_name VARCHAR(100),
  message_id VARCHAR(100) UNIQUE NOT NULL,
  message_type VARCHAR(50),
  content TEXT,
  saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### データエクスポート

```sql
-- CSV形式でエクスポート（Neon SQL Editor）
COPY (
  SELECT * FROM line_messages
  WHERE DATE(timestamp) >= '2025-10-01'
  ORDER BY timestamp ASC
) TO '/tmp/export.csv' CSV HEADER;
```

### データクリーンアップ

```sql
-- 90日以上前のデータ削除
DELETE FROM line_messages
WHERE timestamp < NOW() - INTERVAL '90 days';

-- VACUUMで容量最適化
VACUUM FULL line_messages;
```

### バックアップ推奨方法

#### 月次バックアップスクリプト
```bash
# Neon管理画面からバックアップ作成
# または定期的にSQLダンプ取得
```

---

## 環境変数一覧

### Vercel Settings → Environment Variables

| 変数名 | 説明 | 取得元 |
|--------|------|--------|
| `LINE_CHANNEL_SECRET` | LINEチャネルシークレット | LINE Developers Console |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINEアクセストークン | LINE Developers Console |
| `POSTGRES_URL` | Neon接続文字列 | Neon Console |

---

## 重要URL・認証情報

### LINE
- **Developers Console**: https://developers.line.biz/console/
- **Channel ID**: 2008253035

### Vercel
- **Dashboard**: https://vercel.com/dashboard
- **Project**: line-message-logger

### Neon
- **Console**: https://console.neon.tech
- **Database**: neondb

### GitHub
- **Repository**: https://github.com/rrrrnmtsu/line-chat-logger

---

## ローカル開発

### セットアップ
```bash
cd /Users/remma/line-chat-logger

# 環境変数設定
cp .env.example .env
# .envを編集

# 依存パッケージインストール
npm install

# ローカルサーバー起動
npm start
```

### ngrokでテスト
```bash
# 別ターミナルで
ngrok http 3000

# 表示されたURLをLINE Webhook URLに設定
```

---

## 今後の拡張案

### 機能追加候補
- [ ] ダッシュボードUI作成（統計表示）
- [ ] 自動レポート機能（日次・週次サマリー）
- [ ] 画像・動画メッセージの保存
- [ ] 検索機能の実装
- [ ] CSVエクスポートAPI

### パフォーマンス最適化
- [ ] データベースインデックス最適化
- [ ] キャッシング導入
- [ ] バッチ処理による負荷分散

---

**作成日**: 2025-10-08
**最終更新**: 2025-10-08
**バージョン**: 1.0.0
