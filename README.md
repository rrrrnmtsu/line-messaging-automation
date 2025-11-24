# Project - Personal Project Ecosystem

プロジェクトエコシステムの統合管理リポジトリ

---

## 概要

複数の自動化ワークフロー、データ分析システム、連携ツール、再利用可能なライブラリモジュールを統合管理するプロジェクト。

---

## プロジェクト構成

### 📂 projects

プロジェクトはカテゴリ別に整理されています。

#### analytics
- **[airregi-analytics](./projects/analytics/airregi-analytics/)**: Airレジ分析システム

#### automation
- **[dify-n8n-workflow](./projects/automation/dify-n8n-workflow/)**: Dify-n8n統合ワークフロー
- **[researchagent](./projects/automation/researchagent/)**: リサーチエージェント
- **その他**: `gas-automation`, `n8n-workspace`, `test-taskmaster-demo`, `twitter-gas-integration`

#### communication
- **[line-chat-logger](./projects/communication/line-chat-logger/)**: LINEチャットロガー
- **[line-messaging](./projects/communication/line-messaging/)**
- **[lineworks-chat-logger](./projects/communication/lineworks-chat-logger/)**

#### finance
- **[crypto-scalping](./projects/finance/crypto-scalping/)**: 仮想通貨スキャルピングシステム

#### mobile
- **[ios_claudeworks](./projects/mobile/ios_claudeworks/)**
- **[ios-claude-zapier-integration](./projects/mobile/ios-claude-zapier-integration/)**

#### scraping
- **[book_ocr](./projects/scraping/book_ocr/)**
- **[fc2-video-scraper](./projects/scraping/fc2-video-scraper/)**

#### integration
- **[garoon-sheets-sync](./projects/integration/garoon-sheets-sync/)**
- **[logic-pro-python-integration](./projects/integration/logic-pro-python-integration/)**

### 📦 lib
- **[modules-library](./lib/modules-library/)**: 再利用可能なTypeScriptモジュール集（70モジュール）
  - 📦 リポジトリ: <https://github.com/rrrrnmtsu/modules-library>
  - ✅ iOS Claude Code対応
  - 🔧 15カテゴリ（AI、API、認証、自動化、セキュリティ等）
  - 📚 完全なドキュメント・型定義・実装例

### 📚 docs
- **[MOCs](./docs/MOCs/)**: Map of Content


### 🛠 _system
- **assets**: 画像・デザインアセット
- **scripts**: ユーティリティスクリプト

---

## デザインファイル管理

### Google Drive

デザインファイル（PSD/AI等）はGoogle Driveで管理しています。

- **メインフォルダ**: [project-design-files](https://drive.google.com/drive/folders/xxxxx)
  - ブランディング素材: [01_branding](https://drive.google.com/drive/folders/xxxxx)
  - UI デザイン: [02_ui-design](https://drive.google.com/drive/folders/xxxxx)
  - マーケティング素材: [03_marketing](https://drive.google.com/drive/folders/xxxxx)
  - Web素材: [04_web-assets](https://drive.google.com/drive/folders/xxxxx)

### 書き出しアセット（Git管理）

- ディレクトリ: [assets/images/](./_system/assets/images/)
- 一覧: [ASSET_INDEX.md](./_system/assets/ASSET_INDEX.md)

### 命名規則・運用ルール

詳細は以下を参照:
- [DESIGN_FILE_MANAGEMENT.md](./docs/reports/DESIGN_FILE_MANAGEMENT.md) - デザインファイル管理規則
- [SETUP_GOOGLE_DRIVE.md](./docs/setup/SETUP_GOOGLE_DRIVE.md) - セットアップガイド

### アクセス権限

デザインファイルの閲覧・編集権限が必要な場合は、プロジェクトリーダーに連絡してください。

---

## ドキュメント

### 構造化・知識管理

- [Home.md](./Home.md) - プロジェクトホーム
- [MOC_IMPLEMENTATION_REPORT.md](./docs/archive/reports/MOC_IMPLEMENTATION_REPORT.md) - MOC実装レポート
- [TAG_TAXONOMY.md](./docs/standards/TAG_TAXONOMY.md) - タグ分類体系
- [METADATA_STANDARDS.md](./docs/standards/METADATA_STANDARDS.md) - メタデータ標準

### セットアップ・ガイド

- [README_Codex_MCP_Setup.md](./docs/setup/README_Codex_MCP_Setup.md) - Codex MCP設定
- [SETUP_GOOGLE_DRIVE.md](./docs/setup/SETUP_GOOGLE_DRIVE.md) - Google Driveセットアップ

---

## セットアップ

### 前提条件

- Node.js 18+
- Python 3.9+
- Git

### クイックスタート

```bash
# リポジトリクローン
git clone https://github.com/rrrrnmtsu/project.git
cd project

# 各サブプロジェクトのセットアップは個別のREADMEを参照
```

---

## ライセンス

Private Repository - All Rights Reserved

---

**作成日**: 2025-01-10
**管理者**: rrrrnmtsu
