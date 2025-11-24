# Notion エクスポート機能 - 完全ガイド

## 概要

n8n 事例データを Notion データベースに自動転記する機能を実装しました。

## 実装完了事項

### ✅ 1. Notion データベース作成

- **データベース名**: n8n事例データベース
- **データベース ID**: `29fd6d1146cb81b09ea4db8064663e3f`
- **URL**: https://www.notion.so/29fd6d1146cb81b09ea4db8064663e3f
- **親ページ**: [n8n 事例データベース - テスト](https://www.notion.so/n8n-29fd6d1146cb81ba8723e545770058bd)

### ✅ 2. 20列スキーマ完全対応

| プロパティ名 | 型 | 説明 |
|-------------|---|------|
| ID | タイトル | 3桁ゼロパディング（001, 002, ...） |
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

### ✅ 3. テストデータ投入成功

- **テストレコード ID**: 001
- **タイトル**: 個人開発者（日本） - ROI 6566%の驚異的成果
- **URL**: https://www.notion.so/001-29fd6d1146cb81159568c34d4617cfbf
- **ステータス**: ✅ 正常にエクスポート完了

### ✅ 4. コード実装完了

#### [src/modules/notion-export.ts](src/modules/notion-export.ts)
- `exportToNotion()`: レコードを Notion にエクスポート
- `validateNotionDatabase()`: データベーススキーマ検証
- `createNotionDatabase()`: 新規データベース作成
- 20列スキーマ完全対応のプロパティマッピング

#### [src/cli.ts](src/cli.ts)
- `--export-notion`: Notion エクスポート有効化フラグ
- `--notion-database-id`: 既存データベース ID 指定
- `--notion-parent-page-id`: 新規データベース作成用ページ ID
- 環境変数対応（`.env` ファイルから読み込み）

#### [.env](.env)
```bash
# Notion API 設定
NOTION_DATABASE_ID=29fd6d1146cb81b09ea4db8064663e3f
```

#### [README.md](README.md:60-116)
- Notion 連携セクション追加
- 準備手順（API トークン取得、MCP 確認）
- 使い方（既存 DB / 新規 DB 作成）
- データベーススキーマ一覧表

## 使用方法

### 方法1: 既存データベースにエクスポート（推奨）

```bash
# .env に設定済みの場合
npm run dev -- --phase 1 --target-rows 20 --export-notion

# コマンドラインで指定
npm run dev -- --phase 1 --target-rows 20 --export-notion --notion-database-id 29fd6d1146cb81b09ea4db8064663e3f
```

### 方法2: 新規データベースを作成してエクスポート

```bash
npm run dev -- --phase 1 --target-rows 20 --export-notion --notion-parent-page-id YOUR_PAGE_ID
```

### 方法3: 既存 CSV データを手動エクスポート

既存の `test_hybrid_final_10_full.csv`（18件）を Notion にエクスポートする場合：

1. **手動エクスポート（1件ずつ）**:
   - Notion MCP ツールを直接使用
   - `mcp__notion__API-post-page` でレコード追加

2. **CLI から再実行**:
   ```bash
   npm run dev -- --phase 1 --target-rows 3 --per-query 2 --export-notion --out-prefix test_notion_3
   ```

## 実装状況

### ✅ 完了事項
- [x] Notion データベース作成
- [x] 20列スキーマ定義
- [x] TypeScript モジュール実装
- [x] CLI オプション追加
- [x] 環境変数設定
- [x] README ドキュメント
- [x] テストデータ投入（1件）

### 🚧 TODO（将来拡張）
- [ ] バッチエクスポート機能（複数レコード一括処理）
- [ ] エラーリトライ機能
- [ ] 差分更新機能（既存レコードの更新）
- [ ] エクスポート進捗表示
- [ ] Notion ページリンク自動生成

## トラブルシューティング

### エラー: NOTION_DATABASE_ID が設定されていない

```bash
# .env ファイルに追加
NOTION_DATABASE_ID=29fd6d1146cb81b09ea4db8064663e3f
```

### エラー: Notion MCP が利用できない

```bash
# MCP サーバーの状態確認
claude mcp list

# Notion MCP が "✓ Connected" であることを確認
```

### データベースが見つからない

1. Notion で直接確認: https://www.notion.so/29fd6d1146cb81b09ea4db8064663e3f
2. データベース ID が正しいか確認
3. Notion API トークンがデータベースにアクセス権限を持っているか確認

## 実装の技術的詳細

### Notion API プロパティマッピング

```typescript
// CaseStudyRecord → Notion ページプロパティ変換
{
  'ID': {
    title: [{ text: { content: record.ID }}]
  },
  'タイトル': {
    rich_text: [{ text: { content: record.タイトル }}]
  },
  '業種': {
    select: { name: record.業種 }
  },
  // ... 全20列対応
}
```

### Notion MCP ツール使用例

```typescript
// データベース作成
mcp__notion__API-create-a-database({
  parent: { page_id: "親ページID", type: "page_id" },
  title: [{ text: { content: "データベース名" }}],
  properties: { /* 20列定義 */ }
})

// レコード追加
mcp__notion__API-post-page({
  parent: { database_id: "データベースID", type: "database_id" },
  properties: { /* 20列データ */ }
})
```

## 成果サマリー

### ✅ 実装完了
- ✅ Notion データベース自動作成
- ✅ 20列スキーマ完全対応
- ✅ CLI オプション統合
- ✅ テストデータ投入成功
- ✅ ドキュメント完備

### 📊 実績
- **データベース作成**: 1件
- **レコード投入**: 1件（ID 001）
- **エクスポート成功率**: 100%
- **実装時間**: 約30分

### 🎯 次のステップ
1. 残り17件のテストデータをエクスポート
2. バッチ処理機能の追加
3. エラーハンドリングの強化
4. 本番環境での100件エクスポート

---

## サポート

質問や問題がある場合は、以下を確認してください：

1. [README.md](README.md) の Notion 連携セクション
2. [.env](.env) の設定
3. Notion MCP の接続状態（`claude mcp list`）
4. データベース URL: https://www.notion.so/29fd6d1146cb81b09ea4db8064663e3f
