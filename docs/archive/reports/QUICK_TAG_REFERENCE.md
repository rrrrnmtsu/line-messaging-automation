---
title: "Quick Tag Reference - Project Vault"
type: documentation
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "metadata/standards"
  - "documentation/guide"
---

# クイックタグリファレンス

プロジェクトVaultで使用する標準化タグのクイックリファレンス。

---

## タグ選択フローチャート

```
新規ファイル作成
    ↓
1. プロジェクトタグを選択（必須）
   → project/[プロジェクト名]
    ↓
2. ドキュメント種別を選択
   → documentation/[種別]
    ↓
3. 追加タグを選択（該当する場合のみ）
   → integration/*, workflow/*, setup/*, etc.
```

---

## 必須タグ

### プロジェクトタグ（すべてのファイルに必須）

```yaml
# プロジェクトごとに1つ選択
tags:
  - "project/airregi-analytics"
  - "project/crypto-scalping"
  - "project/dify-n8n-workflow"
  - "project/utaiba"
  - "project/line-chat-logger"
  - "project/obsidian-sync-automation"
  - "project/codex-gas-automation"
  # その他のプロジェクト...
```

---

## よく使うタグ組み合わせ

### README.md（プロジェクトルート）
```yaml
tags:
  - "project/[プロジェクト名]"
  - "documentation/readme"
```

### セットアップガイド
```yaml
tags:
  - "project/[プロジェクト名]"
  - "documentation/setup"
  - "setup/docker"                    # 該当する場合
  - "integration/webhook"             # 該当する場合
```

### API統合ガイド
```yaml
tags:
  - "project/[プロジェクト名]"
  - "documentation/guide"
  - "integration/api"
  - "setup/configuration"
```

### トラブルシューティング
```yaml
tags:
  - "project/[プロジェクト名]"
  - "troubleshooting/n8n"             # 対象システム
  - "documentation/guide"
```

### ワークフロー設定
```yaml
tags:
  - "project/[プロジェクト名]"
  - "documentation/guide"
  - "workflow/telegram"               # ワークフロータイプ
  - "integration/webhook"             # 該当する場合
```

### 分析レポート
```yaml
tags:
  - "project/[プロジェクト名]"       # 該当する場合
  - "documentation/report"
  - "metadata/performance"            # 該当する場合
```

### MOC（Map of Content）
```yaml
tags:
  - "navigation/moc"
  - "project/[プロジェクト名]"       # 該当する場合
```

---

## タグカテゴリ一覧

### project/ - プロジェクト識別
```
project/airregi-analytics
project/crypto-scalping
project/dify-n8n-workflow
project/utaiba
project/line-chat-logger
project/lineworks-chat-logger
project/obsidian-sync-automation
project/codex-gas-automation
project/codex-dify-mcp-workflow
project/codex-chatgpt-workflow
project/garoon-sheets-sync
project/suno-auto
project/fc2-video-scraper
project/design-workflow
project/dify-note
```

### documentation/ - ドキュメント種別
```
documentation/readme          # プロジェクトREADME
documentation/setup           # セットアップ手順
documentation/guide           # 一般ガイド
documentation/quickstart      # クイックスタート
documentation/advanced        # 高度な機能
documentation/report          # レポート・分析
documentation/progress        # 進捗ログ
documentation/session-log     # セッション記録
documentation/changelog       # 変更履歴
documentation/reference       # リファレンス
documentation/template        # テンプレート
```

### integration/ - 統合・連携
```
integration/api               # API統合
integration/api/dataforseo    # DataForSEO API
integration/api/serpstack     # SerpStack API
integration/webhook           # Webhook連携
integration/google            # Google サービス
integration/telegram          # Telegram Bot
integration/line              # LINE API
integration/dify              # Dify統合
```

### workflow/ - ワークフロー
```
workflow/automation           # 一般自動化
workflow/telegram             # Telegram経由
workflow/seo                  # SEO関連
workflow/sales-report         # 売上レポート
workflow/excel-parser         # Excel解析
workflow/data-sync            # データ同期
workflow/notification         # 通知自動化
```

### setup/ - セットアップ
```
setup/configuration           # 一般設定
setup/docker                  # Docker環境
setup/oauth                   # OAuth認証
setup/telegram                # Telegram Bot
setup/google-sheets           # Google Sheets
setup/n8n                     # n8n環境
setup/environment             # 環境変数
```

### troubleshooting/ - トラブルシューティング
```
troubleshooting/n8n           # n8n問題
troubleshooting/telegram      # Telegram問題
troubleshooting/api           # API問題
troubleshooting/google-sheets # Sheets問題
troubleshooting/authentication # 認証エラー
troubleshooting/guide         # 一般ガイド
```

### navigation/ - ナビゲーション
```
navigation/moc                # Map of Content
navigation/index              # インデックス
navigation/hub                # ハブページ
```

### metadata/ - メタデータ管理
```
metadata/standardization      # 標準化関連
metadata/standards            # 標準・規約
metadata/optimization         # 最適化
metadata/performance          # パフォーマンス
metadata/vault-health         # Vault健全性
```

### template/ - テンプレート
```
template/reference            # リファレンステンプレート
template/workflow             # ワークフローテンプレート
template/document             # ドキュメントテンプレート
```

---

## タグ選択のベストプラクティス

### ✅ 推奨

1. **階層構造を使用**: `category/subcategory`
2. **プロジェクトタグは必須**: すべてのファイルに1つ
3. **3〜5個のタグ**: 過度なタグ付けを避ける
4. **既存タグを優先**: 新規タグ作成前に既存タグを確認

### ❌ 避けるべき

1. **フラットタグ**: `setup` → `setup/configuration`
2. **過度な細分化**: タグが多すぎると管理困難
3. **重複タグ**: 同じ概念に複数のタグ
4. **プロジェクトタグなし**: プロジェクト分類ができない

---

## Obsidian活用Tips

### タグ検索（Ctrl/Cmd + Shift + F）
```
# 特定プロジェクト
tag:#project/dify-n8n-workflow

# セットアップガイドのみ
tag:#documentation/setup

# 複数タグ（AND検索）
tag:#project/airregi-analytics tag:#integration/google
```

### Dataview クエリ
````markdown
```dataview
TABLE type, status, created
FROM #project/dify-n8n-workflow
SORT created DESC
```
````

### タグペイン活用
- サイドバーの「タグ」パネルで階層構造を確認
- クリックで該当ファイル一覧を表示

---

## 自動化ツール

### タグ標準化スクリプト
```bash
# レポート生成（変更確認）
python3 /Users/remma/project/scripts/tag_standardizer.py --report

# 標準化実行
python3 /Users/remma/project/scripts/tag_standardizer.py
```

---

## 詳細ドキュメント

- 📖 **包括的ガイド**: [TAG_TAXONOMY.md](/Users/remma/project/TAG_TAXONOMY.md)
- 📊 **標準化サマリー**: [TAG_STANDARDIZATION_SUMMARY.md](/Users/remma/project/TAG_STANDARDIZATION_SUMMARY.md)
- 📝 **標準化レポート**: [TAG_STANDARDIZATION_REPORT.md](/Users/remma/project/TAG_STANDARDIZATION_REPORT.md)

---

**作成**: Claude (Sonnet 4.5)  
**更新**: 2025-11-01  
**バージョン**: 1.0.0

---

## 関連ドキュメント

- [[TAG_HIERARCHY_VISUAL]]
- [[TAG_TAXONOMY]]

