---
title: "Project Vault - Home"
type: moc
status: active
created: "2025-11-01"
updated: "2025-11-01"
tags:
  - "navigation/moc"
  - "navigation/index"
---

# Project Vault - ホーム

**最終更新**: 2025-11-01
**総プロジェクト数**: 15
**総ドキュメント数**: 136 Markdownファイル

---

## クイックナビゲーション

### プロジェクトMOC
主要なプロジェクトごとのMap of Content

- [[MOC - Airregi Analytics]] - Airレジ売上分析システム
- [[MOC - Crypto Scalping]] - 仮想通貨スキャルピング・デイトレード
- [[MOC - LINE Chat Logger]] - LINEチャットログ自動保存システム
- [[MOC - Dify n8n Workflow]] - Telegram売上日報自動処理（最大規模プロジェクト）
- [[MOC - Automation Projects]] - 自動化系プロジェクト統合

### テクニカルMOC
技術スタックや横断的トピックごとのMOC

- [[MOC - API Integration]] - API統合・認証パターン
- [[MOC - Google Services]] - Google Sheets、OAuth、Apps Script
- [[MOC - Authentication]] - 認証・セキュリティ実装
- [[MOC - Deployment]] - デプロイメント・インフラ
- [[MOC - Troubleshooting]] - トラブルシューティング全般

### ドキュメントタイプMOC
ドキュメント種別ごとの索引

- [[MOC - Setup Guides]] - セットアップガイド統合
- [[MOC - Session Logs]] - 開発セッションログ統合
- [[MOC - Analysis Reports]] - 分析レポート統合

---

## プロジェクト一覧

### アクティブプロジェクト

#### ビジネス自動化
| プロジェクト | 目的 | 技術スタック | ステータス |
|------------|------|------------|---------|
| [[MOC - Airregi Analytics]] | Airレジ売上分析・Google Sheets連携 | Python, Google Sheets API | アクティブ |
| [[MOC - Dify n8n Workflow]] | Telegram売上日報自動処理 | n8n, Dify, Claude AI | 本番稼働 |
| [[Garoon Sheets Sync]] | Garoon + Google Sheets同期 | Google Apps Script | 完了 |

#### チャットログ・コミュニケーション
| プロジェクト | 目的 | 技術スタック | ステータス |
|------------|------|------------|---------|
| [[MOC - LINE Chat Logger]] | LINEチャットログ自動保存 | Node.js, Vercel, Neon Postgres | 本番稼働 |
| [[LINE Works Chat Logger]] | LINE WORKSログ保存 | Node.js | アクティブ |

#### 金融・トレーディング
| プロジェクト | 目的 | 技術スタック | ステータス |
|------------|------|------------|---------|
| [[MOC - Crypto Scalping]] | 仮想通貨スキャルピング | TradingView, Bybit MCP | アクティブ |

#### AI・自動化ワークフロー
| プロジェクト | 目的 | 技術スタック | ステータス |
|------------|------|------------|---------|
| [[Codex Gas Automation]] | Codex + Google Apps Script自動化 | OpenAI Codex, GAS | 完了 |
| [[Codex Dify MCP Workflow]] | Codex + Dify + MCP連携 | Codex, Dify, MCP | 開発中 |
| [[Codex ChatGPT Workflow]] | Codex + ChatGPT連携 | Codex, ChatGPT | 完了 |

#### ウェブサイト・コンテンツ
| プロジェクト | 目的 | 技術スタック | ステータス |
|------------|------|------------|---------|
| [[UTAIBA]] | UTAIBAウェブサイト | フロントエンド | アクティブ |
| [[Suno Auto]] | Suno自動化ツール | Python | 完了 |

#### データ収集・スクレイピング
| プロジェクト | 目的 | 技術スタック | ステータス |
|------------|------|------------|---------|
| [[FC2 Video Scraper]] | FC2動画スクレイパー | Python | アクティブ |

#### システム・インフラ
| プロジェクト | 目的 | 技術スタック | ステータス |
|------------|------|------------|---------|
| [[Obsidian Sync Automation]] | Obsidian同期自動化 | Python/Bash | アクティブ |
| [[Design Workflow]] | デザインワークフロー | - | アクティブ |

---

## 技術スタック別索引

### バックエンド・スクリプティング
- **Python**: [[MOC - Airregi Analytics]], [[FC2 Video Scraper]], [[Suno Auto]]
- **Node.js**: [[MOC - LINE Chat Logger]], [[LINE Works Chat Logger]]
- **Google Apps Script**: [[Garoon Sheets Sync]], [[Codex Gas Automation]]

### ワークフロー自動化
- **n8n**: [[MOC - Dify n8n Workflow]]
- **Dify**: [[MOC - Dify n8n Workflow]], [[Codex Dify MCP Workflow]]

### データベース
- **PostgreSQL**: [[MOC - Dify n8n Workflow]]
- **Neon Postgres**: [[MOC - LINE Chat Logger]]

### AI/LLM
- **Claude AI**: [[MOC - Dify n8n Workflow]]
- **OpenAI**: [[Codex Gas Automation]], [[Codex ChatGPT Workflow]]

### デプロイメント
- **Vercel**: [[MOC - LINE Chat Logger]]
- **Docker**: [[MOC - Dify n8n Workflow]]

---

## クロスプロジェクトトピック

### API統合
[[MOC - API Integration]]で詳細を確認

**使用API一覧**:
- Google Sheets API: [[MOC - Airregi Analytics]], [[MOC - Dify n8n Workflow]]
- LINE Messaging API: [[MOC - LINE Chat Logger]]
- Telegram Bot API: [[MOC - Dify n8n Workflow]]
- Bybit API: [[MOC - Crypto Scalping]]
- DataForSEO / SerpStack: [[MOC - Dify n8n Workflow]]

### 認証パターン
[[MOC - Authentication]]で詳細を確認

- **OAuth 2.0**: Google Services
- **API Key**: LINE, Telegram, AI APIs
- **Basic Auth**: DataForSEO
- **Bearer Token**: Claude, OpenAI

### データ処理
- **Excel解析**: [[MOC - Dify n8n Workflow]]
- **CSV処理**: [[MOC - Airregi Analytics]]
- **JSON処理**: 全プロジェクト共通

---

## Vault管理

### メタデータ標準化
- [[METADATA_STANDARDS]] - メタデータスキーマ定義
- [[TAG_TAXONOMY]] - タグ分類体系
- [[FRONTMATTER_STANDARDIZATION_REPORT]] - フロントマター標準化レポート
- [[TAG_STANDARDIZATION_SUMMARY]] - タグ標準化サマリー

### Vault健全性
- [[CONTENT_CURATION_REPORT]] - コンテンツキュレーションレポート
- [[KNOWLEDGE_GRAPH_IMPLEMENTATION_SUMMARY]] - ナレッジグラフ実装サマリー
- [[CONNECTION_REPORT]] - 接続分析レポート

### Vault最適化
**現在のメトリクス**:
- 総ファイル数: 136
- フロントマター標準化: 完了
- タグ階層化: 完了
- ナレッジグラフリンク: 324
- MOCカバレッジ: 向上中

---

## セットアップガイド

### 新規プロジェクト開始時
1. [[MOC - Setup Guides]]でプロジェクトタイプに応じたガイドを選択
2. 認証が必要な場合は[[MOC - Authentication]]を参照
3. API統合が必要な場合は[[MOC - API Integration]]を参照

### トラブル発生時
1. [[MOC - Troubleshooting]]で問題のカテゴリを探す
2. プロジェクト固有の問題は各プロジェクトMOC内のトラブルシューティングセクションを参照

---

## リソース

### 外部ツール設定
- [[README_Codex_MCP_Setup]] - Codex MCP設定ガイド
- [[LCP_web_dev_2025]] - LCP Web開発ガイド（2025年版）

### テンプレート
- プロジェクトREADMEテンプレート: [[METADATA_STANDARDS]]を参照
- セットアップガイドテンプレート: [[MOC - Setup Guides]]を参照

---

## 次のステップ

### プロジェクト開始
- 新規プロジェクトを開始する場合: 対応するMOCを作成し、このホームからリンク
- 既存プロジェクトを拡張する場合: 該当プロジェクトのMOCを更新

### Vault改善
- [ ] 全プロジェクトのMOC作成完了
- [ ] クロストピックMOC拡充
- [ ] セッションログの統合
- [ ] トラブルシューティングナレッジベース拡充

---

**このVaultについて**:
- **作成日**: 2025-11-01
- **管理者**: remma
- **Vault目的**: 技術プロジェクトのナレッジマネジメント・ドキュメント統合
- **使用ツール**: Obsidian, Claude Code

---

## 関連ドキュメント

- [[MOC - Airregi Analytics]]
- [[MOC - API Integration]]
- [[MOC - Authentication]]
- [[MOC - Crypto Scalping]]
- [[MOC - Deployment]]
- [[MOC - Dify n8n Workflow]]
- [[MOC - Google Services]]
- [[MOC - LINE Chat Logger]]
- [[MOC - Setup Guides]]
- [[MOC - Troubleshooting]]
