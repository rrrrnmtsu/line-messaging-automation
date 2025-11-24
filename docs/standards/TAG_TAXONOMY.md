---
title: "Project Vault - Tag Taxonomy"
type: documentation
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "metadata/standards"
  - "documentation/guide"
---

# プロジェクトVault タグ分類体系

**作成日**: 2025-11-01  
**現状**: 59個のユニークタグ、306タグインスタンス  
**対象**: /Users/remma/project (125 Markdownファイル)

---

## 概要

このドキュメントは、プロジェクトVault全体で使用する**標準化されたタグ分類体系（Tag Taxonomy）**を定義します。すべてのタグは階層構造（`category/subcategory`形式）に従い、Obsidianのタグ階層機能を最大限活用します。

---

## タグ階層の原則

### 1. 階層構造の強制
- **必須**: すべてのタグは `category/subcategory` 形式
- **最大深度**: 3レベル（`category/subcategory/detail`）
- **区切り文字**: スラッシュ（`/`）のみ使用
- **命名規則**: 小文字、ハイフン区切り（`multi-word-tag`）

### 2. 一貫性の確保
- 同じ概念には同じタグを使用
- 類似タグの重複を避ける
- プロジェクト名は正規化（例: `dify-n8n-workflow`, `airregi-analytics`）

### 3. 検索性の最適化
- 意味的に明確なタグ名
- 過度に細分化しない（タグ数を管理可能に保つ）
- プロジェクトタグは必須

---

## 標準タグ階層

### 1. project/ - プロジェクト識別タグ

プロジェクトごとの識別タグ。**すべてのファイルに最低1つのプロジェクトタグを付与すること。**

```
project/
├── airregi-analytics           # Airレジ売上分析システム
├── crypto-scalping             # 暗号通貨スキャルピング
├── dify-n8n-workflow           # Telegram売上日報自動処理
├── utaiba                      # UTAIBAウェブサイトプロジェクト
├── line-chat-logger            # LINEチャットロガー
├── lineworks-chat-logger       # LINE WORKSチャットロガー
├── obsidian-sync-automation    # Obsidian同期自動化
├── codex-gas-automation        # Codex + GAS自動化
├── codex-dify-mcp-workflow     # Codex + Dify + MCP連携
├── codex-chatgpt-workflow      # Codex + ChatGPT連携
├── garoon-sheets-sync          # Garoon + Sheets同期
├── suno-auto                   # Suno自動化ツール
├── fc2-video-scraper           # FC2動画スクレイパー
├── design-workflow             # デザインワークフロー
└── dify-note                   # Difyノート
```

**使用例**:
```yaml
tags:
  - "project/airregi-analytics"
  - "project/dify-n8n-workflow"
```

---

### 2. documentation/ - ドキュメント種別タグ

ドキュメントの種類・目的を示すタグ。

```
documentation/
├── readme                      # プロジェクトREADME
├── setup                       # セットアップ手順
├── guide                       # 一般的なガイド・チュートリアル
├── quickstart                  # クイックスタートガイド
├── advanced                    # 高度な機能・設定
├── report                      # 分析レポート・調査結果
├── progress                    # 進捗ログ・開発ログ
├── session-log                 # セッション記録
├── changelog                   # 変更履歴
├── reference                   # リファレンス資料
└── template                    # テンプレート
```

**使用例**:
```yaml
tags:
  - "documentation/setup"
  - "documentation/guide"
  - "documentation/report"
```

**統合ルール**:
- ❌ 削除: `documentation`（階層なし）
- ✅ 使用: `documentation/guide`, `documentation/setup`等

---

### 3. integration/ - 統合・連携タグ

外部サービス・APIとの統合を示すタグ。

```
integration/
├── api/                        # API統合
│   ├── dataforseo             # DataForSEO API
│   ├── serpstack              # SerpStack API
│   ├── openai                 # OpenAI API
│   └── anthropic              # Anthropic Claude API
├── webhook                     # Webhook連携
├── google/                     # Google サービス
│   ├── sheets                 # Google Sheets
│   ├── apps-script            # Google Apps Script
│   └── oauth                  # Google OAuth認証
├── telegram                    # Telegram Bot統合
├── line                        # LINE API統合
└── dify                        # Dify統合
```

**使用例**:
```yaml
tags:
  - "integration/api/dataforseo"
  - "integration/webhook"
  - "integration/google/sheets"
```

**統合ルール**:
- `integration/google` → `integration/google/sheets`（詳細化）
- `integration/api` + `setup/api` → `integration/api`（統一）

---

### 4. workflow/ - ワークフロー・自動化タグ

自動化ワークフローの種類を示すタグ。

```
workflow/
├── automation                  # 一般的な自動化
├── telegram                    # Telegram経由ワークフロー
├── seo                         # SEO関連ワークフロー
├── sales-report                # 売上レポート処理
├── excel-parser                # Excel解析処理
├── data-sync                   # データ同期
└── notification                # 通知自動化
```

**使用例**:
```yaml
tags:
  - "workflow/telegram"
  - "workflow/seo"
  - "workflow/automation"
```

---

### 5. setup/ - セットアップ・設定タグ

セットアップ・環境構築に関するタグ。

```
setup/
├── configuration               # 一般的な設定
├── docker                      # Docker環境設定
├── oauth                       # OAuth認証設定
├── telegram                    # Telegram Bot設定
├── google-sheets               # Google Sheets設定
├── n8n                         # n8n環境設定
└── environment                 # 環境変数・.env設定
```

**使用例**:
```yaml
tags:
  - "setup/docker"
  - "setup/configuration"
  - "setup/oauth"
```

**統合ルール**:
- `setup/general` → `setup/configuration`（統一）
- `setup/api` → `integration/api`（より適切なカテゴリへ）

---

### 6. troubleshooting/ - トラブルシューティングタグ

問題解決・エラー対処に関するタグ。

```
troubleshooting/
├── n8n                         # n8n関連トラブル
├── telegram                    # Telegram Bot問題
├── api                         # API接続問題
├── google-sheets               # Google Sheets問題
├── authentication              # 認証エラー
└── guide                       # トラブルシューティング一般
```

**使用例**:
```yaml
tags:
  - "troubleshooting/n8n"
  - "troubleshooting/api"
```

---

### 7. navigation/ - ナビゲーションタグ

Vault内のナビゲーション・構造化に関するタグ。

```
navigation/
├── moc                         # Map of Content（MOC）
├── index                       # インデックスページ
└── hub                         # ハブページ
```

**使用例**:
```yaml
tags:
  - "navigation/moc"
```

**統合ルール**:
- `moc` → `navigation/moc`（階層化）
- `index` → `navigation/index`（階層化）

---

### 8. metadata/ - メタデータ管理タグ

Vault管理・メタデータに関するタグ。

```
metadata/
├── standardization             # 標準化関連
├── standards                   # 標準・規約
├── optimization                # 最適化
├── performance                 # パフォーマンス
└── vault-health                # Vault健全性
```

**使用例**:
```yaml
tags:
  - "metadata/standardization"
  - "metadata/standards"
```

**統合ルール**:
- `standardization` → `metadata/standardization`（階層化）
- `optimization` → `metadata/optimization`（階層化）
- `performance` → `metadata/performance`（階層化）
- `vault-health` → `metadata/vault-health`（階層化）

---

### 9. template/ - テンプレートタグ

再利用可能なテンプレートに関するタグ。

```
template/
├── reference                   # リファレンステンプレート
├── workflow                    # ワークフローテンプレート
└── document                    # ドキュメントテンプレート
```

**使用例**:
```yaml
tags:
  - "template/reference"
```

---

## タグ標準化マッピング

### 統合・削除対象タグ

以下のタグは標準化により変更されます：

| 現在のタグ | 標準化後のタグ | 理由 |
|-----------|--------------|------|
| `documentation` | `documentation/guide` | 階層化必須 |
| `index` | `navigation/index` | 階層化 |
| `moc` | `navigation/moc` | 階層化 |
| `navigation` | `navigation/moc` | 階層化 |
| `standardization` | `metadata/standardization` | 階層化 |
| `optimization` | `metadata/optimization` | 階層化 |
| `performance` | `metadata/performance` | 階層化 |
| `vault-health` | `metadata/vault-health` | 階層化 |
| `sales-automation` | `workflow/sales-report` | より具体的 |
| `setup/general` | `setup/configuration` | 統一 |
| `setup/api` | `integration/api` | 適切なカテゴリへ |
| `setup/api/serpstack` | `integration/api/serpstack` | 適切なカテゴリへ |

---

## タグ使用ガイドライン

### 基本ルール

1. **プロジェクトタグは必須**: すべてのファイルに `project/xxx` タグを付与
2. **ドキュメントタイプタグを推奨**: `documentation/xxx` タグで種類を明示
3. **タグ数は3〜5個**: 過度なタグ付けを避ける
4. **階層は必須**: フラットタグ（`/`なし）は禁止

### ファイル種別ごとの推奨タグ

#### README.md（プロジェクトルート）
```yaml
tags:
  - "project/[プロジェクト名]"
  - "documentation/readme"
```

#### セットアップガイド
```yaml
tags:
  - "project/[プロジェクト名]"
  - "documentation/setup"
  - "setup/[具体的な設定項目]"
  - "integration/[統合サービス]"  # 該当する場合
```

#### トラブルシューティング
```yaml
tags:
  - "project/[プロジェクト名]"
  - "troubleshooting/[対象システム]"
  - "documentation/guide"
```

#### MOC（Map of Content）
```yaml
tags:
  - "project/[プロジェクト名]"  # 該当する場合
  - "navigation/moc"
```

#### 分析レポート
```yaml
tags:
  - "project/[プロジェクト名]"  # 該当する場合
  - "documentation/report"
  - "metadata/[分析対象]"  # 該当する場合
```

#### ワークフローガイド
```yaml
tags:
  - "project/[プロジェクト名]"
  - "documentation/guide"
  - "workflow/[ワークフロータイプ]"
```

---

## Obsidian活用ガイド

### タグ検索例

```
# 特定プロジェクトのすべてのドキュメント
tag:#project/dify-n8n-workflow

# セットアップガイドのみ
tag:#documentation/setup

# n8nのトラブルシューティング
tag:#troubleshooting/n8n

# 複数タグの組み合わせ（AND検索）
tag:#project/airregi-analytics tag:#integration/google
```

### Dataview クエリ例

#### プロジェクト別ファイル一覧
```dataview
TABLE type, status, created
FROM #project/dify-n8n-workflow
SORT created DESC
```

#### セットアップガイド一覧
```dataview
LIST
FROM #documentation/setup
SORT file.name ASC
```

#### 最近のレポート
```dataview
TABLE updated
FROM #documentation/report
WHERE updated >= date(today) - dur(30 days)
SORT updated DESC
```

---

## メンテナンス計画

### 月次レビュー
1. 新規タグの確認と分類体系への統合
2. フラットタグ（階層なし）の洗い出しと修正
3. 重複タグの統合

### 四半期レビュー
1. タグ分類体系の見直し
2. 使用頻度の低いタグの統廃合
3. 新カテゴリの追加検討

---

## 自動化ツール

### タグ標準化スクリプト
```bash
# 分析のみ（ドライラン）
python3 /Users/remma/project/scripts/tag_standardizer.py --report

# 標準化実行
python3 /Users/remma/project/scripts/tag_standardizer.py
```

---

## バージョン履歴

| バージョン | 日付 | 変更内容 |
|------------|------|----------|
| 1.0.0 | 2025-11-01 | 初版作成、59タグの分析と分類体系定義 |

---

**作成者**: Claude (Sonnet 4.5) - Tag Standardization Agent  
**最終更新**: 2025-11-01  
**ステータス**: Active

---

## 関連ドキュメント

- [[TAG_HIERARCHY_VISUAL]]

