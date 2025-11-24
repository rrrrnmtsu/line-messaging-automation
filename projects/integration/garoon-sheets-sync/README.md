---
title: "Garoon Workflow to Google Sheets Sync"
type: readme
status: active
created: "2025-10-28"
updated: "2025-10-28"
tags:
  - "project/garoon-sheets-sync"
  - "documentation/readme"
  - "integration/google"
---

# Garoon Workflow to Google Sheets Sync

このリポジトリは、Garoonのワークフロー申請データを取得し、Googleスプレッドシートへ同期するためのサンプル実装です。cybozu.com共通管理者またはワークフローアプリ管理者権限のAPIユーザーを想定しています。

## 機能概要
- Garoon REST API (`GET /g/api/v1/workflow/admin/requests`) を利用した申請データの取得
- ページング (`hasNext` / `offset`) と承認日時フィルタによる差分取得
- 添付ファイルIDの取得とダウンロードキュー連携（任意）
- 取得データの整形とGoogle Sheets APIへのUPSERT
- Google Apps Script（GAS）経由でシート上のボタンから同期を発火

## ディレクトリ構成
```
.
├── CODEX_DONE.txt
├── PROGRESS.md
├── README.md
├── requirements.txt
├── .env.example
├── gas
│   └── sync_trigger.gs
├── src
│   └── garoon_sheets_sync
│       ├── __init__.py
│       ├── cloud_function.py
│       ├── config.py
│       ├── garoon_client.py
│       ├── sheets_client.py
│       └── sync.py
└── shared
    └── results
        └── codex
            └── latest_sync.json
```

## 前提条件
1. Garoon REST APIが利用可能なドメイン
2. APIユーザー（管理者権限）またはOAuthクライアント
3. Google CloudプロジェクトとSheets API有効化、サービスアカウントまたはOAuthクライアント
4. Python 3.10以降、`pip`コマンド

## セットアップ手順（ローカル実行）
1. 仮想環境の作成（例: `python -m venv .venv`）。
2. 依存パッケージのインストール:
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. `.env.example` をコピーして `.env` を作成し、環境変数を設定:
   - `GAROON_BASE_URL` (例: `https://example.cybozu.com/g/api/v1`)
   - `GAROON_AUTH_METHOD` (`basic` / `oauth`)
   - `GAROON_USERNAME`, `GAROON_PASSWORD`（basic利用時）
   - `GAROON_OAUTH_CLIENT_ID`, `GAROON_OAUTH_CLIENT_SECRET`, `GAROON_OAUTH_REFRESH_TOKEN`（oauth利用時）
   - `GOOGLE_SERVICE_ACCOUNT_FILE` または `GOOGLE_OAUTH_TOKEN_FILE`
   - `GOOGLE_SPREADSHEET_ID`
4. Google Sheets API認証情報を `credentials/` ディレクトリなどに配置（`.gitignore` 済み）。

## 実行例
```bash
source .venv/bin/activate
python -m src.garoon_sheets_sync.sync --range-start 2025-01-01T00:00:00+09:00
```

## Google Cloud Functions / Cloud Run 連携
`src/garoon_sheets_sync/cloud_function.py` は HTTP トリガーのCloud Functions（第2世代推奨）または Cloud Run で利用可能です。

1. 必要な環境変数をデプロイ先に設定します（`.env` を使わない場合）。
   - `GAROON_BASE_URL`, `GAROON_AUTH_METHOD`, 認証情報, `GOOGLE_SPREADSHEET_ID`, `GOOGLE_SERVICE_ACCOUNT_FILE` 等
   - 認証ファイルは Secret Manager などに格納し、マウントまたは環境変数で読み込みます。
2. デプロイ例（Cloud Functions 第2世代）:
   ```bash
   gcloud functions deploy garoon-sync \
     --runtime=python310 \
     --region=asia-northeast1 \
     --entry-point=garoon_sync \
     --trigger-http \
     --allow-unauthenticated \
     --set-env-vars=GAROON_BASE_URL=...,GOOGLE_SPREADSHEET_ID=...
   ```
   ※ 認証情報ファイルを利用する場合は Cloud Storage / Secret Manager を併用してください。
3. デプロイ後に発行される HTTPS URL を控えます（例: `https://asia-northeast1-...cloudfunctions.net/garoon-sync`）。

## Google Apps Script ボタン連携
`gas/sync_trigger.gs` をスプレッドシートの Apps Script プロジェクトに貼り付けると、メニューから同期を呼び出せます。

1. スプレッドシートの拡張機能 → App Script を開き、既存コードを `sync_trigger.gs` に置き換え。
2. `Script Properties` に `SYNC_ENDPOINT_URL` を追加し、Cloud Functions / Cloud Run のエンドポイントURLを設定。
3. 初回のみ権限付与のために `triggerGaroonSync` を実行 → シートに戻るとメニューに「Garoon連携」が表示されます。
4. メニューまたはボタン（図形などに `triggerGaroonSync` を紐づけ）をクリックすると HTTP POST が走り、Python側の同期が開始されます。

## 注意事項
- API制限：1ドメインあたり同時接続100、1リクエスト最大1000件。
- 2要素認証中のユーザーは基本認証不可。OAuthまたは専用ユーザー推奨。
- 添付ファイルの同期は任意。必要に応じて `shared/results/codex/latest_sync.json` などにメタ情報を出力してください。
- Cloud Functions/Run を公開する場合は、IDトークン検証やAPI Gateway等でアクセス制限を検討してください。

## 開発メモ
- コード中のコメントは全て日本語で記述しています。
- 構成や変数名は命名規則（snake_case）に従います。
- テストは `pytest` を想定。後続タスクで追加可能です。
