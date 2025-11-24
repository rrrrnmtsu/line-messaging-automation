---
title: "MOC - Airregi Analytics"
type: moc
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "project/airregi-analytics"
  - "navigation/moc"
---

# MOC - Airregi Analytics

**プロジェクト**: Airレジ売上データ分析システム
**目的**: Airレジの売上データをローカルで取得・分析し、Google Sheetsにエクスポート
**ステータス**: アクティブ

---

## 概要

AirレジからエクスポートしたCSVデータを分析し、日次・月次集計、商品別売上、支払方法別分析を行い、Google Sheetsに自動エクスポートするシステム。

**主要機能**:
- CSVインポート・データ分析
- JSON/Excel形式レポート生成
- Google Sheets自動連携
- Webhook統合（将来的な自動化）

---

## クイックスタート

### 基本情報
- [[README|projects/analytics/airregi-analytics/README]] - プロジェクト全体概要
- [[USAGE|projects/analytics/airregi-analytics/USAGE]] - 使用方法詳細

### セットアップ
1. [[GOOGLE_SHEETS_SETUP|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]] - Google Sheets連携設定（15分）
2. [[WEBHOOK_SETUP|projects/analytics/airregi-analytics/WEBHOOK_SETUP]] - Webhook設定

---

## 主要ドキュメント

### セットアップ・設定
| ドキュメント | 目的 | 所要時間 |
|------------|------|---------|
| [[GOOGLE_SHEETS_SETUP\|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]] | Google Sheets API認証設定 | 15分 |
| [[WEBHOOK_SETUP\|projects/analytics/airregi-analytics/WEBHOOK_SETUP]] | Webhook統合設定 | 10分 |

### API仕様
| ドキュメント | 内容 |
|------------|------|
| [[API_SPECIFICATION\|projects/analytics/airregi-analytics/API_SPECIFICATION]] | API仕様定義 |

### プロジェクトステータス
- [[FINAL_STATUS|projects/analytics/airregi-analytics/FINAL_STATUS]] - 最終ステータスレポート
- [[PROJECT_SUMMARY|projects/analytics/airregi-analytics/PROJECT_SUMMARY]] - プロジェクトサマリー

---

## プロジェクト構造

```
projects/analytics/airregi-analytics/
├── config/
│   ├── .env                      # 環境変数
│   └── google_credentials.json  # Google API認証情報
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
└── logs/                         # ログファイル
```

---

## 主要スクリプト

### データ処理
```bash
# CSVインポート・分析
python import_csv.py --file data/import/airregi_export.csv --analyze

# Google Sheets同期
python google_sheets_sync.py --summary data/processed/summary_report_20251014.json

# サンプルデータ生成
python create_sample_csv.py
```

---

## 技術スタック

### 言語・フレームワーク
- **Python 3.x**
- **pandas**: データ分析
- **openpyxl**: Excelレポート生成

### 外部サービス連携
- **Google Sheets API**: データエクスポート
- **Google Drive API**: ファイル共有

### 認証
- **OAuth 2.0**: Google Services認証
- **サービスアカウント**: 自動化シナリオ用

---

## データフロー

```
Airレジ
  ↓ (CSVエクスポート)
CSVファイル
  ↓ (import_csv.py)
JSONデータ (data/raw/)
  ↓ (analyzer.py)
分析結果 (data/processed/)
  ↓ (google_sheets_sync.py)
Google Sheets
```

---

## 分析項目

### 日次サマリー
- 総売上金額
- 取引件数
- 平均客単価
- 最大/最小取引金額

### 商品別TOP10
- 売上金額順ランキング
- 販売数量

### 支払方法別売上
- 現金
- クレジットカード
- 電子マネー
- QRコード決済

---

## Google Sheets連携

### セットアップ手順
1. [[GOOGLE_SHEETS_SETUP|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]]を参照
2. Google Cloud Consoleでプロジェクト作成
3. Google Sheets API / Drive API有効化
4. サービスアカウント作成
5. 認証情報JSONを`config/google_credentials.json`に保存

### データエクスポート
```bash
# サマリーレポートのエクスポート
python google_sheets_sync.py --summary data/processed/summary_report_20251014.json

# 取引データのエクスポート
python google_sheets_sync.py --transactions data/raw/imported_transactions_20251014.json

# 共有設定
python google_sheets_sync.py \
  --summary data/processed/summary_report_20251014.json \
  --share manager@example.com
```

---

## Webhook統合

### 概要
将来的な自動化のためのWebhook受信機能。現在は手動トリガーのみ。

### 設定
- [[WEBHOOK_SETUP|projects/analytics/airregi-analytics/WEBHOOK_SETUP]]を参照
- 環境変数: `WEBHOOK_PORT=8080`

---

## トラブルシューティング

### CSVインポートエラー
**症状**: CSVファイルの読み込みエラー
**原因**: エンコーディング問題、ヘッダー不一致
**対処**:
1. CSVファイルがUTF-8エンコードか確認
2. ヘッダー行がAirレジフォーマットと一致しているか確認

### Google Sheets連携エラー
**症状**: 認証エラー、APIアクセスエラー
**対処**:
1. `config/google_credentials.json`が正しい場所にあるか確認
2. Google Sheets API / Google Drive APIが有効か確認
3. [[GOOGLE_SHEETS_SETUP|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]]のトラブルシューティングセクション参照

### ログ確認
```bash
tail -f logs/airregi_analytics.log
```

---

## セキュリティ

### 認証情報管理
- `config/google_credentials.json`は`.gitignore`で除外
- `.env`ファイルも`.gitignore`で除外
- 認証情報は絶対に公開しない

### データ取り扱い
- データファイルには個人情報が含まれる可能性あり
- ローカルのみで処理、外部サーバーには送信しない
- 必要に応じてデータの匿名化を検討

---

## 関連MOC

- [[Home]] - Vaultホーム
- [[MOC - Google Services]] - Google API統合全般
- [[MOC - API Integration]] - API統合パターン
- [[MOC - Deployment]] - デプロイメント手法

---

## 次のステップ

### 機能拡張
- [ ] リアルタイムWebhook統合
- [ ] 自動レポート生成（スケジュール実行）
- [ ] ダッシュボード機能追加
- [ ] 複数店舗対応

### 最適化
- [ ] データ処理の高速化
- [ ] エラーハンドリング強化
- [ ] ログレベルの調整

---

**最終更新**: 2025-11-01
**メンテナンス**: 月次レビュー推奨

---

## 関連ドキュメント

- [[Home]]
- [[MOC - Google Services]]
- [[MOC - API Integration]]
- [[README|projects/analytics/airregi-analytics/README]]
- [[GOOGLE_SHEETS_SETUP|projects/analytics/airregi-analytics/GOOGLE_SHEETS_SETUP]]
- [[API_SPECIFICATION|projects/analytics/airregi-analytics/API_SPECIFICATION]]
