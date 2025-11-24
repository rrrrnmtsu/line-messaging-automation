---
title: "MOC - Authentication"
type: moc
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "navigation/moc"
  - "integration/authentication"
---

# MOC - Authentication

**カテゴリ**: クロスプロジェクトMOC
**対象**: 認証・セキュリティ実装パターン
**適用範囲**: 全プロジェクト

---

## 概要

複数のプロジェクトで使用する認証方式・セキュリティパターンを集約したMOC。API認証、OAuth 2.0、APIキー管理、セキュリティベストプラクティスを包括的にカバー。

---

## 認証パターン一覧

### 1. OAuth 2.0
**使用プロジェクト**: [[MOC - Airregi Analytics]], [[MOC - Dify n8n Workflow]]
**対象サービス**: Google APIs

#### 認証フロー
```
1. クライアントIDとシークレットを取得（Google Cloud Console）
2. 認証URLにリダイレクト
3. ユーザーが権限承認
4. 認証コードを取得
5. アクセストークンと交換
6. APIリクエストにトークンを添付
```

#### 実装例（n8n）
- [[GOOGLE-OAUTH-SETUP|projects/automation/dify-n8n-workflow/n8n/GOOGLE-OAUTH-SETUP]]

#### セキュリティ考慮事項
- リフレッシュトークンの安全な保存
- トークン期限切れ時の自動更新
- スコープの最小権限原則

---

### 2. API Key認証
**使用プロジェクト**: [[MOC - LINE Chat Logger]], [[MOC - Dify n8n Workflow]]
**対象サービス**: LINE Messaging API, Telegram Bot API, SerpStack

#### 実装パターン

##### HTTPヘッダー方式
```javascript
// SerpStack API
{
  "headers": {
    "apikey": "{{ $credentials.apiKey }}"
  }
}
```

##### URLパラメータ方式
```javascript
// 一部のAPI
https://api.example.com/endpoint?api_key=YOUR_API_KEY
```

#### セキュリティ考慮事項
- APIキーは環境変数で管理（`.env`ファイル）
- `.gitignore`で除外
- 定期的なローテーション
- 本番環境とテスト環境で別のキーを使用

---

### 3. Bearer Token認証
**使用プロジェクト**: [[MOC - Dify n8n Workflow]]
**対象サービス**: Anthropic Claude API, OpenAI API

#### 実装パターン
```javascript
// HTTPリクエストヘッダー
{
  "headers": {
    "Authorization": "Bearer {{ $credentials.apiKey }}",
    "anthropic-version": "2023-06-01"  // Claude専用
  }
}
```

#### セキュリティ考慮事項
- トークンは絶対にログに出力しない
- HTTPS通信必須
- トークン漏洩時の即座な無効化

---

### 4. Basic認証
**使用プロジェクト**: [[MOC - Dify n8n Workflow]]
**対象サービス**: DataForSEO API, n8n管理画面

#### 実装パターン
```javascript
// Base64エンコード
const credentials = Buffer.from('email:password').toString('base64');
Authorization: Basic ${credentials}
```

#### n8nでの設定
```javascript
// n8n Credentials
Type: Basic Auth
Username: your_email@example.com
Password: your_password
```

#### セキュリティ考慮事項
- 必ずHTTPS通信で使用
- パスワードは複雑なものを設定
- 認証情報は環境変数で管理

---

### 5. Webhook署名検証
**使用プロジェクト**: [[MOC - LINE Chat Logger]], [[MOC - Airregi Analytics]]
**対象サービス**: LINE Messaging API, Telegram Bot API

#### LINEの署名検証
```javascript
const crypto = require('crypto');

function validateSignature(body, signature, channelSecret) {
  const hash = crypto
    .createHmac('SHA256', channelSecret)
    .update(JSON.stringify(body))
    .digest('base64');

  return hash === signature;
}
```

#### セキュリティ考慮事項
- すべてのWebhookリクエストで署名検証を実施
- 検証失敗時は即座にリクエストを拒否
- タイムスタンプ検証（リプレイアタック対策）

---

## プロジェクト別認証マップ

### Airregi Analytics
| サービス | 認証方式 | ドキュメント |
|---------|---------|-------------|
| Google Sheets API | OAuth 2.0 (サービスアカウント) | [[GOOGLE_SHEETS_SETUP\|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]] |
| Google Drive API | OAuth 2.0 (サービスアカウント) | [[GOOGLE_SHEETS_SETUP\|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]] |

### Dify n8n Workflow
| サービス | 認証方式 | ドキュメント |
|---------|---------|-------------|
| Google Sheets API | OAuth 2.0 | [[GOOGLE-OAUTH-SETUP\|projects/automation/dify-n8n-workflow/n8n/GOOGLE-OAUTH-SETUP]] |
| Claude Vision API | Bearer Token | [[ai-direct-integration-guide\|projects/automation/dify-n8n-workflow/docs/ai-direct-integration-guide]] |
| OpenAI API | Bearer Token | [[ai-direct-integration-guide\|projects/automation/dify-n8n-workflow/docs/ai-direct-integration-guide]] |
| DataForSEO API | Basic Auth | [[DATAFORSEO-AUTHENTICATION-GUIDE\|projects/automation/dify-n8n-workflow/n8n/DATAFORSEO-AUTHENTICATION-GUIDE]] |
| SerpStack API | API Key | [[SERPSTACK-API-SETUP\|projects/automation/dify-n8n-workflow/n8n/SERPSTACK-API-SETUP]] |
| Telegram Bot API | API Key | [[telegram-bot-setup\|projects/automation/dify-n8n-workflow/docs/telegram-bot-setup]] |

### LINE Chat Logger
| サービス | 認証方式 | ドキュメント |
|---------|---------|-------------|
| LINE Messaging API | API Key + Webhook署名 | [[README\|projects/communication/line-chat-logger/README]] |

### Crypto Scalping
| サービス | 認証方式 | ドキュメント |
|---------|---------|-------------|
| Bybit API | API Key + Secret | [[README\|projects/finance/crypto-scalping/README]] |

---

## 環境変数管理

### .envファイル構造

#### Airregi Analytics
```env
# config/.env
GOOGLE_CREDENTIALS_PATH=config/google_credentials.json
WEBHOOK_PORT=8080
```

#### Dify n8n Workflow
```env
# .env
DIFY_SECRET_KEY=your-secret-key-32-chars-minimum
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin_password_changeme
POSTGRES_PASSWORD=your_postgres_password

GOOGLE_SHEET_ID=your_spreadsheet_id
TELEGRAM_BOT_TOKEN=123456:ABCdefGHI
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
```

#### LINE Chat Logger
```env
# .env
LINE_CHANNEL_SECRET=your_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_access_token
POSTGRES_URL=your_neon_postgres_url
```

---

## セキュリティベストプラクティス

### 認証情報の保護

#### 絶対にGitにコミットしない
`.gitignore`に以下を追加:
```gitignore
.env
*.key
credentials.json
google_credentials.json
config/*.json
```

#### 環境変数の暗号化
本番環境では環境変数を暗号化保存:
- Vercel: 自動暗号化
- Docker: Secrets機能
- n8n: 内部暗号化ストレージ

---

### APIキーのローテーション

#### 定期ローテーション計画
- **開発環境**: 6ヶ月ごと
- **本番環境**: 3ヶ月ごと
- **漏洩疑い時**: 即座に無効化・再発行

#### ローテーション手順
1. 新しいAPIキーを発行
2. 新キーを環境変数に追加（既存と並行稼働）
3. 新キーでテスト
4. 旧キーを削除
5. 旧キーを無効化

---

### 権限の最小化

#### OAuth 2.0スコープ
必要最小限のスコープのみ要求:
```javascript
// 読み取り専用で十分な場合
scopes: ['https://www.googleapis.com/auth/spreadsheets.readonly']

// 書き込みが必要な場合のみ
scopes: ['https://www.googleapis.com/auth/spreadsheets']
```

#### APIキー制限
Google Cloud Consoleでの制限:
- IPアドレス制限
- HTTPリファラー制限
- アプリケーション制限

---

## トラブルシューティング

### OAuth 2.0エラー

#### トークン期限切れ
**症状**: `401 Unauthorized`
**対処**:
1. リフレッシュトークンで新しいアクセストークンを取得
2. n8nの場合: Credentialsで「Reconnect」

#### スコープ不足
**症状**: `403 Forbidden`
**対処**:
1. 必要なスコープを確認
2. OAuth 2.0設定でスコープを追加
3. 再認証

---

### APIキーエラー

#### 無効なAPIキー
**症状**: `401 Unauthorized`, `403 Forbidden`
**対処**:
1. APIキーが正しいか確認
2. APIキーが有効か確認（サービス側で無効化されていないか）
3. 必要に応じて再発行

#### レート制限
**症状**: `429 Too Many Requests`
**対処**:
1. リクエスト頻度を下げる
2. エクスポネンシャルバックオフでリトライ
3. APIプランのアップグレードを検討

---

### Webhook署名検証エラー

#### 署名不一致
**症状**: 署名検証失敗
**対処**:
1. Channel Secretが正しいか確認
2. リクエストボディが改変されていないか確認
3. 署名アルゴリズムが正しいか確認（SHA256等）

---

## n8n認証設定

### Google OAuth 2.0
```
Credential Type: OAuth2
Authorization URL: https://accounts.google.com/o/oauth2/auth
Access Token URL: https://oauth2.googleapis.com/token
Scope: https://www.googleapis.com/auth/spreadsheets
Client ID: <from Google Cloud Console>
Client Secret: <from Google Cloud Console>
```

### Basic Auth（DataForSEO）
```
Credential Type: Basic Auth
Username: your_email@example.com
Password: your_password
```

### Header Auth（API Key）
```
Credential Type: Header Auth
Name: Authorization
Value: Bearer {{ $credentials.apiKey }}
```

---

## セキュリティチェックリスト

### 開発時
- [ ] `.env`ファイルを`.gitignore`に追加
- [ ] 認証情報をハードコードしない
- [ ] テスト用と本番用で別の認証情報を使用

### デプロイ時
- [ ] 環境変数が正しく設定されているか確認
- [ ] HTTPS通信の強制
- [ ] 不要な認証情報の削除

### 運用時
- [ ] APIキーの定期ローテーション
- [ ] アクセスログの監視
- [ ] 異常なAPIリクエストの検出

---

## 参考リソース

### 公式ドキュメント
- [OAuth 2.0仕様](https://oauth.net/2/)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [LINE Messaging API](https://developers.line.biz/ja/docs/messaging-api/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 関連MOC

- [[Home]] - Vaultホーム
- [[MOC - API Integration]] - API統合パターン
- [[MOC - Google Services]] - Google Services統合
- [[MOC - Deployment]] - デプロイメント・セキュリティ

---

**最終更新**: 2025-11-01
**メンテナンス**: セキュリティアップデート時に更新

---

## 関連ドキュメント

- [[Home]]
- [[MOC - API Integration]]
- [[MOC - Google Services]]
- [[MOC - Deployment]]
