# Project Ecosystem 再構成 - 要件定義書

**バージョン**: 1.0.0
**作成日**: 2025-11-03
**対象期間**: 2025年11月〜12月（約4週間）
**承認者**: remma

---

## エグゼクティブサマリー

### プロジェクト概要

現在、`/Users/remma/project` には18の異なるプロジェクトが混在しており、**本番稼働プロジェクト**、**実験的プロジェクト**、**再利用可能なコンポーネント**が同一階層に配置されています。この構造は以下の問題を引き起こしています：

- 本番プロジェクトと実験プロジェクトの区別が困難
- 共通機能が複数プロジェクトで重複実装されている
- 発想ベースの開発において命名規則・品質基準が曖昧
- モバイル環境（iOS Claude Code）での開発が困難

### 目的

本要件定義書は、**3リポジトリモデル**への移行を通じて、以下の目標を達成することを目的としています：

1. **発想の自由度維持**: `ideas/` で実験・プロトタイピングを自由に実施
2. **本番品質の確保**: `products/` で厳格な品質基準を適用
3. **再利用性の向上**: `library/` で共通モジュールを体系的に管理
4. **モバイル開発の実現**: iOS Claude Code（クラウドSandbox）で `library/` モジュールを開発

### 3リポジトリモデルの利点

| リポジトリ | 目的 | 品質基準 | 主要対象 |
|-----------|------|---------|---------|
| **ideas/** | 発想ベース開発・実験 | 最小限（動作確認のみ） | 実験12プロジェクト |
| **products/** | 本番稼働システム | 本番品質（テスト・CI/CD） | 本番6プロジェクト |
| **library/** | 再利用可能モジュール | 最高品質（型定義・API文書・iOS互換） | 抽出6モジュール |

### 期待効果

#### 定量効果
- **開発効率**: 50%向上（共通モジュール再利用）
- **コード重複**: 40%削減（モジュール統合）
- **新規プロジェクト立ち上げ**: 75%時間短縮（テンプレート活用）
- **バグ発生率**: 30%削減（テスト充実）

#### 定性効果
- 発想・実験の心理的ハードルが下がる（`ideas/` での自由度）
- 本番システムの安定性が向上（`products/` での品質管理）
- 外出中もモジュール開発が可能（iOS Claude Code対応）
- ナレッジの体系化・チーム共有が容易

---

## 1. 現状分析

### 1.1 既存18プロジェクト一覧

| # | プロジェクト名 | 技術スタック | 現状ステータス | 主要機能 |
|---|--------------|------------|--------------|---------|
| 1 | **researchagent** | Node.js/TypeScript | 本番稼働 | n8n事例収集・Notion出力 |
| 2 | **line-chat-logger** | Node.js/Express | 本番稼働（Vercel） | LINEログ保存・ダッシュボード |
| 3 | **lineworks-chat-logger** | Node.js/Express | 本番稼働（Vercel） | LINE WORKSログ保存 |
| 4 | **airregi-analytics** | Python/Pandas | 本番稼働 | Airレジ売上分析・Sheets連携 |
| 5 | **garoon-sheets-sync** | Python + GAS | 本番稼働 | Garoon → Sheets同期 |
| 6 | **crypto-scalping** | Markdown + Bybit MCP | 本番稼働 | 仮想通貨トレード記録 |
| 7 | **dify-n8n-workflow** | Docker Compose | 実験中 | Dify × n8n統合環境 |
| 8 | **codex-chatgpt-workflow** | Markdown | 実験中 | 業務ワークフロー管理 |
| 9 | **codex-dify-mcp-workflow** | Docker | 実験中 | Dify + MCP開発環境 |
| 10 | **codex-gas-automation** | GAS/TypeScript | 半実験 | GAS業務自動化テンプレート |
| 11 | **suno_auto** | Node.js + MCP | 実験中 | Suno AI音楽生成（MCP Server） |
| 12 | **fc2-video-scraper** | Python | 実験終了 | FC2動画スクレイピング |
| 13 | **obsidian-sync-automation** | Shell Scripts | 実験中 | Obsidian Vault同期 |
| 14 | **design-workflow** | Minimal | 設計資料 | デザインワークフロー |
| 15 | **utaiba** | 不明 | 不明 | utaiba事業関連 |
| 16 | **scripts** | Python | ユーティリティ | tag_standardizer.py等 |
| 17 | **.obsidian** | 設定ファイル | 設定 | Obsidian設定 |
| 18 | **各種ドキュメント** | Markdown | ドキュメント | MOC、レポート類 |

### 1.2 抽出可能な再利用モジュール

Plan modeの詳細分析により、以下の**6つの再利用可能モジュール**を特定しました：

#### モジュール候補一覧

| モジュール名 | 抽出元プロジェクト | 機能概要 | iOS互換性 |
|------------|------------------|---------|----------|
| **web-scraper** | researchagent | DuckDuckGo検索、Cheerio HTML解析、リトライ制御 | ✅ 完全対応 |
| **data-structuring** | researchagent | CSV/JSON/Markdown相互変換、テーブル生成 | ✅ 完全対応 |
| **ollama-client** | researchagent | Ollama/OpenAI統一API、ストリーミング対応 | ✅ 完全対応 |
| **webhook-handler** | line-chat-logger | 汎用Webhook受信、署名検証、Express統合 | ✅ 完全対応 |
| **google-sheets-client** | airregi-analytics<br>garoon-sheets-sync | Google Sheets API v4ラッパー、バッチ最適化 | ✅ 完全対応 |
| **jwt-middleware** | lineworks-chat-logger | JWT署名検証ミドルウェア | ✅ 完全対応 |

#### モジュール詳細

##### 1. web-scraper

**抽出元**: `projects/automation/researchagent/src/modules/search.ts`, `fetch.ts`

**API設計例**:
```typescript
export interface ScraperConfig {
  userAgent?: string;
  timeout?: number;
  maxRetries?: number;
}

export class WebScraper {
  constructor(config?: ScraperConfig);
  async search(query: string, options?: SearchOptions): Promise<SearchResult[]>;
  async fetchHTML(url: string): Promise<string>;
  async extractText(html: string, selector: string): Promise<string[]>;
}
```

**依存関係**: axios, cheerio, p-limit

**工数見積**: 3人日

---

##### 2. data-structuring

**抽出元**: `projects/automation/researchagent/src/modules/output.ts`

**API設計例**:
```typescript
export class DataFormatter {
  static toCSV<T>(data: T[]): string;
  static fromCSV<T>(csv: string, schema: z.ZodSchema<T>): T[];
  static toMarkdownTable<T>(data: T[], options?: MarkdownTableOptions): string;
  static toJSON<T>(data: T[]): string;
  static fromJSON<T>(json: string, schema: z.ZodSchema<T>): T[];
}
```

**依存関係**: csv-parse, csv-stringify, zod

**工数見積**: 2人日

---

##### 3. ollama-client

**抽出元**: `projects/automation/researchagent/src/modules/llm.ts`

**API設計例**:
```typescript
export interface LLMConfig {
  provider: 'ollama' | 'openai' | 'anthropic';
  apiKey?: string;
  baseUrl?: string;
  model: string;
}

export class LLMClient {
  constructor(config: LLMConfig);
  async complete(prompt: string, options?: CompletionOptions): Promise<CompletionResponse>;
  async *completeStream(prompt: string, options?: CompletionOptions): AsyncIterable<string>;
}
```

**依存関係**: axios（peerDependencies: openai, @anthropic-ai/sdk）

**工数見積**: 3人日

---

##### 4. webhook-handler

**抽出元**: `projects/communication/line-chat-logger/src/index.js`

**API設計例**:
```typescript
export interface WebhookConfig {
  port?: number;
  path?: string;
  secret?: string;
  signatureHeader?: string;
}

export class WebhookServer {
  constructor(config: WebhookConfig);
  on(event: string, handler: WebhookHandler): void;
  start(): Promise<void>;
  stop(): Promise<void>;
}
```

**依存関係**: express, body-parser

**工数見積**: 2人日

---

##### 5. google-sheets-client

**抽出元**: `projects/integration/garoon-sheets-sync/main.py`, `projects/analytics/airregi-analytics/src/sheets.py`

**API設計例**:
```typescript
export interface SheetsConfig {
  credentials: {
    client_id: string;
    client_secret: string;
    refresh_token: string;
  };
}

export class GoogleSheetsClient {
  constructor(config: SheetsConfig);
  async getValues(spreadsheetId: string, range: string): Promise<any[][]>;
  async updateValues(spreadsheetId: string, range: string, values: any[][]): Promise<void>;
  async appendValues(spreadsheetId: string, range: string, values: any[][]): Promise<void>;
  async batchUpdate(spreadsheetId: string, requests: any[]): Promise<void>;
}
```

**依存関係**: googleapis, google-auth-library

**工数見積**: 4人日（2プロジェクトからの統合）

---

##### 6. jwt-middleware

**抽出元**: `projects/communication/lineworks-chat-logger/src/middleware/jwt.js`

**API設計例**:
```typescript
export interface JWTConfig {
  secret: string;
  algorithms?: string[];
  issuer?: string;
}

export function jwtMiddleware(config: JWTConfig): (req: Request, res: Response, next: NextFunction) => void;
```

**依存関係**: jsonwebtoken, express

**工数見積**: 1人日

---

**合計工数**: 15人日（約3週間）

---

## 2. アーキテクチャ設計

### 2.1 3リポジトリ構造

```
/Users/remma/
│
├── ideas/                              # 【発想・実験リポジトリ】
│   ├── README.md                       # 使い方・品質基準
│   ├── 2024-10-01-projects/automation/dify-n8n-workflow/
│   ├── 2024-10-13-suno-auto-mcp/
│   ├── 2024-10-26-projects/scraping/fc2-video-scraper/
│   ├── 2024-11-01-codex-chatgpt-workflow/
│   ├── wip-obsidian-sync/
│   ├── poc-design-workflow/
│   └── archive/                        # 失敗・放棄プロジェクト
│
├── products/                           # 【本番プロジェクトリポジトリ】
│   ├── README.md                       # 運用ガイドライン
│   ├── data-collection/
│   │   ├── projects/automation/researchagent/
│   │   ├── projects/analytics/airregi-analytics/
│   │   └── projects/finance/crypto-scalping/
│   ├── communication/
│   │   ├── projects/communication/line-chat-logger/
│   │   └── projects/communication/lineworks-chat-logger/
│   └── automation/
│       └── projects/integration/garoon-sheets-sync/
│
└── library/                            # 【再利用モジュールリポジトリ】
    ├── README.md                       # モジュール開発ガイド
    ├── web-scraper/
    ├── data-structuring/
    ├── ollama-client/
    ├── webhook-handler/
    ├── google-sheets-client/
    └── jwt-middleware/
```

### 2.2 品質基準

| リポジトリ | 必須要件 | 推奨要件 | 不要 |
|-----------|---------|---------|------|
| **ideas/** | README.md、ローカル動作確認 | LEARNINGS.md | テスト、CI/CD |
| **products/** | README、.env.example、DEPLOYMENT.md、CHANGELOG、監視設定 | CI/CD、自動テスト | - |
| **library/** | TypeScript型定義、テスト80%+、APIドキュメント、examples、iOS互換性検証 | CI/CD、セキュリティ監査 | - |

---

## 3. iOS Claude Code対応要件

### 3.1 クラウドSandbox制約

| カテゴリ | 制約 | 対策 |
|---------|------|------|
| ネットワーク | HTTP/HTTPS APIのみ | ローカルDB・ファイルシステム使用不可 |
| 状態管理 | セッション間で状態保持不可 | 外部DB/ストレージに委譲 |
| 依存関係 | npm標準パッケージのみ | ネイティブバイナリ不可 |
| ファイルI/O | 一時ファイル（`/tmp`）のみ | 最小限の使用 |
| 環境変数 | Claude Code UIで注入 | `process.env`経由 |

### 3.2 使用可能パッケージ

✅ **推奨**: axios, cheerio, csv-parse, csv-stringify, zod, express, jsonwebtoken, lodash, date-fns

❌ **不可**: puppeteer, sharp, sqlite3, bcrypt, node-gyp, canvas

### 3.3 環境変数管理

```typescript
// 標準パターン（Zod検証）
import { z } from 'zod';

const ConfigSchema = z.object({
  API_KEY: z.string().min(1),
  TIMEOUT: z.coerce.number().default(30000),
  MAX_RETRIES: z.coerce.number().default(3)
});

export function loadConfig() {
  const result = ConfigSchema.safeParse(process.env);
  if (!result.success) {
    throw new Error(`Config error: ${result.error.message}`);
  }
  return result.data;
}
```

---

## 4. 移行計画

### 4.1 フェーズ別スケジュール

| フェーズ | 期間 | 成果物 | 工数 |
|---------|------|--------|------|
| **フェーズ0: 準備** | 1日 | リポジトリ3つ作成、標準ディレクトリ構造 | 0.5人日 |
| **フェーズ1: products/移行** | 1週間 | 本番6プロジェクト移行完了 | 3人日 |
| **フェーズ2: ideas/整理** | 2日 | 実験12プロジェクト整理完了 | 1人日 |
| **フェーズ3: モジュール抽出** | 2週間 | library/6モジュール完成 | 7人日 |
| **フェーズ4: 統合テスト** | 3日 | products/がlibrary/利用開始 | 2人日 |
| **合計** | 約4週間 | 3リポジトリ体制完成 | 13.5人日 |

### 4.2 18プロジェクト移行マッピング

| # | プロジェクト | 目標リポジトリ | 優先度 | 抽出モジュール | 工数 |
|---|------------|--------------|--------|--------------|------|
| 1 | researchagent | products/data-collection/ | 高 | web-scraper, data-structuring, ollama-client | 2日 |
| 2 | line-chat-logger | products/communication/ | 高 | webhook-handler | 1日 |
| 3 | lineworks-chat-logger | products/communication/ | 高 | webhook-handler, jwt-middleware | 1日 |
| 4 | airregi-analytics | products/data-collection/ | 高 | google-sheets-client | 1.5日 |
| 5 | garoon-sheets-sync | products/automation/ | 高 | google-sheets-client | 1.5日 |
| 6 | crypto-scalping | products/data-collection/ | 中 | - | 1日 |
| 7-15 | 実験9プロジェクト | ideas/[date]-[name]/ | 低 | - | 各0.5日 |
| 16 | scripts | library/utilities/ | 中 | 個別判断 | 1日 |

---

## 5. 開発ワークフロー

### 5.1 新規アイデアのプロトタイピング

```bash
# 1. ideas/に新規ディレクトリ
cd ~/ideas
mkdir $(date +%Y-%m-%d)-my-new-idea

# 2. 最小限のREADME作成
echo "# My New Idea" > $(date +%Y-%m-%d)-my-new-idea/README.md

# 3. コーディング開始
cd $(date +%Y-%m-%d)-my-new-idea
npm init -y
```

### 5.2 products/への昇格

**昇格基準**:
- 3回以上再利用された
- ROIが明確
- テストが存在する
- ドキュメントが整備されている

### 5.3 library/モジュール抽出

**抽出基準**:
- 2つ以上のproducts/で同じ機能が実装されている
- 独立したAPIとして定義可能
- iOS Claude Code互換性を満たせる

---

## 6. 成功指標（KPI）

### 定量指標

| KPI | 目標値 | 測定方法 |
|-----|--------|---------|
| モジュール再利用率 | 70%以上 | library/使用products/の割合 |
| コード重複削減 | 40%以上 | 移行前後の重複コード比較 |
| テストカバレッジ（library/） | 80%以上 | Jestカバレッジレポート |
| デプロイ頻度 | 週1回以上 | GitHub Actions実行回数 |
| 平均修復時間（MTTR） | 1時間以内 | 障害からrollback完了まで |
| iOS互換モジュール率 | 100% | library/全モジュールのiOS動作確認 |

### 定性指標

- 新規プロジェクト開発時間50%短縮
- library/モジュールが3つ以上のproducts/で利用される
- iOS Claude Codeで全library/モジュールが動作する
- ドキュメントが整備され、外部開発者が利用可能

---

## 7. リスク管理

| リスク | 影響度 | 確率 | 対策 |
|-------|--------|------|------|
| モジュール抽出時の依存関係複雑化 | 高 | 中 | 段階的抽出、テスト駆動 |
| products/本番への影響 | 高 | 低 | ステージング検証、段階デプロイ |
| iOS互換性問題 | 中 | 中 | 早期検証、代替パッケージ準備 |
| 工数超過 | 中 | 中 | 優先度調整、段階リリース |

---

## 8. 次期アクション

### 今週中に実施

1. **リポジトリ作成**
   ```bash
   mkdir -p ~/workspace/{ideas,products,library}
   cd ~/workspace
   git init
   ```

2. **README.md作成**（各リポジトリ）

3. **web-scraper抽出開始**

### 今月中に完了

- フェーズ1: products/移行完了
- フェーズ2: ideas/整理完了
- モジュール3つ完成（web-scraper, data-structuring, ollama-client）

### 来月以降

- 残りモジュール抽出
- CI/CD整備
- モノレポ構造導入
- 外部公開検討

---

## 9. 承認・合意事項

| 項目 | 承認者 | 承認日 | ステータス |
|------|-------|--------|----------|
| 要件定義書全体 | remma | 2025-11-03 | ✅ 承認済み |
| 3リポジトリモデル | remma | 2025-11-03 | ✅ 承認済み |
| モジュール抽出方針 | remma | 2025-11-03 | ✅ 承認済み |
| iOS互換性要件 | remma | 2025-11-03 | ✅ 承認済み |
| 移行スケジュール（4週間） | remma | 2025-11-03 | ✅ 承認済み |

---

**次のステップ**: この要件定義書を承認後、**フェーズ0（準備）**を開始してください。

```bash
# フェーズ0開始コマンド
mkdir -p ~/workspace/{ideas,products,library}
cd ~/workspace
echo "3リポジトリモデル構築開始" > STATUS.md
```

---

## 変更履歴

| バージョン | 日付 | 変更内容 | 承認者 |
|-----------|------|---------|--------|
| 1.0.0 | 2025-11-03 | 初版作成 | remma |
