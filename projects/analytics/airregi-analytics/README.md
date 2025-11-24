---
title: "Airレジ 売上データ分析システム"
type: readme
status: active
created: "2025-10-14"
updated: "2025-10-14"
tags:
  - "project/airregi-analytics"
  - "documentation/readme"
---

# Airレジ 売上データ分析システム

## 概要
Airレジの売上データをローカルで取得・分析し、Google Sheetsにエクスポートするワークフローシステム

## 主要機能
- **CSVインポート**: AirレジエクスポートデータのCSVファイルを読み込み
- **データ分析**: 日次・月次集計、商品別売上、支払方法別分析
- **レポート生成**: JSON形式およびExcel形式でのレポート出力
- **Google Sheets連携**: 分析結果を自動的にGoogle Sheetsにエクスポート

## プロジェクト構造
```
airregi-analytics/
├── config/
│   ├── .env                      # 環境変数（要作成）
│   └── google_credentials.json  # Google API認証情報（要作成）
├── src/
│   ├── analysis/
│   │   └── analyzer.py           # 売上分析エンジン
│   ├── integrations/
│   │   └── google_sheets.py      # Google Sheets連携
│   └── utils/
│       └── logger.py             # ログ管理
├── data/
│   ├── import/                   # CSVインポート元
│   ├── raw/                      # 生データ（JSON）
│   └── processed/                # 分析結果（JSON）
├── reports/                      # レポート（Excel）
├── logs/                         # ログファイル
├── import_csv.py                 # CSVインポートスクリプト
├── google_sheets_sync.py         # Google Sheets同期スクリプト
├── create_sample_csv.py          # サンプルデータ生成
├── requirements.txt              # Python依存関係
├── README.md                     # 本ファイル
├── GOOGLE_SHEETS_SETUP.md        # Google Sheets連携設定ガイド
└── USAGE.md                      # 使用方法詳細
```

## クイックスタート

### 1. 環境構築
```bash
# リポジトリをクローンまたはダウンロード
cd airregi-analytics

# 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. サンプルデータで試す
```bash
# サンプルCSVファイルを生成
python create_sample_csv.py

# CSVをインポートして分析
python import_csv.py --file data/import/sample_transactions.csv --analyze
```

これで以下のファイルが生成されます:
- `data/raw/imported_transactions_YYYYMMDD_HHMMSS.json` - インポートされた取引データ
- `data/processed/summary_report_YYYYMMDD.json` - 分析サマリー
- `reports/sales_report_YYYYMMDD.xlsx` - Excelレポート

### 3. Google Sheets連携（オプション）

詳細は [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) を参照してください。

**簡易手順**:
1. Google Cloud Consoleでサービスアカウントを作成
2. 認証情報JSONを `config/google_credentials.json` に保存
3. 分析結果をエクスポート:
   ```bash
   python google_sheets_sync.py --summary data/processed/summary_report_20251014.json
   ```

## 使用方法

### CSVインポート

AirレジからエクスポートしたCSVファイルをインポート:

```bash
python import_csv.py --file /path/to/airregi_export.csv --analyze
```

オプション:
- `--file`: CSVファイルのパス（必須）
- `--analyze`: インポート後に自動分析を実行
- `--type`: データタイプ（`transactions` または `settlement`、デフォルト: `transactions`）

### Google Sheetsエクスポート

分析結果をGoogle Sheetsにエクスポート:

```bash
# サマリーレポートをエクスポート
python google_sheets_sync.py --summary data/processed/summary_report_20251014.json

# 取引データをエクスポート
python google_sheets_sync.py --transactions data/raw/imported_transactions_20251014.json

# 他のユーザーと共有
python google_sheets_sync.py \
  --summary data/processed/summary_report_20251014.json \
  --share manager@example.com
```

詳細は [USAGE.md](USAGE.md) を参照してください。

## 設定ファイル

### `config/.env`
環境変数を設定（現在は主にWebhook用）:
```bash
WEBHOOK_PORT=8080
```

### `config/google_credentials.json`
Google Sheets API認証情報（サービスアカウントのJSONキー）

詳細は [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) を参照。

## 分析項目

生成されるレポートには以下の項目が含まれます:

- **日次サマリー**: 総売上金額、取引件数、平均客単価、最大/最小取引金額
- **商品別TOP10**: 売上金額順のランキング、販売数量
- **支払方法別売上**: 現金、クレジットカード、電子マネー、QRコード決済などの内訳

## トラブルシューティング

### CSVインポートエラー
- CSVファイルのエンコーディングを確認（UTF-8推奨）
- ヘッダー行が正しいフォーマットか確認

### Google Sheets連携エラー
- 認証情報ファイルが正しい場所にあるか確認
- Google Sheets API / Google Drive API が有効になっているか確認
- 詳細は [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) のトラブルシューティングセクション参照

### ログ確認
```bash
tail -f logs/airregi_analytics.log
```

## 注意事項
- 認証情報（`config/google_credentials.json`）は絶対に公開しない
- `.gitignore`に認証情報ファイルが含まれていることを確認
- データファイルには個人情報が含まれる可能性があるため取り扱いに注意

---

## 関連ドキュメント

### セットアップ・設定
- [[GOOGLE_SHEETS_SETUP]]
- [[SETUP_COMPLETE]]
- [[WEBHOOK_SETUP]]

