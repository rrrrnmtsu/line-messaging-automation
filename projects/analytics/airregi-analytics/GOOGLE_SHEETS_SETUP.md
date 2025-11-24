---
title: "Google Sheets連携セットアップガイド"
type: setup-guide
status: active
created: "2025-10-20"
updated: "2025-10-20"
tags:
  - "project/airregi-analytics"
  - "documentation/setup"
  - "setup/configuration"
  - "integration/google"
---

# Google Sheets連携セットアップガイド

Airレジ分析データをGoogle Sheetsに自動エクスポートする機能のセットアップ手順です。

## 目次
1. [Google Cloud Console での設定](#1-google-cloud-console-での設定)
2. [認証情報の配置](#2-認証情報の配置)
3. [使用方法](#3-使用方法)
4. [トラブルシューティング](#4-トラブルシューティング)

---

## 1. Google Cloud Console での設定

### 1.1 プロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 画面上部の「プロジェクトを選択」→「新しいプロジェクト」をクリック
3. プロジェクト名を入力（例: `airregi-analytics`）
4. 「作成」をクリック

### 1.2 APIの有効化

1. 左側メニューから「APIとサービス」→「ライブラリ」を選択
2. 以下のAPIを検索して有効化:
   - **Google Sheets API**
   - **Google Drive API**

各APIの「有効にする」ボタンをクリックしてください。

### 1.3 サービスアカウントの作成

1. 左側メニューから「APIとサービス」→「認証情報」を選択
2. 「認証情報を作成」→「サービスアカウント」を選択
3. サービスアカウントの詳細を入力:
   - **サービスアカウント名**: `airregi-sheets-sync`
   - **サービスアカウントID**: 自動生成される
   - **説明**: `Airレジ分析データのGoogle Sheets連携`
4. 「作成して続行」をクリック
5. ロールの選択（オプション）:
   - 基本的には不要ですが、必要に応じて「閲覧者」などを選択
6. 「完了」をクリック

### 1.4 認証情報（JSONキー）のダウンロード

1. 作成したサービスアカウントをクリック
2. 「キー」タブを選択
3. 「鍵を追加」→「新しい鍵を作成」をクリック
4. キーのタイプで「JSON」を選択
5. 「作成」をクリック
6. JSONファイルが自動的にダウンロードされます

**重要**: このJSONファイルは機密情報です。安全に保管してください。

---

## 2. 認証情報の配置

### 2.1 ファイルの配置

ダウンロードしたJSONファイルを以下のいずれかの場所に配置:

**推奨**: プロジェクトのconfigディレクトリ
```bash
cp ~/Downloads/[ダウンロードしたファイル名].json config/google_credentials.json
```

### 2.2 環境変数の設定（オプション）

別の場所に配置する場合は、`.env`ファイルに追加:

```bash
# config/.env に追加
GOOGLE_CREDENTIALS_PATH=/path/to/your/credentials.json
```

---

## 3. 使用方法

### 3.1 基本的な使い方

#### サマリーレポートをエクスポート

```bash
python google_sheets_sync.py --summary data/processed/summary_report_20251014.json
```

実行すると:
- 新しいスプレッドシートが自動作成される
- タイトル: `Airレジ売上分析_YYYY-MM-DD`
- 日次サマリー、商品別TOP10、支払方法別売上が整形されてエクスポートされる
- スプレッドシートのURLが表示される

#### 取引データをエクスポート

```bash
python google_sheets_sync.py --transactions data/raw/imported_transactions_20251014.json
```

### 3.2 オプション

#### スプレッドシート名を指定

```bash
python google_sheets_sync.py \
  --summary data/processed/summary_report_20251014.json \
  --title "店舗A_10月売上"
```

#### 認証情報ファイルを指定

```bash
python google_sheets_sync.py \
  --summary data/processed/summary_report_20251014.json \
  --credentials /path/to/credentials.json
```

#### スプレッドシートを他のユーザーと共有

```bash
# 単一ユーザーに共有
python google_sheets_sync.py \
  --summary data/processed/summary_report_20251014.json \
  --share manager@example.com

# 複数ユーザーに共有（カンマ区切り）
python google_sheets_sync.py \
  --summary data/processed/summary_report_20251014.json \
  --share manager@example.com,staff@example.com

# 閲覧権限のみで共有
python google_sheets_sync.py \
  --summary data/processed/summary_report_20251014.json \
  --share viewer@example.com \
  --share-role reader
```

共有権限:
- `reader`: 閲覧のみ
- `writer`: 編集可能（デフォルト）
- `owner`: オーナー権限

### 3.3 ワークフロー例

#### 1. CSVインポート → 分析 → Sheetsエクスポート

```bash
# 1. CSVをインポートして分析
python import_csv.py --file data/import/sample_transactions.csv --analyze

# 2. 生成されたサマリーをGoogle Sheetsにエクスポート
python google_sheets_sync.py --summary data/processed/summary_report_20251014.json
```

#### 2. 定期的な自動エクスポート（例: 毎日）

シェルスクリプトを作成:

```bash
#!/bin/bash
# daily_sync.sh

# 最新のサマリーファイルを取得
LATEST_SUMMARY=$(ls -t data/processed/summary_report_*.json | head -1)

# Google Sheetsにエクスポート
python google_sheets_sync.py \
  --summary "$LATEST_SUMMARY" \
  --share manager@example.com
```

実行権限を付与:
```bash
chmod +x daily_sync.sh
```

---

## 4. トラブルシューティング

### 4.1 認証情報ファイルが見つからない

**エラー**: `Google認証情報ファイルが見つかりません`

**解決策**:
1. JSONファイルが正しい場所にあるか確認
   ```bash
   ls -l config/google_credentials.json
   ```
2. ファイルパスを明示的に指定
   ```bash
   python google_sheets_sync.py \
     --summary data/processed/summary_report_20251014.json \
     --credentials /path/to/your/credentials.json
   ```

### 4.2 権限エラー

**エラー**: `Permission denied` または `Insufficient permissions`

**解決策**:
1. Google Sheets API と Google Drive API が有効になっているか確認
2. サービスアカウントのJSONファイルが正しいか確認
3. 既存のスプレッドシートにアクセスする場合、サービスアカウントのメールアドレス（JSONファイル内の`client_email`）をスプレッドシートに共有

### 4.3 スプレッドシートが見つからない

**エラー**: `SpreadsheetNotFound`

**原因**: 指定した名前のスプレッドシートが存在しない、またはアクセス権限がない

**解決策**:
1. `--title` を指定せずに新規作成させる
2. 既存のスプレッドシートを使う場合、サービスアカウントに共有権限を付与

### 4.4 依存関係のインストールエラー

**エラー**: `ModuleNotFoundError: No module named 'gspread'`

**解決策**:
```bash
source venv/bin/activate
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client gspread
```

### 4.5 サービスアカウントのメールアドレスを確認

JSONファイルから確認:
```bash
cat config/google_credentials.json | grep client_email
```

または:
```python
import json
with open('config/google_credentials.json') as f:
    data = json.load(f)
    print(data['client_email'])
```

このメールアドレスを使って、既存のスプレッドシートに共有権限を付与できます。

---

## 5. 高度な使い方

### 5.1 Pythonコードから直接使用

```python
from src.integrations.google_sheets import export_summary_to_sheets

# サマリーをエクスポート
url = export_summary_to_sheets(
    summary_file='data/processed/summary_report_20251014.json',
    spreadsheet_title='店舗A_10月売上',
    credentials_path='config/google_credentials.json'
)

print(f"エクスポート完了: {url}")
```

### 5.2 既存のスプレッドシートを更新

```python
from src.integrations.google_sheets import GoogleSheetsClient

# クライアント初期化
client = GoogleSheetsClient('config/google_credentials.json')

# 既存のスプレッドシートを開く（存在しない場合は作成）
spreadsheet = client.create_or_get_spreadsheet('店舗A_売上データ')

# サマリーをエクスポート
import json
with open('data/processed/summary_report_20251014.json') as f:
    summary_data = json.load(f)

url = client.export_daily_summary('店舗A_売上データ', summary_data)
print(f"更新完了: {url}")
```

---

## 6. セキュリティのベストプラクティス

1. **認証情報の保護**
   - JSONファイルをGitにコミットしない（`.gitignore`に追加済み）
   - 本番環境では環境変数や専用の秘密管理サービスを使用

2. **最小権限の原則**
   - サービスアカウントには必要最小限の権限のみ付与
   - 不要になったサービスアカウントは無効化または削除

3. **定期的なローテーション**
   - 認証情報は定期的に更新
   - 古いキーは削除

4. **アクセスログの確認**
   - Google Cloud Console でAPI使用状況を定期的に確認

---

## 7. 参考リンク

- [Google Sheets API ドキュメント](https://developers.google.com/sheets/api)
- [Google Drive API ドキュメント](https://developers.google.com/drive/api)
- [gspread ライブラリドキュメント](https://docs.gspread.org/)
- [Google Cloud Console](https://console.cloud.google.com/)

---

## サポート

問題が解決しない場合は、ログファイルを確認してください:
```bash
tail -f logs/airregi_analytics.log
```
