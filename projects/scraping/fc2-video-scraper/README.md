---
title: "FC2動画スクレイピングツール"
type: readme
status: active
created: "2025-10-08"
updated: "2025-10-08"
tags:
  - "project/fc2-video-scraper"
  - "documentation/readme"
---

# FC2動画スクレイピングツール

FC2サイト内で指定ワードを検索し、動画URLとサムネイル画像をCSVで一覧化するツールです。

## ⚠️ 重要なお知らせ

**FC2動画は強力なボット検出システムを実装しています。** Seleniumを使った自動スクレイピングはほぼ確実にブロックされます。

### 推奨される使用方法

✅ **HTMLパーサー方式（推奨・成功率100%）**
1. ブラウザで手動検索・ページ保存
2. `html_parser.py` でHTML解析
3. CSV出力

❌ **Seleniumスクレイパー（非推奨・成功率0%）**
- FC2のボット検出で即座にブロックされます

詳細は [USAGE.md](USAGE.md) を参照してください。

## 機能

### 1. HTMLパーサー（`html_parser.py`）★推奨★
- 手動ダウンロードしたHTMLファイルから動画情報を抽出
- **確実にデータ取得可能**
- ボット検出を回避
- 使用方法:
  ```bash
  python html_parser.py fc2_search_result.html
  ```

### 2. Seleniumスクレイパー（`scraper.py`, `scraper_advanced.py`）
- 自動スクレイピング（**成功率: ほぼ0%**）
- FC2のボット検出でブロックされる
- 参考実装として残存

## 必要要件

- Python 3.8以上
- BeautifulSoup4, lxml（HTMLパーサー用）
- Google Chrome（Seleniumスクレイパー使用時のみ）

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd fc2-video-scraper
```

### 2. 仮想環境の作成（推奨）

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

## 使い方（推奨: HTMLパーサー）

### ステップ1: ブラウザでHTMLを保存

1. ブラウザで https://video.fc2.com/a/ にアクセス
2. 「素人」などのキーワードで検索
3. 検索結果ページを表示
4. 右クリック → 「名前を付けてページを保存」
5. 「ウェブページ、完全」を選択
6. ファイル名: `fc2_search_result.html`

### ステップ2: HTMLパーサーで解析

```bash
# 基本的な使い方
python html_parser.py fc2_search_result.html

# 出力先を指定
python html_parser.py fc2_search_result.html output/custom_output.csv
```

### 複数ページの処理

```bash
# 各ページを個別に保存・解析
python html_parser.py page1.html output/page1.csv
python html_parser.py page2.html output/page2.csv
python html_parser.py page3.html output/page3.csv
```

## 出力ファイル

CSVファイルは以下の形式で出力されます：

```
output/fc2_videos_<タイムスタンプ>.csv
```

### CSV構造

| カラム | 内容 |
|--------|------|
| No | 連番 |
| Title | 動画タイトル |
| URL | 動画URL |
| Thumbnail | サムネイル画像URL |
| Parsed_At / Scraped_At | 取得日時 |

## Seleniumスクレイパー（参考・非推奨）

### 環境変数の設定

`.env.example` を `.env` にコピーして編集：

```bash
cp .env.example .env
```

`.env` ファイルの設定例：

```env
# FC2 検索設定
SEARCH_KEYWORD=検索したいワード
MAX_PAGES=3
OUTPUT_DIR=output

# ブラウザ設定
HEADLESS=False
BROWSER_TIMEOUT=30
```

### 実行（成功率は非常に低い）

```bash
# 基本版
python scraper.py

# 高度版（ボット検出回避機能付き）
python scraper_advanced.py
```

**注意**: ほぼ確実に「ページが見つかりません」エラーになります。

## トラブルシューティング

### HTMLパーサーで動画が見つからない

**原因**: JavaScriptで動的に読み込まれるコンテンツ

**解決策**:
1. ブラウザでページを完全に読み込み（スクロールして全コンテンツ表示）
2. 「名前を付けてページを保存」→「ウェブページ、完全」を選択
3. 再度HTMLパーサーを実行

### Seleniumスクレイパーがエラーページに飛ばされる

**原因**: FC2のボット検出システム

**解決策**: **HTMLパーサー方式を使用してください**（自動化は現状困難）

### ChromeDriverエラー
```bash
# ChromeDriverを手動で更新
pip install --upgrade webdriver-manager
```

## 注意事項

### 法的・倫理的注意
- **利用規約の遵守**: FC2の利用規約を確認し、違反しないようご注意ください
- **スクレイピング頻度**: サーバーに過度な負荷をかけないよう注意
- **個人利用推奨**: 商用利用や大規模スクレイピングは避けてください
- **著作権尊重**: 取得したデータの二次利用には十分注意してください

### 技術的注意
- HTMLパーサー方式が最も確実で安全です
- Seleniumスクレイパーは参考実装として提供しています
- FC2の仕様変更により動作しなくなる可能性があります

## ファイル構成

```
fc2-video-scraper/
├── html_parser.py          # ★推奨★ HTMLパーサー
├── scraper.py              # Seleniumスクレイパー（基本版）
├── scraper_advanced.py     # Seleniumスクレイパー（高度版）
├── requirements.txt        # 依存パッケージ
├── .env.example            # 環境変数テンプレート
├── README.md               # このファイル
└── USAGE.md                # 詳細な使用方法
```

## ライセンス

このツールは教育・研究目的で提供されています。使用は自己責任でお願いします。

## 免責事項

- 本ツールの使用による一切の損害について、作成者は責任を負いません
- FC2の仕様変更により動作しなくなる可能性があります
- スクレイピング行為は各サイトの利用規約を遵守してください
