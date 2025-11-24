---
title: "Airレジ売上データ分析システム - プロジェクトサマリー"
type: analysis-report
status: completed
created: "2025-10-13"
updated: "2025-10-13"
tags:
  - "project/airregi-analytics"
  - "documentation/report"
---

# Airレジ売上データ分析システム - プロジェクトサマリー

## プロジェクト概要

**目的**: Airレジ APIを使用して店舗の売上データを自動取得し、構造化された分析を実施するシステム

**構築日**: 2025年10月13日

**技術スタック**:
- Python 3.x
- requests (HTTP通信)
- pandas (データ分析)
- openpyxl (Excel出力)
- python-dotenv (環境変数管理)

---

## システム構成

### ディレクトリ構造
```
airregi-analytics/
├── config/                 # 設定ファイル
│   ├── .env               # 認証情報（機密）
│   └── .env.example       # 環境変数テンプレート
├── src/                   # ソースコード
│   ├── api/               # API通信
│   │   └── client.py      # APIクライアント
│   ├── data/              # データ処理
│   │   └── fetcher.py     # データ取得
│   ├── analysis/          # データ分析
│   │   └── analyzer.py    # 分析エンジン
│   └── utils/             # ユーティリティ
│       └── logger.py      # ログ管理
├── data/                  # データ保存
│   ├── raw/               # 生データ
│   └── processed/         # 処理済みデータ
├── reports/               # レポート出力
├── logs/                  # ログファイル
├── tests/                 # テストコード
├── main.py                # メインスクリプト
├── test_api.py            # API接続テスト
├── setup.sh               # セットアップスクリプト
└── requirements.txt       # Python依存関係
```

### 主要コンポーネント

#### 1. APIクライアント (`src/api/client.py`)
- **機能**: Airレジ APIとの通信
- **認証**: APIキー + APIトークン
- **エラーハンドリング**: 自動リトライ、レート制限対応
- **主要メソッド**:
  - `get_transactions()` - 取引データ取得
  - `get_sales_summary()` - 売上サマリー取得
  - `get_settlements()` - 精算データ取得

#### 2. データ取得 (`src/data/fetcher.py`)
- **機能**: APIからデータ取得とファイル保存
- **データ形式**: JSON
- **主要メソッド**:
  - `fetch_daily_transactions()` - 日次取引データ
  - `fetch_period_transactions()` - 期間指定取引データ
  - `fetch_monthly_summary()` - 月次サマリー

#### 3. データ分析 (`src/analysis/analyzer.py`)
- **機能**: 売上データの多角的分析
- **分析内容**:
  - 日次売上サマリー（総額、平均単価、時間帯別など）
  - 商品別売上分析（TOP10、販売数量など）
  - 支払方法別分析（構成比、件数など）
- **出力形式**: JSON、Excel

#### 4. ログ管理 (`src/utils/logger.py`)
- **機能**: 処理ログの記録
- **出力先**: ファイル + コンソール
- **ログレベル**: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

## 主要機能

### 1. データ取得機能
- 過去2ヶ月分のデータ取得対応
- 日次・週次・月次の取得モード
- 自動リトライ・エラーハンドリング

### 2. データ分析機能
- 日次売上分析
- 商品別売上ランキング
- 支払方法別分析
- 時間帯別売上分析

### 3. レポート生成機能
- JSON形式（プログラム連携用）
- Excel形式（人間可読）
- 複数シート対応

### 4. ログ・監視機能
- 全処理のログ記録
- エラートラッキング
- API通信ログ

---

## セットアップ手順

### クイックスタート
```bash
cd /Users/remma/airregi-analytics
./setup.sh
```

### 手動セットアップ
```bash
# 1. 仮想環境作成
python3 -m venv venv
source venv/bin/activate

# 2. 依存パッケージインストール
pip install -r requirements.txt

# 3. 環境変数設定確認
cat config/.env
```

---

## 使用方法

### API接続テスト
```bash
python test_api.py
```

### 日次分析実行
```bash
python main.py
# または
python main.py --mode daily
```

### 週次分析実行
```bash
python main.py --mode weekly
```

### 月次サマリー実行
```bash
python main.py --mode monthly
```

---

## 出力ファイル

### 生データ (`data/raw/`)
| ファイル | 内容 |
|---------|------|
| `transactions_YYYYMMDD.json` | 日次取引データ |
| `settlement_YYYYMMDD.json` | 精算データ |
| `summary_YYYYMM.json` | 月次サマリー |

### 分析結果 (`data/processed/`)
| ファイル | 内容 |
|---------|------|
| `summary_report_YYYYMMDD.json` | 日次分析サマリー |

### レポート (`reports/`)
| ファイル | 内容 |
|---------|------|
| `sales_report_YYYYMMDD.xlsx` | Excel形式売上レポート |

### ログ (`logs/`)
| ファイル | 内容 |
|---------|------|
| `Main_YYYYMMDD.log` | メイン処理ログ |
| `AirRegiAPI_YYYYMMDD.log` | API通信ログ |
| `DataFetcher_YYYYMMDD.log` | データ取得ログ |
| `SalesAnalyzer_YYYYMMDD.log` | 分析処理ログ |

---

## 定期実行設定

### cron設定例
```bash
# 毎日午前3時に日次分析実行
0 3 * * * cd /Users/remma/airregi-analytics && /Users/remma/airregi-analytics/venv/bin/python main.py --mode daily

# 毎週月曜日午前4時に週次分析実行
0 4 * * 1 cd /Users/remma/airregi-analytics && /Users/remma/airregi-analytics/venv/bin/python main.py --mode weekly

# 毎月1日午前5時に月次サマリー実行
0 5 1 * * cd /Users/remma/airregi-analytics && /Users/remma/airregi-analytics/venv/bin/python main.py --mode monthly
```

---

## セキュリティ対策

### 実装済み
1. **認証情報の保護**
   - `.env`ファイルで管理
   - `.gitignore`で除外
   - ログに認証情報を含めない

2. **データアクセス制御**
   - ファイルシステムのアクセス権限
   - データディレクトリの分離

3. **エラーハンドリング**
   - 例外処理の実装
   - ログへの詳細記録

### 推奨事項
1. 定期的なAPIキー・トークンの更新
2. ログファイルの定期的なアーカイブ・削除
3. データファイルへのアクセス制限
4. バックアップの実施

---

## 既知の制約

### API制限
- **データ取得範囲**: 過去2ヶ月分のみ
- **レート制限**: 詳細不明（自動リトライで対応）

### 技術的制約
- Python 3.7以上が必要
- ネットワーク接続必須
- Airレジ APIの仕様変更に依存

---

## 今後の拡張候補

### 機能拡張
1. **可視化機能**
   - グラフ・チャート生成
   - ダッシュボード構築

2. **予測分析**
   - 売上予測
   - 在庫最適化

3. **アラート機能**
   - 異常値検知
   - メール通知

4. **他システム連携**
   - Google Sheets連携
   - Slack通知
   - データベース保存

### システム改善
1. **パフォーマンス最適化**
   - 並列処理
   - キャッシング

2. **テストカバレッジ向上**
   - ユニットテスト
   - 統合テスト

3. **CI/CD導入**
   - 自動テスト
   - 自動デプロイ

---

## トラブルシューティング

### API接続エラー
1. 認証情報を確認
2. ネットワーク接続を確認
3. エンドポイントURLを確認
4. ログファイルでエラー詳細を確認

### データが取得できない
1. 対象日にデータが存在するか確認
2. 営業日・精算のタイミングを確認
3. API制限（過去2ヶ月）を確認

### 詳細は [USAGE.md](USAGE.md) を参照

---

## ドキュメント一覧

| ファイル | 内容 |
|---------|------|
| [README.md](README.md) | プロジェクト概要 |
| [USAGE.md](USAGE.md) | 使用方法詳細 |
| [API_SPECIFICATION.md](API_SPECIFICATION.md) | API仕様（推定版） |
| PROJECT_SUMMARY.md | このファイル |

---

## プロジェクト情報

**プロジェクト名**: airregi-analytics
**バージョン**: 1.0.0
**ライセンス**: 未設定
**作成者**: remma
**作成日**: 2025年10月13日

---

## 連絡先・サポート

- **Airレジサポート**: https://faq.airregi.jp/
- **技術サポート**: Airレジテクニカルサポートに問い合わせ

---

## 変更履歴

### v1.0.0 (2025-10-13)
- 初回リリース
- 基本的なデータ取得・分析機能実装
- Excel・JSONレポート生成機能実装
