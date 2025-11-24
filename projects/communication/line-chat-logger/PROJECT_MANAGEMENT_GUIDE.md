---
title: "LINE Chat Logger - プロジェクト管理ガイド"
type: documentation
status: active
created: "2025-10-08"
updated: "2025-10-08"
tags:
  - "project/line-chat-logger"
---

# LINE Chat Logger - プロジェクト管理ガイド

## 📋 概要

LINEのトーク内容からAIが自動的に以下を抽出・分析します：

- **タスク抽出** - 「〇〇を実装する」「△△を確認」などのアクションアイテム
- **進捗把握** - 「完了しました」「進行中」などのステータス
- **ボトルネック検出** - 「困っている」「うまくいかない」などの課題
- **リスク検出** - 「遅延」「バグ発生」「問題」などのリスク要因
- **優先度判定** - 「緊急」「重要」などから優先度を自動判定

---

## 🎯 使い方

### 1. 通常通りLINEでやりとり

プロジェクトのグループチャットで自然に会話するだけでOK。

**例**:
```
山田: 認証機能を実装する予定です
佐藤: 了解です。明日までにデザインレビュー完了します
田中: ちょっと困っています。APIのエラーが解決できません
```

### 2. 自動分析

各メッセージがリアルタイムで分析され、以下が抽出されます：

**山田さんのメッセージ** →
- タスク: 「認証機能を実装」
- 優先度: low

**佐藤さんのメッセージ** →
- タスク: 「デザインレビュー」
- 進捗: pending

**田中さんのメッセージ** →
- ボトルネック検出: severity: medium
- キーワード: 「困っている」「エラー」「解決できない」

---

## 📊 ダッシュボードAPI

### エンドポイント

```
https://line-message-logger.vercel.app/dashboard
```

### 使用例

#### 全体ダッシュボード取得
```bash
curl https://line-message-logger.vercel.app/dashboard
```

**レスポンス例**:
```json
{
  "success": true,
  "actionItems": [...],
  "dashboard": {
    "total_messages": 150,
    "action_items_count": 25,
    "critical_count": 3,
    "high_priority_count": 8,
    "bottleneck_count": 5,
    "risk_count": 4
  },
  "groups": [...]
}
```

#### アクションアイテムのみ取得
```bash
curl "https://line-message-logger.vercel.app/dashboard?type=action-items"
```

#### 特定グループのダッシュボード
```bash
curl "https://line-message-logger.vercel.app/dashboard?type=dashboard&groupId=GROUP_ID&days=7"
```

---

## 🗄️ データベース確認

### Neon SQLエディタで確認

#### アクションアイテム一覧
```sql
SELECT
  user_name,
  tasks,
  priority,
  bottleneck,
  risks,
  timestamp
FROM project_analysis
WHERE has_action_items = TRUE
ORDER BY priority DESC, timestamp DESC
LIMIT 20;
```

#### 優先度別集計
```sql
SELECT
  priority,
  COUNT(*) as count
FROM project_analysis
WHERE has_action_items = TRUE
GROUP BY priority
ORDER BY
  CASE priority
    WHEN 'critical' THEN 1
    WHEN 'high' THEN 2
    WHEN 'medium' THEN 3
    WHEN 'low' THEN 4
  END;
```

#### ボトルネック検出
```sql
SELECT
  user_name,
  group_name,
  bottleneck->>'severity' as severity,
  bottleneck->>'keywords' as keywords,
  timestamp
FROM project_analysis
WHERE bottleneck->>'detected' = 'true'
ORDER BY timestamp DESC;
```

#### リスク分析
```sql
SELECT
  group_name,
  jsonb_array_elements(risks)->>'category' as risk_category,
  jsonb_array_elements(risks)->>'severity' as severity,
  COUNT(*) as count
FROM project_analysis
WHERE risks != '[]'::jsonb
GROUP BY group_name, risk_category, severity
ORDER BY count DESC;
```

#### グループ別進捗サマリー
```sql
SELECT
  group_name,
  COUNT(*) as total_messages,
  COUNT(CASE WHEN has_action_items THEN 1 END) as action_items,
  COUNT(CASE WHEN bottleneck->>'detected' = 'true' THEN 1 END) as bottlenecks,
  AVG(CASE priority
    WHEN 'critical' THEN 4
    WHEN 'high' THEN 3
    WHEN 'medium' THEN 2
    WHEN 'low' THEN 1
  END) as avg_priority
FROM project_analysis
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY group_name
ORDER BY avg_priority DESC;
```

---

## 🔍 AI分析の詳細

### タスク抽出パターン

以下のパターンでタスクを自動検出：

- 「〇〇を実装する」
- 「△△を確認する」
- 「××をテストする」
- 「TODO: 〇〇」
- 「〇〇をお願いします」

### 進捗ステータス

- **completed**: 「完了」「終わった」「done」
- **in_progress**: 「進行中」「作業中」「対応中」
- **blocked**: 「困っている」「ブロック」「待ち」
- **pending**: 「未着手」「これから」

### ボトルネック検出キーワード

- 「困っている」「問題」「課題」
- 「うまくいかない」「エラー」「動かない」
- 「分からない」「詰まっている」「難しい」

### リスクカテゴリ

- **schedule**: 遅れ、遅延、間に合わない、期限
- **technical**: バグ、エラー、不具合、障害
- **resource**: 人手不足、リソース、時間が足りない
- **quality**: 品質、テスト失敗、仕様違い

### 優先度判定

- **critical**: 緊急 + 重要
- **high**: 緊急 または ASAP、至急
- **medium**: 重要、必須
- **low**: その他

---

## 💡 活用例

### 1. 毎朝のスタンドアップ準備

```sql
-- 前日のアクションアイテム確認
SELECT user_name, tasks, priority
FROM project_analysis
WHERE has_action_items = TRUE
  AND timestamp >= NOW() - INTERVAL '1 day'
ORDER BY priority DESC;
```

### 2. ボトルネック早期発見

```sql
-- ボトルネック発生中のメンバー特定
SELECT
  user_name,
  COUNT(*) as bottleneck_count,
  array_agg(DISTINCT jsonb_array_elements_text(bottleneck->'keywords')) as common_issues
FROM project_analysis
WHERE bottleneck->>'detected' = 'true'
  AND timestamp >= NOW() - INTERVAL '3 days'
GROUP BY user_name
ORDER BY bottleneck_count DESC;
```

### 3. リスク管理

```sql
-- 高リスク項目の抽出
SELECT
  group_name,
  user_name,
  jsonb_array_elements(risks) as risk_detail,
  timestamp
FROM project_analysis
WHERE jsonb_array_elements(risks)->>'severity' = 'high'
ORDER BY timestamp DESC;
```

### 4. タスク進捗レポート

```sql
-- 週次タスク完了率
SELECT
  DATE(timestamp) as date,
  COUNT(*) as total_tasks,
  COUNT(CASE WHEN progress = 'completed' THEN 1 END) as completed_tasks,
  ROUND(
    COUNT(CASE WHEN progress = 'completed' THEN 1 END)::numeric /
    COUNT(*)::numeric * 100,
    2
  ) as completion_rate
FROM project_analysis
WHERE timestamp >= NOW() - INTERVAL '7 days'
  AND jsonb_array_length(tasks) > 0
GROUP BY DATE(timestamp)
ORDER BY date;
```

---

## 🛠️ カスタマイズ

### 検出キーワードの追加

[api/lib/ai-analyzer.js](file:///Users/remma/line-chat-logger/api/lib/ai-analyzer.js) を編集：

```javascript
// ボトルネック検出キーワード追加例
const bottleneckKeywords = [
  '困っている', '問題', '課題',
  // 追加
  'ヘルプ', '相談', 'アドバイスください'
];
```

### リスクカテゴリ追加

```javascript
const riskPatterns = {
  schedule: ['遅れ', '遅延', '間に合わない'],
  technical: ['バグ', 'エラー', '不具合'],
  resource: ['人手不足', 'リソース'],
  quality: ['品質', 'テスト失敗'],
  // 新規追加
  communication: ['連絡がない', '情報不足', '共有されていない']
};
```

---

## 📈 次のステップ

### 推奨機能拡張

1. **Slackへの通知連携**
   - 高優先度タスク検出時に自動通知
   - リスク検出時のアラート

2. **週次レポート自動生成**
   - プロジェクト進捗サマリー
   - ボトルネック・リスク一覧

3. **ダッシュボードUI作成**
   - グラフ表示
   - リアルタイム更新

4. **自然言語クエリ**
   - 「今週の重要タスクは?」
   - 「ボトルネックになっているメンバーは?」

---

**作成日**: 2025-10-08
**バージョン**: 1.0.0
