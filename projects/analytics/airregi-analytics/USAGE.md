---
title: "Airレジ売上データ分析システム - 使用方法"
type: documentation
status: active
created: "2025-10-13"
updated: "2025-10-13"
tags:
  - "project/airregi-analytics"
---

# Airレジ売上データ分析システム - 使用方法

## セットアップ

### 1. Python環境構築
```bash
cd /Users/remma/airregi-analytics

# 仮想環境作成
python3 -m venv venv

# 仮想環境有効化
source venv/bin/activate

# 依存パッケージインストール
pip install -r requirements.txt
```

### 2. 環境変数設定
認証情報はすでに `config/.env` に設定済みです。

### 3. ディレクトリ準備
```bash
# .gitkeep ファイルを作成（Gitでディレクトリを追跡）
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch logs/.gitkeep
touch reports/.gitkeep
```

## 実行方法

### API接続テスト
```bash
python test_api.py
```

このスクリプトは以下を実行します：
- APIクライアントの初期化確認
- 認証情報の検証
- 各エンドポイントへの接続テスト

### 日次分析（デフォルト）
昨日の売上データを取得・分析します。

```bash
python main.py
# または
python main.py --mode daily
```

**実行内容:**
- 前日の取引データ取得
- 前日の精算データ取得
- 日次売上分析
- 商品別売上分析
- 支払方法別分析
- JSONレポート生成
- Excelレポート生成

### 週次分析
過去7日間のデータを取得します。

```bash
python main.py --mode weekly
```

### 月次サマリー
前月の売上サマリーを取得します。

```bash
python main.py --mode monthly
```

## 出力ファイル

### 生データ（data/raw/）
- `transactions_YYYYMMDD.json` - 日次取引データ
- `settlement_YYYYMMDD.json` - 精算データ
- `summary_YYYYMM.json` - 月次サマリー

### 分析結果（data/processed/）
- `summary_report_YYYYMMDD.json` - 分析サマリー

### レポート（reports/）
- `sales_report_YYYYMMDD.xlsx` - Excel形式の売上レポート
  - シート1: 日次サマリー
  - シート2: 商品別売上
  - シート3: 支払方法別

### ログ（logs/）
- `Main_YYYYMMDD.log` - メイン処理ログ
- `AirRegiAPI_YYYYMMDD.log` - API通信ログ
- `DataFetcher_YYYYMMDD.log` - データ取得ログ
- `SalesAnalyzer_YYYYMMDD.log` - 分析処理ログ

## 分析内容

### 日次サマリー
- 総売上金額
- 取引件数
- 平均客単価
- 最大・最小取引金額
- 時間帯別売上

### 商品別売上
- 商品ごとの売上金額
- 販売回数
- 平均単価
- 販売数量
- TOP10ランキング

### 支払方法別
- 支払方法ごとの金額
- 取引件数
- 構成比

## 定期実行設定（cron）

### 毎日自動実行
```bash
# crontab編集
crontab -e

# 毎日午前3時に日次分析実行
0 3 * * * cd /Users/remma/airregi-analytics && /Users/remma/airregi-analytics/venv/bin/python main.py --mode daily

# 毎週月曜日午前4時に週次分析実行
0 4 * * 1 cd /Users/remma/airregi-analytics && /Users/remma/airregi-analytics/venv/bin/python main.py --mode weekly

# 毎月1日午前5時に月次サマリー実行
0 5 1 * * cd /Users/remma/airregi-analytics && /Users/remma/airregi-analytics/venv/bin/python main.py --mode monthly
```

## トラブルシューティング

### API接続エラー
1. **認証エラー (401 Unauthorized)**
   - APIキー・トークンが正しいか確認
   - Airレジ バックオフィスで認証情報を再発行

2. **エンドポイントエラー (404 Not Found)**
   - ベースURLが正しいか確認
   - Airレジの公式ドキュメントで正しいエンドポイントを確認

3. **レート制限エラー (429 Too Many Requests)**
   - 自動的にリトライします
   - リクエスト頻度を下げる

### データが空
- 対象日にデータが存在するか確認
- 営業日・精算のタイミングを確認

### ログ確認
```bash
# 最新のログを確認
tail -f logs/Main_$(date +%Y%m%d).log
```

## カスタマイズ

### エンドポイントの追加
[src/api/client.py](src/api/client.py) に新しいメソッドを追加:

```python
def get_custom_data(self, param1, param2):
    params = {'param1': param1, 'param2': param2}
    return self.get('custom/endpoint', params=params)
```

### 分析ロジックの追加
[src/analysis/analyzer.py](src/analysis/analyzer.py) に新しい分析メソッドを追加

### レポート形式の変更
[src/analysis/analyzer.py](src/analysis/analyzer.py) の `export_to_excel` メソッドを編集

## セキュリティ注意事項

1. **認証情報の管理**
   - `.env` ファイルは絶対に公開しない
   - Gitにコミットしない（`.gitignore`で除外済み）
   - 定期的にAPIキー・トークンを更新

2. **データの取り扱い**
   - 生データには個人情報が含まれる可能性あり
   - データファイルへのアクセス制限
   - 不要なデータは定期的に削除

3. **ログの管理**
   - ログファイルに認証情報が含まれないよう注意
   - 古いログは定期的にアーカイブ・削除

## サポート

問題が発生した場合：
1. ログファイルを確認
2. Airレジのサポートページを確認
3. API仕様書を確認
