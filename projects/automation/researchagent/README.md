# n8n Research Agent

n8n事例を自動収集し、構造化されたMarkdown表・CSV・ピボット集計・ROI上位表を生成するリサーチエージェント。

## 特徴

- **全自動収集**: Web検索 → クロール → LLM抽出 → 出力まで完全自動化
- **20列スキーマ**: 業種・KPI・n8nノード・ROI等を体系的に抽出
- **事実ベース原則**: 本文に明記された情報のみ抽出、推定は明示
- **優先ドメイン対応**: 公式サイト・コミュニティを優先的に収集
- **重複排除**: 組織/製品/ユースケース/出典でユニーク化
- **多様な出力**: Markdown表＋CSV、ピボット集計、ROI上位20件

## 必要環境

- Node.js 18以上
- **Ollama（推奨）** - ローカルLLM実行環境
  - モデル: `gpt-oss:120b-cloud` または `gpt-oss:20b`
  - インストール: https://ollama.com/
- または OpenAI API Key（有料）

## インストール

```bash
# 依存関係インストール
npm install

# Ollamaモデルのダウンロード（推奨）
ollama pull gpt-oss:120b-cloud

# .envファイル作成
cp .env.example .env

# .envにAPI設定
# Ollama使用の場合:
# LLM_PROVIDER=ollama
# OLLAMA_MODEL=gpt-oss:120b-cloud
# OLLAMA_API_URL=http://localhost:11434

# OpenAI使用の場合（有料）:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your_api_key_here
```

### Ollama vs OpenAI 比較

| 項目 | Ollama（推奨） | OpenAI |
|------|---------------|--------|
| **コスト** | 無料（ローカル実行） | 有料（APIコール課金） |
| **プライバシー** | 完全ローカル処理 | 外部送信 |
| **速度** | ローカル環境依存 | 安定高速 |
| **モデル** | gpt-oss:120b-cloud (120B) | gpt-4o等 |
| **推奨用途** | 開発・テスト・本番 | 高精度が必須の場合 |

## 使い方

### フェーズ1（産業横断）

```bash
npm run dev -- --phase 1 --target-rows 120 --out-prefix n8n_phase1
```

### フェーズ2（4業種特化）

```bash
npm run dev -- --phase 2 --target-rows 100 --focus realestate,hotel,restaurant,night --out-prefix n8n_phase2
```

### オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--phase` | フェーズ（1 or 2） | 1 |
| `--target-rows` | 目標件数 | 120 |
| `--focus` | フェーズ2用業種（カンマ区切り） | - |
| `--out-prefix` | 出力ファイル接頭辞 | n8n_phase1 |
| `--concurrency` | 並列処理数 | 6 |
| `--per-query` | 1クエリあたりの最大取得件数 | 20 |
| `--export-notion` | Notion にエクスポート | false |
| `--notion-database-id` | Notion データベース ID（既存DB用） | - |
| `--notion-parent-page-id` | Notion 親ページ ID（新規DB作成用） | - |

## Notion 連携（オプション）

抽出した事例データを Notion データベースに自動転記できます。

### 準備

1. Notion API トークンを取得（[Notion Developers](https://www.notion.so/my-integrations)）
2. Notion MCP が有効化されていることを確認（`claude mcp list` で確認）
3. 環境変数を設定

```bash
# .env ファイルに追加
NOTION_DATABASE_ID=your_database_id_here  # 既存DBを使う場合
# または
NOTION_PARENT_PAGE_ID=your_page_id_here   # 新規DB作成の場合
```

### 使い方

#### 既存データベースにエクスポート

```bash
npm run dev -- --phase 1 --target-rows 20 --export-notion --notion-database-id YOUR_DATABASE_ID
```

#### 新規データベースを作成してエクスポート

```bash
npm run dev -- --phase 1 --target-rows 20 --export-notion --notion-parent-page-id YOUR_PAGE_ID
```

### Notion データベーススキーマ

20列スキーマに対応した以下のプロパティが自動作成されます：

| プロパティ名 | 型 | 説明 |
|-------------|---|------|
| ID | タイトル | 3桁ゼロパディング |
| タイトル | テキスト | 事例名 |
| 業種 | セレクト | 業種分類 |
| サブ領域 | テキスト | 予約管理、在庫等 |
| 目的/KPI | テキスト | 数値目標 |
| トリガー種別 | テキスト | Webhook/Cron等 |
| 入力ソース | テキスト | SaaS/DB/ファイル |
| 出力先 | テキスト | SaaS/DB/通知 |
| 主要n8nノード | テキスト | 3-10個 |
| 外部API/連携ツール | テキスト | 固有名詞 |
| ワークフロー概要 | テキスト | 150字程度 |
| 実装難易度 | セレクト | 1-5 |
| 規模目安 | テキスト | 頻度/件数/店舗等 |
| 成果/ROI | テキスト | 定量優先 |
| 運用上のリスク/前提 | テキスト | 認証、レート制限等 |
| 地域/言語 | セレクト | JP/日本語、Global/英語等 |
| 出典URL | URL | 事例のURL |
| 情報の種類 | セレクト | 一次情報/二次情報/推定 |
| 公開日/更新日 | テキスト | YYYY-MM-DD形式 |
| 重複判定キー | テキスト | ユニークキー |

## 出力ファイル

実行後、`output/` ディレクトリに以下が生成されます：

- `{prefix}_full.md` - 50行ごとのMarkdown表＋直後CSV
- `{prefix}_full.csv` - 全件CSV
- `{prefix}_pivots.md` - ピボット集計（業種別・トリガー別・情報種別）
- `{prefix}_topROI.md` - ROI上位20件
- `{prefix}_focus.md` - フェーズ2専用（4業種のみ）
- `{prefix}_log.jsonl` - 監査ログ（JSONL形式）

## 20列スキーマ

| 列名 | 説明 |
|-----|------|
| ID | 3桁ゼロパディング（001, 002, ...） |
| タイトル | 事例名 |
| 業種 | 不動産/ホテル/飲食/ナイト/EC・小売/医療・ヘルスケア等 |
| サブ領域 | 予約管理、在庫、PMS/OTA、POS、CRM等 |
| 目的/KPI | 数値があれば含む（例: 工数50%削減） |
| トリガー種別 | Webhook/Cron/IMAP/API等（複数可、"/"区切り） |
| 入力ソース | SaaS/DB/ファイル/フォーム名 |
| 出力先 | SaaS/DB/通知/シート/BI |
| 主要n8nノード | 3-10個（例: Webhook, HTTP Request, Code, Slack） |
| 外部API/連携ツール | 固有名詞（例: Shopify, Airtable, Notion） |
| ワークフロー概要 | 150字程度 |
| 実装難易度 | 1-5（1=単純、5=複雑） |
| 規模目安 | 頻度/件数/店舗等 |
| 成果/ROI | 定量優先、なければ定性 |
| 運用上のリスク/前提 | 認証、レート制限、監視要件等 |
| 地域/言語 | JP/日本語、Global/英語等 |
| 出典URL | 事例のURL |
| 情報の種類 | 一次情報/二次情報/推定 |
| 公開日/更新日 | YYYY-MM-DD形式 |
| 重複判定キー | <組織/製品/ユースケース/出典ドメイン> |

## カスタマイズ

### 検索クエリ変更

[config/queries.json](config/queries.json) を編集：

```json
{
  "jp": ["n8n 事例", "n8n 導入事例", ...],
  "en": ["n8n case study", "n8n workflow automation", ...]
}
```

### 優先ドメイン追加

[config/domains.json](config/domains.json) を編集：

```json
{
  "priority": ["n8n.io", "community.n8n.io", "qiita.com", ...],
  "blocked": ["spam-site.com", ...],
  "primary_info_domains": ["n8n.io", "community.n8n.io", ...]
}
```

### 業種マッピング追加

[config/industry-mappings.json](config/industry-mappings.json) を編集。

## ビルド・本番実行

```bash
# TypeScriptコンパイル
npm run build

# ビルド済みJSで実行
npm start -- --phase 1 --target-rows 120 --out-prefix n8n_phase1
```

## トラブルシューティング

### 検索結果が少ない

- `--per-query` を増やす（例: 30）
- `config/queries.json` にクエリを追加
- 並列数を増やす `--concurrency 10`

### LLM抽出エラー

- `.env` の `OPENAI_API_KEY` を確認
- APIレート制限に達している場合は並列数を減らす
- モデルを変更（`.env` の `LLM_MODEL=gpt-4o` 等）

### 目標件数に達しない

- 検索クエリを増やす
- より多くのドメインを優先リストに追加
- `--per-query` を増やす

## ライセンス

MIT

## 開発者向け

### モジュール構成

- `src/modules/search.ts` - Web検索（DuckDuckGo）
- `src/modules/fetch.ts` - HTML取得・本文抽出
- `src/modules/llm-extract.ts` - LLM抽出（OpenAI）
- `src/modules/normalize.ts` - 正規化・重複排除
- `src/modules/output.ts` - Markdown/CSV/ピボット/ROI出力
- `src/cli.ts` - CLIエントリーポイント
- `src/types/schema.ts` - 型定義
- `src/utils/` - ユーティリティ（config, retry）

### 拡張ポイント

- 検索プロバイダの差し替え（DuckDuckGo → SerpAPI/Google CSE）
- LLMプロバイダの差し替え（OpenAI → Anthropic Claude）
- 出力先の追加（Notion, Airtable, BigQuery等）
- n8nワークフロー版への移植

## サポート

issue報告・PR歓迎！
