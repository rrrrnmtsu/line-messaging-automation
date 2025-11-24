# ドキュメント整理・統合計画

**作成日**: 2025-11-11
**目的**: プロジェクトルート配下のドキュメントファイルを整理し、重複削除とファイル数削減を実施

---

## 現状分析

### プロジェクトルート直下（/Users/remma/project）

**総ファイル数**: 29ファイル

#### カテゴリー別内訳

| カテゴリー | ファイル数 | 課題 |
|-----------|-----------|------|
| TAG関連 | 6 | 重複・類似コンテンツが多数 |
| MOC関連 | 7 | レポートと実際のMOCが混在 |
| REPORT系 | 6 | 古いレポートが残存 |
| CURATION系 | 3 | 重複したサマリー・レポート |
| その他 | 7 | 整理済み |

---

## 整理方針

### 目標
- **ファイル数**: 29ファイル → **15ファイル以下** に削減
- **重複排除**: 類似コンテンツを統合
- **アーカイブ**: 古いレポートは docs/archive へ移動
- **分類化**: カテゴリー別ディレクトリ構造を整備

---

## 統合計画

### 1. TAG関連ファイル（6 → 2ファイル）

#### 保持するファイル
- [x] `TAG_TAXONOMY.md` - **マスタータグ定義**
  - 役割: タグの階層構造・定義を集約
  - 統合元: `QUICK_TAG_REFERENCE.md` の内容を追加

- [x] `TAG_STANDARDIZATION_SUMMARY.md` - **TAG関連レポート統合版**
  - 役割: TAG標準化の経緯・実装状況を記録
  - 統合元:
    - `TAG_STANDARDIZATION_REPORT.md`
    - `TAG_IMPLEMENTATION_COMPLETE.md`
    - `TAG_HIERARCHY_VISUAL.md`

#### 削除するファイル（統合後）
- [ ] `TAG_STANDARDIZATION_REPORT.md` → `TAG_STANDARDIZATION_SUMMARY.md` に統合
- [ ] `TAG_IMPLEMENTATION_COMPLETE.md` → `TAG_STANDARDIZATION_SUMMARY.md` に統合
- [ ] `TAG_HIERARCHY_VISUAL.md` → `TAG_STANDARDIZATION_SUMMARY.md` に統合
- [ ] `QUICK_TAG_REFERENCE.md` → `TAG_TAXONOMY.md` に統合

---

### 2. CURATION関連ファイル（3 → 1ファイル）

#### 保持するファイル
- [x] `CONTENT_CURATION_SUMMARY.md` - **キュレーション統合版**
  - 役割: コンテンツキュレーションの全記録
  - 統合元:
    - `CONTENT_CURATION_REPORT.md` - 詳細レポート
    - `CURATION_ACTION_PLAN.md` - アクションプラン
    - `CURATION_SUMMARY.md` - サマリー

#### 削除するファイル（統合後）
- [ ] `CONTENT_CURATION_REPORT.md` → `CONTENT_CURATION_SUMMARY.md` に統合
- [ ] `CURATION_ACTION_PLAN.md` → `CONTENT_CURATION_SUMMARY.md` に統合
- [ ] `CURATION_SUMMARY.md` → `CONTENT_CURATION_SUMMARY.md` に統合

---

### 3. REPORT系ファイル（6 → 2ファイル + archive）

#### 保持するファイル（プロジェクトルート）
- [x] `PROJECT_ECOSYSTEM_REQUIREMENTS.md` - 最新のプロジェクト要件
- [x] `OBSIDIAN_VAULT_PERFORMANCE_REPORT.md` - パフォーマンス分析（参照価値高）

#### docs/archive/reports へ移動
- [ ] `CONNECTION_REPORT.md` - 古いナレッジグラフレポート
- [ ] `FRONTMATTER_STANDARDIZATION_REPORT.md` - 古い標準化レポート
- [ ] `MOC_IMPLEMENTATION_REPORT.md` - 古いMOCレポート
- [ ] `KNOWLEDGE_GRAPH_IMPLEMENTATION_SUMMARY.md` - 古い実装サマリー

---

### 4. MOC関連ファイル（7 → 6ファイル + archive）

#### 保持するファイル（プロジェクトルート）
- [x] `MOC - Airregi Analytics.md` - 実際のMOC
- [x] `MOC - Authentication.md` - 実際のMOC
- [x] `MOC - Crypto Scalping.md` - 実際のMOC
- [x] `MOC - Google Services.md` - 実際のMOC
- [x] `MOC - LINE Chat Logger.md` - 実際のMOC
- [x] `MOC - Troubleshooting.md` - 実際のMOC

#### docs/archive/reports へ移動
- [ ] `MOC_IMPLEMENTATION_REPORT.md` - レポートなので archive へ

---

### 5. その他ファイル（7ファイル - 整理済み）

#### 保持するファイル
- [x] `README.md` - プロジェクトルートのREADME
- [x] `Home.md` - Obsidian Vaultのホーム
- [x] `SETUP_GOOGLE_DRIVE.md` - セットアップガイド
- [x] `DESIGN_FILE_MANAGEMENT.md` - デザインファイル管理
- [x] `METADATA_STANDARDS.md` - メタデータ標準
- [x] `LCP_web_dev_2025.md` - Web開発ガイド
- [x] `README_Codex_MCP_Setup.md` - Codex MCP設定
- [x] `bybit_mcp_setup_log.md` - Bybit MCP設定ログ

---

## 新しいディレクトリ構造

```
/Users/remma/project/
├── README.md
├── Home.md
│
├── docs/
│   ├── standards/
│   │   ├── TAG_TAXONOMY.md
│   │   ├── METADATA_STANDARDS.md
│   │   └── DESIGN_FILE_MANAGEMENT.md
│   │
│   ├── reports/
│   │   ├── TAG_STANDARDIZATION_SUMMARY.md
│   │   ├── CONTENT_CURATION_SUMMARY.md
│   │   ├── OBSIDIAN_VAULT_PERFORMANCE_REPORT.md
│   │   └── PROJECT_ECOSYSTEM_REQUIREMENTS.md
│   │
│   ├── setup/
│   │   ├── SETUP_GOOGLE_DRIVE.md
│   │   ├── README_Codex_MCP_Setup.md
│   │   └── bybit_mcp_setup_log.md
│   │
│   ├── guides/
│   │   └── LCP_web_dev_2025.md
│   │
│   └── archive/
│       └── reports/
│           ├── CONNECTION_REPORT.md
│           ├── FRONTMATTER_STANDARDIZATION_REPORT.md
│           ├── MOC_IMPLEMENTATION_REPORT.md
│           └── KNOWLEDGE_GRAPH_IMPLEMENTATION_SUMMARY.md
│
├── MOCs/
│   ├── MOC - Airregi Analytics.md
│   ├── MOC - Authentication.md
│   ├── MOC - Crypto Scalping.md
│   ├── MOC - Google Services.md
│   ├── MOC - LINE Chat Logger.md
│   └── MOC - Troubleshooting.md
│
├── assets/
├── projects/analytics/airregi-analytics/
├── projects/finance/crypto-scalping/
├── projects/automation/dify-workspace/
├── ...（各プロジェクト）
```

---

## 削減効果

### ファイル数削減

| カテゴリー | 統合前 | 統合後 | 削減数 |
|-----------|-------|-------|-------|
| TAG関連 | 6 | 2 | -4 |
| CURATION関連 | 3 | 1 | -2 |
| REPORT系（archive含む） | 6 | 2 | -4 |
| MOC関連 | 7 | 6 | -1 |
| その他 | 7 | 7 | 0 |
| **合計** | **29** | **18** | **-11** |

### さらなる削減（ディレクトリ構造整理後）

**プロジェクトルート直下**: 29ファイル → **2ファイル**（README.md, Home.md のみ）

**削減率**: 93%

---

## 実行手順

### Phase 1: ディレクトリ構造作成

```bash
mkdir -p /Users/remma/project/docs/{standards,reports,setup,guides,archive/reports}
mkdir -p /Users/remma/project/MOCs
```

### Phase 2: TAG関連ファイル統合

1. `TAG_STANDARDIZATION_SUMMARY.md` を作成（3ファイル統合）
2. `TAG_TAXONOMY.md` に `QUICK_TAG_REFERENCE.md` の内容を追加
3. 統合元ファイルを削除

### Phase 3: CURATION関連ファイル統合

1. `CONTENT_CURATION_SUMMARY.md` を作成（3ファイル統合）
2. 統合元ファイルを削除

### Phase 4: REPORT系ファイル整理

1. 古いレポートを `docs/archive/reports/` へ移動
2. 最新レポートを `docs/reports/` へ移動

### Phase 5: ファイル分類移動

1. MOCファイルを `MOCs/` へ移動
2. セットアップガイドを `docs/setup/` へ移動
3. 標準ドキュメントを `docs/standards/` へ移動

### Phase 6: 検証

1. リンク切れチェック
2. ファイル参照の更新
3. 最終確認

---

## リスク評価

| リスク | 影響度 | 対策 |
|-------|-------|------|
| リンク切れ | 中 | 移動前にバックアップ、移動後にリンクチェック |
| 情報の欠落 | 低 | 統合前に内容を精査、重複排除のみ実施 |
| Git履歴の混乱 | 低 | git mv を使用、コミットメッセージで明示 |

---

## 承認チェックリスト

- [ ] 統合計画を確認
- [ ] ディレクトリ構造を承認
- [ ] 削除対象ファイルを確認
- [ ] 実行開始を承認

---

## 次のアクション

統合計画の承認後、以下を実行します:

1. **Phase 1-2**: TAG関連ファイル統合（所要時間: 15分）
2. **Phase 3**: CURATION関連ファイル統合（所要時間: 10分）
3. **Phase 4-5**: ディレクトリ構造整理（所要時間: 20分）
4. **Phase 6**: 検証とレポート作成（所要時間: 15分）

**総所要時間**: 約60分
