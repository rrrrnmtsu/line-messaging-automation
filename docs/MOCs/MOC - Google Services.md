---
title: "MOC - Google Services"
type: moc
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "navigation/moc"
  - "integration/google"
---

# MOC - Google Services

**カテゴリ**: クロスプロジェクトMOC
**対象**: Google API統合・認証パターン
**関連プロジェクト**: Airregi Analytics, Dify n8n Workflow, Garoon Sheets Sync

---

## 概要

複数のプロジェクトで使用するGoogle Services（Google Sheets API, OAuth 2.0, Google Apps Script）の統合設定・認証パターン・ベストプラクティスを集約したMOC。

**対象サービス**:
- Google Sheets API
- Google Drive API
- Google Apps Script
- Google OAuth 2.0

---

## プロジェクト別使用状況

### Airregi Analytics
- **使用サービス**: Google Sheets API, Google Drive API
- **認証方式**: サービスアカウント（OAuth 2.0）
- **目的**: 売上データのエクスポート・共有
- **ドキュメント**: [[GOOGLE_SHEETS_SETUP|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]]

### Dify n8n Workflow
- **使用サービス**: Google Sheets API
- **認証方式**: OAuth 2.0（n8n統合）
- **目的**: 売上日報データの自動書き込み
- **ドキュメント**:
  - [[google-sheets-setup|projects/automation/dify-n8n-workflow/docs/google-sheets-setup]]
  - [[GOOGLE-OAUTH-SETUP|projects/automation/dify-n8n-workflow/n8n/GOOGLE-OAUTH-SETUP]]
  - [[UPDATE-GOOGLE-SHEETS-PRO-SETUP|projects/automation/dify-n8n-workflow/n8n/UPDATE-GOOGLE-SHEETS-PRO-SETUP]]

### Garoon Sheets Sync
- **使用サービス**: Google Apps Script, Google Sheets API
- **認証方式**: Google Apps Script内部認証
- **目的**: Garoonデータの自動転記
- **ドキュメント**: [[README|projects/integration/garoon-sheets-sync/README]]

---

## Google Sheets API

### セットアップ手順（共通）

#### 1. Google Cloud Project作成
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成
3. プロジェクト名を設定（例: `airregi-analytics-project`）

#### 2. APIの有効化
1. 「APIとサービス」→「ライブラリ」
2. 以下のAPIを有効化:
   - **Google Sheets API**
   - **Google Drive API**（共有機能を使う場合）

#### 3. 認証情報の作成
2つの認証パターンがあります:

##### パターンA: サービスアカウント（自動化向け）
```
1. 「認証情報」→「認証情報を作成」→「サービスアカウント」
2. サービスアカウント名・説明を入力
3. 役割: 「編集者」または「閲覧者」
4. 「完了」→サービスアカウント詳細画面
5. 「キー」タブ→「鍵を追加」→「JSON」
6. JSONファイルをダウンロード→プロジェクトの`config/google_credentials.json`に保存
```

**使用プロジェクト**: [[MOC - Airregi Analytics]]

##### パターンB: OAuth 2.0クライアント（ユーザー認証向け）
```
1. 「認証情報」→「認証情報を作成」→「OAuth 2.0クライアントID」
2. アプリケーションの種類: 「ウェブアプリケーション」
3. 承認済みのリダイレクトURI: n8nのコールバックURLを追加
4. クライアントIDとクライアントシークレットを取得
5. n8n Credentialsに設定
```

**使用プロジェクト**: [[MOC - Dify n8n Workflow]]

---

## OAuth 2.0 認証

### 認証フロー

#### サービスアカウント認証（Python例）
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 認証情報の読み込み
credentials = service_account.Credentials.from_service_account_file(
    'config/google_credentials.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Google Sheets APIクライアント作成
service = build('sheets', 'v4', credentials=credentials)
```

#### OAuth 2.0フロー（n8n）
```
1. n8nでGoogle Sheets Credentialを作成
2. OAuth2認証タイプを選択
3. Google Cloud ConsoleのクライアントID・シークレットを入力
4. 「Connect my account」をクリック
5. Googleアカウントでログイン・権限承認
6. n8nにトークンが保存される
```

**詳細**: [[GOOGLE-OAUTH-SETUP|projects/automation/dify-n8n-workflow/n8n/GOOGLE-OAUTH-SETUP]]

---

## Google Sheets データ操作

### 基本操作パターン

#### データ書き込み（Python）
```python
# 値を書き込む
sheet_range = 'Sheet1!A1:C3'
values = [
    ['Name', 'Age', 'City'],
    ['Alice', 30, 'Tokyo'],
    ['Bob', 25, 'Osaka']
]

body = {'values': values}
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=sheet_range,
    valueInputOption='RAW',
    body=body
).execute()
```

#### データ読み込み（Python）
```python
result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range='Sheet1!A1:C10'
).execute()

values = result.get('values', [])
```

---

### 高度な操作（n8n Google Sheets Pro）

#### UPSERT操作
既存データを更新、存在しない場合は挿入

**設定**: [[UPDATE-GOOGLE-SHEETS-PRO-SETUP|projects/automation/dify-n8n-workflow/n8n/UPDATE-GOOGLE-SHEETS-PRO-SETUP]]

```
Operation: Upsert
Column to Match On: A (例: 取引ID)
```

#### 並列書き込み
複数シートへの同時書き込み

**ワークフロー**:
```
Split Node
  ├→ Google Sheets Pro (基本データ)
  ├→ Google Sheets Pro (決済方法データ)
  ├→ Google Sheets Pro (VIPリスト)
  └→ Merge
```

---

## Google Apps Script

### セットアップ

#### スクリプト作成
1. Google Sheetsを開く
2. 「拡張機能」→「Apps Script」
3. スクリプトエディタでコードを記述

#### トリガー設定
1. スクリプトエディタで「トリガー」をクリック
2. 「トリガーを追加」
3. 実行する関数、イベントソース（時間主導等）を選択

#### API有効化（GAS内から外部API呼び出し時）
```javascript
// Advanced Google Servicesを有効化
// スクリプトエディタ: サービス → Google Sheets API
```

### 使用例（Garoon Sheets Sync）
```javascript
function monthlyDataTransfer() {
  // 月次データ転記処理
  // 詳細: projects/integration/garoon-sheets-sync/gas-scripts/
}
```

---

## 共有・権限管理

### サービスアカウントでの共有
```python
from googleapiclient.discovery import build

drive_service = build('drive', 'v3', credentials=credentials)

# ユーザーに編集権限を付与
permission = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': 'user@example.com'
}

drive_service.permissions().create(
    fileId=SPREADSHEET_ID,
    body=permission
).execute()
```

### OAuth 2.0での共有
n8n Google Sheetsノードでは、ログインユーザーのGoogleアカウントで自動共有

---

## トラブルシューティング

### 認証エラー

#### サービスアカウント認証エラー
**症状**: `google.auth.exceptions.DefaultCredentialsError`
**対処**:
1. `google_credentials.json`ファイルが正しい場所にあるか確認
2. JSONファイルの内容が正しいか確認
3. スコープが正しいか確認

#### OAuth 2.0トークン期限切れ（n8n）
**症状**: `401 Unauthorized`エラー
**対処**:
1. n8n Credentialsで「Reconnect」
2. Googleアカウントで再認証
3. トークンが自動更新される

---

### API制限エラー

#### レート制限（Quota Exceeded）
**症状**: `429 Too Many Requests`
**対処**:
1. リクエスト頻度を下げる
2. バッチ処理を使用（複数行を一度に書き込み）
3. Google Cloud Consoleで割り当て上限を確認

#### 割り当て上限
- **Google Sheets API**: 1日あたり500リクエスト/ユーザー（デフォルト）
- **対処**: Google Cloud Consoleで割り当て増加をリクエスト

---

### データ書き込みエラー

#### 権限不足
**症状**: `403 Forbidden`
**対処**:
1. サービスアカウントにSpreadsheetの編集権限があるか確認
2. OAuth 2.0のスコープに`spreadsheets`が含まれているか確認

#### スプレッドシートIDエラー
**症状**: `404 Not Found`
**対処**:
1. スプレッドシートIDが正しいか確認
2. スプレッドシートが削除されていないか確認

---

## ベストプラクティス

### 認証情報管理
- サービスアカウントJSON: `.gitignore`で除外
- 環境変数: `.env`ファイルで管理
- n8n Credentials: n8n内部で暗号化保存

### パフォーマンス最適化
- バッチ処理: 複数行を一度に書き込み
- キャッシュ: 頻繁に読み込むデータはキャッシュ
- 並列処理: 独立したシートへの書き込みは並列化

### エラーハンドリング
- リトライロジック: ネットワークエラー時に自動リトライ
- ログ記録: すべてのAPI呼び出しをログに記録
- フォールバック: API障害時の代替処理

---

## スコープ一覧

### 読み取り専用
```
https://www.googleapis.com/auth/spreadsheets.readonly
https://www.googleapis.com/auth/drive.readonly
```

### 読み書き
```
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/drive
```

### Google Apps Script
```
https://www.googleapis.com/auth/script.external_request  # 外部API呼び出し
```

---

## 関連ドキュメント

### プロジェクト別
- [[GOOGLE_SHEETS_SETUP|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]]
- [[google-sheets-setup|projects/automation/dify-n8n-workflow/docs/google-sheets-setup]]
- [[GOOGLE-OAUTH-SETUP|projects/automation/dify-n8n-workflow/n8n/GOOGLE-OAUTH-SETUP]]
- [[UPDATE-GOOGLE-SHEETS-PRO-SETUP|projects/automation/dify-n8n-workflow/n8n/UPDATE-GOOGLE-SHEETS-PRO-SETUP]]
- [[README|projects/integration/garoon-sheets-sync/README]]

### 公式ドキュメント
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Google Drive API](https://developers.google.com/drive)
- [Google Apps Script](https://developers.google.com/apps-script)

---

## 関連MOC

- [[Home]] - Vaultホーム
- [[MOC - API Integration]] - API統合全般
- [[MOC - Authentication]] - 認証パターン
- [[MOC - Airregi Analytics]] - Airregi Analyticsプロジェクト
- [[MOC - Dify n8n Workflow]] - Dify n8n Workflowプロジェクト

---

**最終更新**: 2025-11-01
**メンテナンス**: プロジェクト追加時に更新

---

## 関連ドキュメント

- [[Home]]
- [[MOC - API Integration]]
- [[MOC - Authentication]]
- [[MOC - Airregi Analytics]]
- [[projects/automation/dify-n8n-workflow/MOC - Project Overview]]
