---
title: "Project Vault - Metadata Standards"
type: documentation
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "documentation/guide"
  - "metadata/standards"
---

# プロジェクトVault メタデータ標準スキーマ

**作成日**: 2025-11-01  
**対象**: /Users/remma/project  
**総ファイル数**: 123 Markdownファイル

---

## 概要

このドキュメントは、プロジェクトVault内のすべてのMarkdownファイルに適用される**標準化されたYAMLフロントマター**のスキーマ定義です。

---

## 標準フロントマタースキーマ

### 必須フィールド

```yaml
---
title: "ドキュメントタイトル"
type: "ドキュメントタイプ"
status: "ステータス"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "カテゴリ/サブカテゴリ"
---
```

---

## フィールド定義

### 1. title (必須)
- **説明**: ドキュメントの人間可読なタイトル
- **形式**: 文字列（ダブルクォート推奨）
- **生成方法**: ファイル内の最初のH1見出し、またはファイル名から自動生成
- **例**: `"Dify-n8n Workflow セットアップガイド"`

### 2. type (必須)
- **説明**: ドキュメントの種類
- **形式**: 文字列（14種類の定義済みタイプ）
- **許容値**:
  - `readme` - プロジェクトREADME
  - `documentation` - 一般ドキュメント
  - `setup-guide` - セットアップ手順
  - `workflow-guide` - ワークフロー説明
  - `api-documentation` - API仕様
  - `session-log` - セッション記録
  - `progress-log` - 進捗ログ
  - `moc` - Map of Content（ナビゲーション）
  - `analysis-report` - 分析レポート
  - `troubleshooting` - トラブルシューティング
  - `changelog` - 変更履歴
  - `template` - テンプレート
  - `quickstart` - クイックスタート
  - `status-report` - ステータスレポート

### 3. status (必須)
- **説明**: ドキュメントの現在の状態
- **形式**: 文字列（4種類）
- **許容値**:
  - `active` - 現在アクティブ（デフォルト）
  - `completed` - 完了済み
  - `draft` - 草稿
  - `archive` - アーカイブ

### 4. created (必須)
- **説明**: ドキュメント作成日
- **形式**: `YYYY-MM-DD`
- **取得方法**: ファイルシステムの作成日時（`st_birthtime`）
- **例**: `"2025-10-20"`

### 5. updated (必須)
- **説明**: 最終更新日
- **形式**: `YYYY-MM-DD`
- **取得方法**: ファイルシステムの最終更新日時（`st_mtime`）
- **例**: `"2025-11-01"`

### 6. tags (必須)
- **説明**: 階層的なタグ（カテゴリ分類）
- **形式**: YAML配列
- **構造**: `カテゴリ/サブカテゴリ` 形式の階層型
- **制限**: 最大5タグ推奨
- **例**:
  ```yaml
  tags:
    - "project/dify-n8n-workflow"
    - "documentation/setup"
    - "integration/webhook"
    - "workflow/automation"
  ```

---

## タグ分類体系

### プロジェクトタグ
プロジェクト識別用のタグです。すべてのファイルに最低1つのプロジェクトタグを付けることを推奨します。

```
project/
  ├─ airregi-analytics
  ├─ dify-n8n-workflow
  ├─ crypto-scalping
  ├─ utaiba
  ├─ codex-chatgpt-workflow
  ├─ codex-dify-mcp-workflow
  ├─ codex-gas-automation
  ├─ garoon-sheets-sync
  ├─ line-chat-logger
  ├─ lineworks-chat-logger
  ├─ obsidian-sync-automation
  ├─ suno_auto
  ├─ fc2-video-scraper
  ├─ design-workflow
  └─ dify_note
```

### ドキュメントカテゴリタグ
ドキュメントの種類・用途を示すタグです。

```
documentation/
  ├─ readme         # プロジェクトREADME
  ├─ setup          # セットアップ手順
  ├─ guide          # 一般的なガイド
  ├─ report         # レポート・分析
  ├─ session-log    # セッションログ
  ├─ progress       # 進捗ログ
  └─ api            # API仕様
```

### 技術カテゴリタグ
技術的な分類・統合対象を示すタグです。

```
integration/
  ├─ api            # API統合
  ├─ webhook        # Webhook連携
  ├─ google         # Google サービス
  └─ telegram       # Telegram統合

workflow/
  ├─ automation     # 自動化ワークフロー
  ├─ telegram       # Telegramワークフロー
  └─ seo            # SEO関連

setup/
  ├─ configuration  # 設定・構成
  ├─ docker         # Docker関連
  └─ deployment     # デプロイ関連

troubleshooting/
  ├─ guide          # トラブルシューティングガイド
  ├─ n8n            # n8n関連トラブル
  └─ errors         # エラー対応

navigation/
  └─ moc            # Map of Content
```

---

## オプションフィールド

### version
- **説明**: ドキュメントのバージョン番号
- **形式**: セマンティックバージョニング（例: `"1.0.0"`）
- **対象**: README、API仕様など
- **例**: `version: "2.1.0"`

### session_date
- **説明**: セッション実施日
- **形式**: `YYYY-MM-DD`
- **対象**: session-logタイプのみ
- **例**: `session_date: "2025-10-28"`

### author
- **説明**: ドキュメント作成者
- **形式**: 文字列
- **例**: `author: "Claude (Sonnet 4.5)"`, `author: "Codex"`, `author: "Human"`

---

## ファイルタイプ別推奨メタデータ

### README.md（プロジェクトルート）

```yaml
---
title: "[プロジェクト名] - README"
type: readme
status: active
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "project/[プロジェクト名]"
  - "documentation/readme"
version: "1.0.0"
---
```

**推奨追加フィールド**: `version`

---

### セッションログ

```yaml
---
title: "[プロジェクト名] セッションログ"
type: session-log
status: active
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
session_date: "YYYY-MM-DD"
tags:
  - "project/[プロジェクト名]"
  - "documentation/session-log"
---
```

**推奨追加フィールド**: `session_date`

---

### セットアップガイド

```yaml
---
title: "[機能名] セットアップガイド"
type: setup-guide
status: active
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "documentation/setup"
  - "setup/configuration"
  - "[追加の技術タグ]"
---
```

---

### MOC (Map of Content)

```yaml
---
title: "MOC - [トピック名]"
type: moc
status: active
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "navigation/moc"
  - "[カテゴリタグ]"
---
```

---

### 分析レポート

```yaml
---
title: "[対象] 分析レポート"
type: analysis-report
status: completed
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "documentation/report"
  - "[対象カテゴリ]"
---
```

**デフォルトステータス**: `completed`

---

### ワークフローガイド

```yaml
---
title: "[ワークフロー名]"
type: workflow-guide
status: active
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "project/[プロジェクト名]"
  - "workflow/automation"
---
```

---

### API仕様

```yaml
---
title: "[サービス名] API仕様"
type: api-documentation
status: active
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "documentation/api"
  - "integration/api"
version: "1.0.0"
---
```

**推奨追加フィールド**: `version`

---

## メタデータ管理ガイドライン

### 1. 新規ファイル作成時

新しいMarkdownファイルを作成する際は、以下のテンプレートから開始してください。

```yaml
---
title: "[タイトル]"
type: documentation
status: active
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "project/[プロジェクト名]"
---
```

### 2. ステータスの更新

- **active**: 現在も参照・更新されるドキュメント
- **completed**: 完了したタスク・レポート（変更不要）
- **archive**: 過去のドキュメントで参照のみ
- **draft**: 作成中のドキュメント

### 3. タグのベストプラクティス

1. **プロジェクトタグは必須**: すべてのファイルに`project/xxx`タグを付与
2. **階層は最大3レベル**: `category/subcategory/detail`
3. **タグ数は3〜5個**: 多すぎると管理が困難
4. **既存タグを優先**: 新規タグ作成前に既存タグを確認

### 4. 日付の管理

- **created**: 手動変更不要（ファイルシステムから自動取得）
- **updated**: ファイル更新時に自動更新（手動更新も可）
- セッションログの場合、`session_date`も併用

---

## Obsidian活用ガイド

### タグ検索

```
# 特定プロジェクトのすべてのドキュメント
tag:#project/airregi-analytics

# セットアップガイドのみ
tag:#documentation/setup

# 複数タグの組み合わせ
tag:#project/dify-n8n-workflow tag:#workflow/automation
```

### Dataview クエリ例

#### プロジェクト別ファイル一覧

```dataview
TABLE type, status, created
FROM #project/airregi-analytics
SORT created DESC
```

#### 最近更新されたファイル

```dataview
TABLE type, updated
WHERE updated >= date(today) - dur(7 days)
SORT updated DESC
```

#### ステータス別一覧

```dataview
TABLE file.name, type, created
WHERE status = "active"
SORT file.name ASC
```

---

## メンテナンス計画

### 月次レビュー（推奨）

1. **ステータス確認**: 完了したドキュメントを`completed`に変更
2. **タグの統一**: 類似タグの統合・正規化
3. **孤立ファイル確認**: プロジェクトタグのないファイルを確認
4. **リンク切れチェック**: 削除されたファイルへのリンク確認

### 四半期レビュー（推奨）

1. **アーカイブ処理**: 古いドキュメントを`archive`ステータスに
2. **タグ体系見直し**: 新しいカテゴリの追加検討
3. **MOC再構築**: プロジェクト構造の変化に応じてMOC更新

---

## 自動化の推奨

### Git Pre-commit Hook

新規ファイルにフロントマターを自動追加するフックの設定。

```bash
#!/bin/bash
# .git/hooks/pre-commit

python3 /path/to/add_frontmatter.py --auto
```

### 定期スクリプト

更新日を自動更新するスクリプトの定期実行。

```bash
# crontab -e
0 0 * * 0 python3 /path/to/update_modified_dates.py
```

---

## トラブルシューティング

### Q1: フロントマターのフォーマットエラー

**症状**: Obsidianでフロントマターが認識されない

**原因**: YAMLフォーマットの誤り（インデント、クォート等）

**解決**:
- `---`で囲まれているか確認
- インデントが正しいか（スペース2個）
- クォートが正しく閉じられているか

### Q2: タグが反映されない

**症状**: タグ検索でファイルが表示されない

**原因**: タグの形式が不正

**解決**:
- タグがYAML配列形式か確認
- ダブルクォートで囲まれているか確認
- ハイフン（`-`）が各タグの前にあるか確認

### Q3: 既存のフロントマターが重複

**症状**: ファイルに複数のフロントマターブロック

**原因**: スクリプトの誤実行

**解決**:
- バックアップ（`/tmp/project_backup_*`）から復元
- 手動で不要なフロントマターブロックを削除

---

## 関連ドキュメント

- **標準化レポート**: `/Users/remma/project/FRONTMATTER_STANDARDIZATION_REPORT.md`
- **処理スクリプト**: `/tmp/add_frontmatter_with_backup.py`
- **バックアップ**: `/tmp/project_backup_20251101_134303/`

---

## バージョン履歴

| バージョン | 日付 | 変更内容 |
|------------|------|----------|
| 1.0.0 | 2025-11-01 | 初版作成、標準スキーマ定義 |

---

**作成者**: Claude (Sonnet 4.5) - Vault Metadata Agent  
**最終更新**: 2025-11-01  
**ステータス**: Active
