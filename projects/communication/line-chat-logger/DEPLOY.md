---
title: "Vercelデプロイ手順"
type: documentation
status: active
created: "2025-10-08"
updated: "2025-10-08"
tags:
  - "project/line-chat-logger"
---

# Vercelデプロイ手順

## 前提条件
- Vercelアカウント（無料）
- GitHubアカウント

## 1. GitHubリポジトリ作成

```bash
cd /Users/remma/line-chat-logger
git init
git add .
git commit -m "Initial commit: LINE Chat Logger for Vercel"
```

GitHubで新規リポジトリ作成後:

```bash
git remote add origin https://github.com/YOUR_USERNAME/line-chat-logger.git
git branch -M main
git push -u origin main
```

## 2. Vercelプロジェクト作成

1. https://vercel.com にアクセス
2. 「New Project」クリック
3. GitHubリポジトリ（line-chat-logger）をインポート
4. 「Deploy」クリック

## 3. Vercel Postgres設定

1. Vercelダッシュボード → プロジェクト選択
2. 「Storage」タブ → 「Create Database」
3. 「Postgres」を選択 → 「Continue」
4. データベース名を入力 → 「Create」
5. 自動的に環境変数が設定されます

## 4. LINE認証情報を環境変数に設定

1. Vercelダッシュボード → 「Settings」 → 「Environment Variables」
2. 以下を追加:

```
LINE_CHANNEL_SECRET=cfa0ba820ef777f9ccbd9afc2282cdf2
LINE_CHANNEL_ACCESS_TOKEN=9coUUY+W6YpfQrNNFiAEemWTiQufS8zMAhQPuhUm3zm+t82pwAAngTnRAPtc6OwNM0b8i9AoVS1519S/tbWXc6bhPoTY7C6WzPBtGKLqGAT1N0AQ/8DXpCPMQHblrJL0FSpK+0c609tEuQhjM4qZgwdB04t89/1O/w1cDnyilFU=
```

3. 「Save」クリック

## 5. 再デプロイ

1. 「Deployments」タブ
2. 最新デプロイの「...」メニュー → 「Redeploy」

## 6. Webhook URL設定

1. デプロイ完了後、URLを確認（例: `https://line-chat-logger.vercel.app`）
2. LINE Developers Console → Messaging API設定
3. Webhook URLに設定:
   ```
   https://line-chat-logger.vercel.app/webhook
   ```
4. 「検証」ボタンでテスト

## 完了！

LINEにメッセージを送信すると、Vercel Postgresに自動保存されます。

## ログ確認

Vercelダッシュボード → 「Logs」でリアルタイムログ確認可能

## データベース確認

Vercelダッシュボード → 「Storage」 → データベース選択 → 「Data」タブでデータ確認
