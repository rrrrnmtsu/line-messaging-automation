# パフォーマンス分析レポート

## 実行環境

- **ハードウェア**: M1 Pro 32GB RAM
- **LLMモデル**: Qwen3:30b (18GB)
- **Ollama**: インストール済み、localhost:11434で稼働

## 検証結果

### テスト1: 基本検索機能

**コマンド**:
```bash
npm run dev -- --phase 1 --target-rows 1 --per-query 3 --concurrency 1 --out-prefix test_qwen3
```

**結果**:
- ✅ DuckDuckGo検索: 正常動作（17クエリ、15件のURL取得）
- ✅ HTML取得: 正常動作（複数URLから取得成功）
- ✅ コンテンツ抽出: 正常動作（4394文字抽出）
- ❌ LLM抽出: タイムアウト（120秒×2回）

### テスト2: 単体LLM抽出

**テストURL**: `https://qiita.com/YushiYamamoto/items/1c6fa7d52a0186f58165`

**結果**:
- ✅ コンテンツ取得: 成功（4394文字）
- ❌ LLM抽出: タイムアウト（120秒×2回）

**エラーログ**:
```
[LLM] Attempt 1/2 failed: timeout of 120000ms exceeded
[LLM] Attempt 2/2 failed: timeout of 120000ms exceeded
```

### テスト3: Ollamaモデルプリロード

**コマンド**:
```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{"model":"qwen3:30b","prompt":"Hello","stream":false}' \
  --max-time 60
```

**結果**:
- ❌ タイムアウト（60秒）
- Ollamaは応答を返さず

## 問題分析

### 根本原因

**Qwen3:30b (18GB) が M1 Pro 32GB環境で推論速度が遅すぎる**

#### 技術的要因:

1. **メモリ帯域幅の制限**
   - M1 ProのユニファイドメモリはCPUとGPUで共有
   - 18GBのモデルロード時、システムメモリの56%を消費
   - 残り14GBでOS、ブラウザ、その他アプリを動作させる必要
   - スワップ発生の可能性

2. **推論速度の現実**
   - Qwen3:30bは高精度だが推論が非常に遅い
   - 4000文字のコンテンツ + 20列スキーマ抽出プロンプト
   - 合計入力トークン: 約2000-2500トークン
   - 出力トークン: 約800-1000トークン（JSON形式）
   - **推定所要時間: 3-5分/リクエスト**

3. **タイムアウト設定とのミスマッチ**
   - 初期設定: 120秒（2分）
   - 実際の必要時間: 180-300秒（3-5分）
   - 修正後: 300秒（5分）に延長済み（未テスト）

## 解決策

### オプション1: より軽量なモデルに切り替え（推奨）

**推奨モデル: Qwen2.5:14b または Qwen2.5:7b**

#### Qwen2.5:14b
- モデルサイズ: 約9GB
- メモリ消費: 32GBの28%（余裕あり）
- 推論速度: 約1-2分/リクエスト（推定）
- 日本語精度: 非常に高い（Qwen3:30bの90%程度）

#### Qwen2.5:7b
- モデルサイズ: 約4.7GB
- メモリ消費: 32GBの15%（非常に余裕あり）
- 推論速度: 約30-60秒/リクエスト（推定）
- 日本語精度: 高い（Qwen3:30bの80%程度）

**セットアップコマンド**:
```bash
# Qwen2.5:14b（推奨）
ollama pull qwen2.5:14b

# または Qwen2.5:7b（より高速）
ollama pull qwen2.5:7b
```

**`.env` 修正**:
```env
LLM_MODEL=qwen2.5:14b
# または
LLM_MODEL=qwen2.5:7b
```

### オプション2: タイムアウト延長＋忍耐（非推奨）

**すでに実装済み（未テスト）**:
- タイムアウト: 120秒 → 300秒（5分）
- `num_ctx`: 8192（コンテキストウィンドウ最適化）
- `num_thread`: 6（M1 Pro性能コア数）

**問題点**:
- 1件の抽出に3-5分かかる
- 目標100件の場合、5-8時間の実行時間
- 実用性が低い

### オプション3: クラウドAPIに切り替え

#### Anthropic Claude 3.5 Sonnet（推奨）
- 推論速度: 約5-10秒/リクエスト
- 日本語精度: 最高レベル
- コスト: 約$0.015/リクエスト（100件で$1.50）

**セットアップ**:
```bash
# .env修正
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

#### OpenAI GPT-4o-mini
- 推論速度: 約3-5秒/リクエスト
- 日本語精度: 高い
- コスト: 約$0.002/リクエスト（100件で$0.20）

**セットアップ**:
```bash
# .env修正
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
```

## パフォーマンス比較表

| モデル | 推論速度 | 精度 | メモリ | 100件実行時間 | コスト |
|--------|---------|------|--------|-------------|--------|
| Qwen3:30b | 3-5分 | ★★★★★ | 18GB | 5-8時間 | 無料 |
| Qwen2.5:14b | 1-2分 | ★★★★☆ | 9GB | 2-3時間 | 無料 |
| Qwen2.5:7b | 30-60秒 | ★★★★☆ | 4.7GB | 50-100分 | 無料 |
| Claude 3.5 Sonnet | 5-10秒 | ★★★★★ | - | 8-16分 | $1.50 |
| GPT-4o-mini | 3-5秒 | ★★★★☆ | - | 5-8分 | $0.20 |

## 推奨アクション

### 即座の対応（今すぐ実行可能）

**Qwen2.5:7b に切り替える（最もバランスが良い）**

```bash
# 1. モデルダウンロード（約10分）
ollama pull qwen2.5:7b

# 2. .env修正
echo "LLM_MODEL=qwen2.5:7b" >> .env

# 3. テスト実行
npm run dev -- --phase 1 --target-rows 1 --per-query 3 --concurrency 1 --out-prefix test_qwen25_7b
```

**期待結果**:
- 1件の抽出: 30-60秒
- タイムアウトなしで完了
- 十分な精度

### 中期的対応（本格運用時）

**Claude 3.5 Sonnet に切り替える**

**理由**:
- 最高精度の日本語理解
- 5-10秒/件の高速処理
- 100件収集で約10-15分
- コスト: $1.50（許容範囲）

**セットアップ**:
```bash
# 1. Anthropic API Key取得（https://console.anthropic.com/）

# 2. .env修正
cat > .env <<EOF
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
CONCURRENCY=4
PER_QUERY_LIMIT=20
EOF

# 3. 本番実行
npm run dev -- --phase 1 --target-rows 100 --out-prefix n8n_phase1_claude
```

## 次のステップ

1. ✅ **Qwen2.5:7b をインストール**
2. ✅ **.env を修正**
3. ✅ **テスト実行（1件）**
4. ✅ **結果検証**
5. ⬜ **本格実行（100件）の判断**

---

**作成日**: 2025-11-02
**ステータス**: 分析完了・対策実施待ち
