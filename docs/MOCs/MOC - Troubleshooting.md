---
title: "MOC - Troubleshooting"
type: moc
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "navigation/moc"
  - "troubleshooting/guide"
---

# MOC - Troubleshooting

**カテゴリ**: クロスプロジェクトMOC
**対象**: トラブルシューティング・エラー解決
**適用範囲**: 全プロジェクト

---

## 概要

複数のプロジェクトで発生する共通エラー・問題の解決方法を集約したMOC。カテゴリ別に整理し、迅速な問題解決をサポート。

---

## クイック診断

### 問題のカテゴリを特定

| 症状 | カテゴリ | セクション |
|-----|---------|-----------|
| 認証エラー（401, 403） | 認証・API | [[#認証エラー]] |
| APIリクエスト失敗 | API統合 | [[#API接続エラー]] |
| データベース接続失敗 | データベース | [[#データベースエラー]] |
| Webhook受信されない | Webhook | [[#Webhookエラー]] |
| n8nワークフロー失敗 | n8n | [[#n8nエラー]] |
| Google Sheets書き込み失敗 | Google Services | [[#Google Sheetsエラー]] |
| Docker起動失敗 | インフラ | [[#Dockerエラー]] |
| デプロイ失敗 | デプロイメント | [[#デプロイメントエラー]] |

---

## 認証エラー

### OAuth 2.0エラー

#### トークン期限切れ
**症状**:
```
401 Unauthorized
Error: Token has expired
```

**原因**: アクセストークンの有効期限切れ

**対処法**:
1. **n8nの場合**: Credentialsで「Reconnect」をクリック
2. **Pythonの場合**: リフレッシュトークンで新しいアクセストークンを取得
```python
credentials.refresh(Request())
```

**関連ドキュメント**:
- [[MOC - Authentication]]
- [[GOOGLE-OAUTH-SETUP|projects/automation/dify-n8n-workflow/n8n/GOOGLE-OAUTH-SETUP]]

---

#### スコープ不足
**症状**:
```
403 Forbidden
Error: Insufficient Permission
```

**原因**: OAuth 2.0スコープが不足

**対処法**:
1. 必要なスコープを確認
2. OAuth設定でスコープを追加:
```
https://www.googleapis.com/auth/spreadsheets  # 読み書き
https://www.googleapis.com/auth/drive         # Drive API
```
3. 再認証を実行

---

### APIキーエラー

#### 無効なAPIキー
**症状**:
```
401 Unauthorized
Invalid API Key
```

**対処法**:
1. 環境変数を確認:
```bash
echo $API_KEY_NAME
```
2. APIキーが正しいか確認（サービス側ダッシュボード）
3. 必要に応じて再発行

**関連プロジェクト**:
- [[MOC - LINE Chat Logger]]
- [[MOC - Dify n8n Workflow]]

---

#### レート制限
**症状**:
```
429 Too Many Requests
Rate limit exceeded
```

**対処法**:
1. リクエスト頻度を下げる
2. エクスポネンシャルバックオフを実装:
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.statusCode === 429) {
        await sleep(Math.pow(2, i) * 1000);  // 1s, 2s, 4s
        continue;
      }
      throw error;
    }
  }
}
```
3. APIプランのアップグレードを検討

---

## API接続エラー

### タイムアウトエラー
**症状**:
```
Error: connect ETIMEDOUT
Error: Request timeout
```

**対処法**:
1. タイムアウト時間を延長:
```javascript
// n8n HTTP Request Node
Timeout: 30000  // 30秒
```
2. ネットワーク接続を確認
3. APIサービスのステータスページを確認

---

### SSL/TLS証明書エラー
**症状**:
```
Error: unable to verify the first certificate
```

**対処法（開発環境のみ）**:
```javascript
// Node.js
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
```

**本番環境**: SSL証明書を正しく設定

---

## データベースエラー

### PostgreSQL接続エラー

#### 接続失敗
**症状**:
```
Error: connect ECONNREFUSED 127.0.0.1:5432
FATAL: password authentication failed
```

**対処法**:
1. PostgreSQLが起動しているか確認:
```bash
docker compose ps
```
2. 接続情報を確認:
```bash
# .env
POSTGRES_PASSWORD=correct_password
POSTGRES_URL=postgresql://user:password@host:5432/database
```
3. ファイアウォール・ネットワーク設定を確認

**関連プロジェクト**:
- [[MOC - Dify n8n Workflow]]
- [[MOC - LINE Chat Logger]]

---

#### 接続数制限
**症状**:
```
Error: too many clients
```

**対処法**:
1. 接続プールサイズを調整:
```javascript
const pool = new Pool({
  max: 10,  // 最大接続数
  idleTimeoutMillis: 30000
});
```
2. 未使用の接続を閉じる
3. データベースの`max_connections`設定を確認

---

## Webhookエラー

### LINE Messaging API

#### Webhook受信されない
**症状**: メッセージを送信してもWebhookが動作しない

**対処法**:
1. Webhook URLが正しいか確認（LINE Developers Console）
2. Webhook検証を実行:
```bash
# LINE Developers Console
Messaging API → Webhook settings → Verify
```
3. サーバーログを確認:
```bash
# Vercel
vercel logs

# ローカル
console.log('Received webhook:', req.body);
```
4. 署名検証が正しく実装されているか確認

**関連ドキュメント**:
- [[README|projects/communication/line-chat-logger/README]]
- [[WEBHOOK_SETUP_GUIDE|projects/communication/line-chat-logger/WEBHOOK_SETUP_GUIDE]]

---

#### 署名検証エラー
**症状**:
```
400 Bad Request
Invalid signature
```

**対処法**:
1. Channel Secretが正しいか確認
2. 署名検証コードを確認:
```javascript
const signature = req.headers['x-line-signature'];
const hash = crypto
  .createHmac('SHA256', channelSecret)
  .update(JSON.stringify(req.body))
  .digest('base64');

if (hash !== signature) {
  return res.status(400).send('Invalid signature');
}
```

---

### Telegram Bot API

#### Bot Token無効
**症状**:
```
401 Unauthorized
Invalid bot token
```

**対処法**:
1. Bot Tokenを確認（@BotFatherから取得）
2. 環境変数を確認:
```bash
echo $TELEGRAM_BOT_TOKEN
```
3. 必要に応じてBot Tokenを再発行

**関連ドキュメント**:
- [[telegram-bot-setup|projects/automation/dify-n8n-workflow/docs/telegram-bot-setup]]

---

#### プライバシーモードエラー
**症状**: グループチャットでBotがメッセージを受信しない

**対処法**:
1. @BotFatherでプライバシーモードを無効化:
```
/mybots → Select bot → Bot Settings → Group Privacy → Turn off
```

**関連ドキュメント**:
- [[troubleshooting-privacy-mode|projects/automation/dify-n8n-workflow/docs/troubleshooting-privacy-mode]]

---

## n8nエラー

### Mergeノードエラー

#### Multiple Matching Items
**症状**:
```
Error: There are multiple items matching the expression
```

**原因**: Merge設定でマッチング条件が複数のアイテムに該当

**対処法**:
1. Split In Batches使用（推奨）:
```
Split In Batches (Batch Size: 1)
  → Process each item
  → Merge
```

2. Code Nodeで手動Merge:
```javascript
const items = $input.all();
return items.map((item, index) => ({
  json: {
    ...item.json,
    uniqueId: index
  }
});
```

**関連ドキュメント**:
- [[MERGE-NODE-FIX|projects/automation/dify-n8n-workflow/n8n/MERGE-NODE-FIX]]
- [[MULTIPLE-MATCHING-ITEMS-FIX|projects/automation/dify-n8n-workflow/n8n/MULTIPLE-MATCHING-ITEMS-FIX]]
- [[MULTI-ROW-FIX-GUIDE|projects/automation/dify-n8n-workflow/n8n/MULTI-ROW-FIX-GUIDE]]

---

### Google Sheets Pro UPSERTエラー
**症状**: UPSERT操作が失敗

**対処法**:
1. マッチング列を確認（列Aが推奨）
2. データ型の一致を確認
3. 権限を確認（書き込み権限必要）

**関連ドキュメント**:
- [[UPDATE-GOOGLE-SHEETS-PRO-SETUP|projects/automation/dify-n8n-workflow/n8n/UPDATE-GOOGLE-SHEETS-PRO-SETUP]]

---

### DataForSEO APIエラー
**症状**: 認証エラー、データ抽出エラー

**対処法**:
1. Basic認証情報を確認
2. エンドポイントURLを確認
3. レスポンス構造を確認（APIバージョン変更の可能性）

**関連ドキュメント**:
- [[DATAFORSEO-API-FIX|projects/automation/dify-n8n-workflow/n8n/DATAFORSEO-API-FIX]]
- [[DATAFORSEO-AUTHENTICATION-GUIDE|projects/automation/dify-n8n-workflow/n8n/DATAFORSEO-AUTHENTICATION-GUIDE]]

---

## Google Sheetsエラー

### 書き込み失敗

#### 権限不足
**症状**:
```
403 Forbidden
The caller does not have permission
```

**対処法**:
1. サービスアカウントに編集権限を付与:
   - Google Sheetsで「共有」
   - サービスアカウントのメールアドレスを追加
   - 「編集者」権限を付与

2. OAuth 2.0のスコープを確認:
```
https://www.googleapis.com/auth/spreadsheets
```

**関連ドキュメント**:
- [[MOC - Google Services]]
- [[GOOGLE_SHEETS_SETUP|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]]

---

#### スプレッドシートIDエラー
**症状**:
```
404 Not Found
Requested entity was not found
```

**対処法**:
1. スプレッドシートIDを確認:
```
https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
```
2. スプレッドシートが削除されていないか確認
3. アクセス権限があるか確認

---

## Dockerエラー

### コンテナ起動失敗

#### ポート競合
**症状**:
```
Error: bind: address already in use
```

**対処法**:
1. 使用中のポートを確認:
```bash
lsof -i :5678
```
2. `.env`でポート変更:
```env
N8N_PORT=5679
```
3. 競合プロセスを停止

---

#### イメージビルドエラー
**症状**:
```
Error: failed to build image
```

**対処法**:
1. Dockerイメージキャッシュをクリア:
```bash
docker compose build --no-cache
```
2. Dockerディスク容量を確認:
```bash
docker system df
```
3. 不要なイメージ・コンテナを削除:
```bash
docker system prune -a
```

**関連ドキュメント**:
- [[setup|projects/automation/dify-n8n-workflow/docs/setup]]

---

## デプロイメントエラー

### Vercelデプロイ失敗

#### 環境変数未設定
**症状**: デプロイ成功後、ランタイムエラー

**対処法**:
1. Vercel Dashboardで環境変数を設定
2. 必要な環境変数:
```
LINE_CHANNEL_SECRET
LINE_CHANNEL_ACCESS_TOKEN
POSTGRES_URL
```
3. 再デプロイ

**関連プロジェクト**:
- [[MOC - LINE Chat Logger]]

---

#### ビルドエラー
**症状**:
```
Error: Build failed
```

**対処法**:
1. `package.json`の依存関係を確認
2. Node.jsバージョンを確認（Vercelのサポート範囲内か）
3. ビルドログを詳細確認:
```bash
vercel logs --output
```

---

## 一般的なトラブルシューティング手法

### ログ確認

#### n8n
```bash
# Dockerログ
docker compose logs -f n8n

# 特定ワークフローの実行ログ
# n8n UI: Executions → 詳細
```

#### Vercel
```bash
vercel logs --follow
vercel logs --output
```

#### Python
```bash
tail -f logs/application.log
```

---

### デバッグモード

#### n8n
```bash
# .env
N8N_LOG_LEVEL=debug
```

#### Node.js
```bash
NODE_ENV=development node app.js
```

---

### ネットワーク診断

#### 接続確認
```bash
# API疎通確認
curl -I https://api.example.com/endpoint

# Webhookテスト
curl -X POST https://your-domain.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

#### DNS確認
```bash
nslookup api.example.com
dig api.example.com
```

---

## プロジェクト固有トラブルシューティング

### Dify n8n Workflow
- [[ISSUES-FIX|projects/automation/dify-n8n-workflow/n8n/ISSUES-FIX]]
- [[ERROR-FIX-MULTIPLE-MATCHING-ITEMS|projects/automation/dify-n8n-workflow/n8n/ERROR-FIX-MULTIPLE-MATCHING-ITEMS]]
- [[n8n-merge-issues-fix|projects/automation/dify-n8n-workflow/docs/n8n-merge-issues-fix]]

### Airregi Analytics
- [[GOOGLE_SHEETS_SETUP#トラブルシューティング|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]]

### LINE Chat Logger
- [[WEBHOOK_SETUP_GUIDE|projects/communication/line-chat-logger/WEBHOOK_SETUP_GUIDE]]

---

## 関連MOC

- [[Home]] - Vaultホーム
- [[MOC - API Integration]] - API統合パターン
- [[MOC - Authentication]] - 認証エラー
- [[MOC - Google Services]] - Google Servicesエラー
- [[MOC - Deployment]] - デプロイメントエラー

---

**最終更新**: 2025-11-01
**メンテナンス**: 新しいエラーパターン発見時に更新

---

## 関連ドキュメント

- [[Home]]
- [[MOC - API Integration]]
- [[MOC - Authentication]]
- [[MOC - Google Services]]
- [[projects/automation/dify-n8n-workflow/MOC - Project Overview]]
