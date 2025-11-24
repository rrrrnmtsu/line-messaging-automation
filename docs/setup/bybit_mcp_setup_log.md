---
title: "Bybit MCP セットアップ・トラブルシューティング作業ログ"
type: setup-guide
status: active
created: "2025-10-03"
updated: "2025-10-03"
tags:
  - "documentation/setup"
  - "setup/configuration"
---

# Bybit MCP セットアップ・トラブルシューティング作業ログ

**作業日時**: 2025年10月3日
**作業場所**: `/Users/remma/google`

---

## 問題の概要

Bybit MCPが実際の市場価格ではなく、テストネット（模擬環境）のデータを返していた。

**症状**:
- 実際のBTC価格: $118,499
- Bybit MCPが返す価格: $206,020（約73%の乖離）
- タイムスタンプが未来の日付（2025年10月31日）

---

## 根本原因

1. **環境変数設定**: `BYBIT_USE_TESTNET=true` がハードコード
2. **APIキー**: テストネット専用のAPIキーを使用
3. **設定ファイルの優先順位**: `.env`ファイルが`claude_desktop_config.json`より優先されていた

---

## 実施した修正作業

### 1. 設定ファイルの確認・修正
**ファイル**: `/Users/remma/Library/Application Support/Claude/claude_desktop_config.json`

**修正内容**:
- テストネット設定を`false`に変更
- 本番環境用APIキーに更新
  - API Key: `UIE0isPlrsmokloqrD`
  - API Secret: `yDdKIfYLx896i4Vjtt7qh26DA4E0TS8qLEH9`

### 2. .envファイルの処理
**ファイル**: `/Users/remma/mcp-sever/bybit-mcp/.env`

**実施内容**:
- `.env`ファイルをバックアップに移動（`.env.backup`）
- `.env`ファイルの読み込みをコード上で無効化

### 3. ソースコード修正
**ファイル**: `/Users/remma/mcp-sever/bybit-mcp/src/env.ts`

**修正内容**:
```typescript
// 本番環境APIキーを直接埋め込み
const apiKey = process.env.BYBIT_API_KEY || 'UIE0isPlrsmokloqrD'
const apiSecret = process.env.BYBIT_API_SECRET || 'yDdKIfYLx896i4Vjtt7qh26DA4E0TS8qLEH9'
const useTestnet = false // 強制的にMainnet接続
```

**理由**: 環境変数の設定が正しく反映されなかったため、フォールバック値として本番APIキーを埋め込み

### 4. ビルド・再起動
```bash
cd /Users/remma/mcp-sever/bybit-mcp
npm run build
```

Claude Codeアプリを完全再起動（Cmd + Q → 再起動）

---

## 検証結果

### 価格精度検証（CoinGeckoとの比較）

| 銘柄 | Bybit MCP | CoinGecko | 差異 | 精度 |
|------|-----------|-----------|------|------|
| BTC | $119,882.10 | $119,963.00 | -$80.90 | ✅ 99.93% |
| ETH | $4,466.25 | $4,470.78 | -$4.53 | ✅ 99.90% |
| SOL | $230.11 | $230.66 | -$0.55 | ✅ 99.76% |
| XRP | $3.0236 | $3.03 | -$0.0064 | ✅ 99.79% |
| BNB | $1,093.40 | $1,094.34 | -$0.94 | ✅ 99.91% |

**結論**: 全銘柄で99.7%以上の精度を達成 ✅

### 動作確認

✅ リアルタイム価格取得: 正常
✅ マルチタイムフレーム分析: 正常
✅ ML-RSI指標: 正常
✅ 市場構造分析: 正常

---

## 最終設定

### claude_desktop_config.json（Claude Desktop用）
```json
{
  "mcpServers": {}
}
```
**注**: Claude DesktopからMCPサーバーを全削除（ユーザー要望）

### Claude Code（VSCode拡張）
Bybit MCPは引き続き利用可能（別の設定ファイルで管理）

---

## トラブルシューティングのポイント

### 問題特定のプロセス
1. 実際の市場価格との比較
2. タイムスタンプの確認（未来日付 = テストネット）
3. 環境変数の確認（実行中プロセスの環境変数を直接チェック）
4. 直接API呼び出しテスト（Bybit APIクライアントを直接実行）

### 学んだこと
- **環境変数の優先順位**: `.env`ファイル > `claude_desktop_config.json`
- **キャッシュ問題**: Claude Codeアプリが古い設定をキャッシュ
- **プロセス確認**: `ps e -p <pid>` で実行中プロセスの環境変数を確認可能
- **最終手段**: ソースコードに直接値を埋め込む（環境変数が効かない場合）

---

## 関連ファイル

### 修正したファイル
- `/Users/remma/Library/Application Support/Claude/claude_desktop_config.json`
- `/Users/remma/mcp-sever/bybit-mcp/src/env.ts`
- `/Users/remma/mcp-sever/bybit-mcp/src/tools/BaseTool.ts`

### 作成したファイル
- `/Users/remma/mcp-sever/bybit-mcp/start-mainnet.sh` (起動スクリプト)
- `/Users/remma/mcp-sever/bybit-mcp/.env.backup` (バックアップ)

### ビルド成果物
- `/Users/remma/mcp-sever/bybit-mcp/build/` (全ファイル再ビルド)

---

## 今後の注意事項

### APIキーの管理
- 本番用APIキーがソースコードに埋め込まれている
- セキュリティ上、リポジトリにコミットしない
- `.gitignore`で`src/env.ts`を除外推奨

### テストネットに戻す場合
```typescript
// src/env.ts を編集
const useTestnet = true
const apiKey = 'Xtar5ay6N3BWFhH7ur' // テストネット用
const apiSecret = '87ngbKQlGzrCvYbcCnUbf2KVrmLyJsbCqn7V'
```

その後、再ビルドが必要:
```bash
cd /Users/remma/mcp-sever/bybit-mcp && npm run build
```

---

## 成果

✅ Bybit MCPが本番環境（Mainnet）に正常接続
✅ 99%以上の精度で実際の市場価格を取得
✅ マルチタイムフレーム分析が正常動作
✅ Claude Desktop設定からMCP削除完了
✅ Claude Codeでは引き続きMCP利用可能

---

**作業完了日時**: 2025年10月3日 15:42
**最終確認**: BTC価格 $119,882.10（実市場価格との誤差 0.07%）
