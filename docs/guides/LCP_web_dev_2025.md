---
title: "LCP（Largest Contentful Paint）完全ガイド - web.dev 2025年版"
type: documentation
status: active
created: "2025-10-21"
updated: "2025-10-21"
tags:
---

# LCP（Largest Contentful Paint）完全ガイド - web.dev 2025年版

**調査日**: 2025-10-21
**情報源**: web.dev公式ドキュメント

---

## 1. LCPの定義と重要性

### LCPとは
**Largest Contentful Paint（最大コンテンツ描画時間）**は、ページ読み込み開始時点から、ビューポート内で最大の画像・テキストブロック・動画がレンダリングされるまでの時間を測定する指標です。

### なぜ重要か
- **体感的な読み込み速度**を示す最も重要な指標
- ユーザーがページのメインコンテンツを実際に見られるタイミングを測定
- **Core Web Vitals**の中核指標（SEO・UXに直接影響）
- ページが実際に「使える状態」になったと感じるポイントを示す

---

## 2. 推奨値・閾値（2025年版）

| 評価カテゴリー | LCP値 | 説明 |
|----------------|-------|------|
| **Good（良好）** | **≤ 2.5秒** | 目標とすべき基準値 |
| **Needs Improvement（要改善）** | 2.5〜4.0秒 | 改善の余地あり |
| **Poor（不良）** | > 4.0秒 | 早急な対策が必要 |

### 測定基準
- **75パーセンタイル値**で評価（訪問の75%が達成する値）
- モバイル・デスクトップで個別に測定
- **2025年現在も2.5秒基準は変更なし**

---

## 3. LCP改善のベストプラクティス（優先順位順）

### ❶ リソース読み込み遅延の排除（最重要）
**効果**: 最大の改善インパクト
**目標**: LCP要素の読み込み開始を可能な限り早める

#### 具体的施策
```html
<!-- LCP画像のプリロード -->
<link rel="preload" as="image" href="/hero-image.jpg" fetchpriority="high">
```

- `fetchpriority="high"` 属性の活用
- Above-the-fold画像に `loading="lazy"` を使わない
- クリティカルパス上のリソース優先度を上げる
- 不要なJavaScriptの遅延実行

---

### ❷ TTFB（Time to First Byte）の改善
**効果**: サーバー応答時間の短縮

#### 具体的施策
- **CDN導入**: ユーザーに近いエッジサーバーから配信
- **サーバーサイドキャッシュ**: Redis/Memcached等の活用
- **データベース最適化**: クエリ改善・インデックス追加
- **SSR最適化**: サーバーサイドレンダリングの高速化
- **HTTP/3対応**: より高速なプロトコルの採用

---

### ❸ リソース発見と優先順位の最適化
**効果**: クリティカルリソースを優先的に読み込む

#### 具体的施策
- 非クリティカルリソースの遅延読み込み
- Below-the-fold画像のlazyload適用
- サードパーティスクリプトの最適化
- リソースヒントの活用（preconnect, dns-prefetch）
- 不要なリダイレクトの削除

---

### ❹ レンダリング作業の削減
**効果**: ブラウザの処理負荷軽減

#### 具体的施策
- **DOMサイズの削減**: 不要な要素の削除
- **CSSの最適化**: 未使用CSSの削除、クリティカルCSS抽出
- **JavaScriptの最適化**: バンドルサイズ削減、コード分割
- **レイアウト再計算の最小化**: CSSアニメーションの最適化

---

## 4. 2024-2025年の最新動向と重要発見

### 🔥 従来の常識を覆す新事実

web.devの最新分析により、LCP最適化の常識が大きく変わりました。

#### 従来の誤解
❌ **「画像圧縮・最適化がLCP改善の最重要施策」**

#### 実際の真実
✅ **「リソース読み込み遅延の排除が最重要」**

---

### データで見る実態

**LCPが不良なサイトの分析結果**:
```
TTFBからLCP画像リクエストまでの待機時間: 1.3秒 ⚠️
実際の画像ダウンロード時間: 0.3〜0.4秒

→ 待機時間が実ダウンロードの約4倍!
```

#### 重要な洞察
> "When looking at field performance data for users in Chrome, **image download time is almost never the bottleneck**. Instead, other parts of LCP are a much bigger problem."
>
> （Chromeのフィールドデータ分析では、画像ダウンロード時間はほぼボトルネックになっておらず、LCPの他の要素が遥かに大きな問題である）

---

### 先進的な改善手法

#### bfcache（Back/Forward Cache）の活用
**効果**: 戻る/進むボタンでの遷移を瞬時に実行

```javascript
// bfcacheの適合性チェック
window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    console.log('ページがbfcacheから復元されました');
  }
});
```

**メリット**:
- ページをメモリスナップショットから即座に復元
- LCPを実質ゼロにできる
- ユーザー体験の劇的な向上

**注意点**:
- `unload`イベントの使用は避ける
- 永続的な接続（WebSocket等）の適切な処理
- セッション状態の管理

---

## 5. LCP最適化の実践フロー

### Step 1: 現状把握
```bash
# Chrome DevToolsでの確認
1. DevTools > Lighthouse > パフォーマンス測定
2. "Largest Contentful Paint" の値を確認
3. LCP要素を特定（どの画像/テキストか）
```

**推奨ツール**:
- Chrome DevTools（Lighthouse）
- PageSpeed Insights
- Chrome User Experience Report（CrUX）
- Web Vitals Chrome拡張

---

### Step 2: ボトルネック特定

LCPを4つの要素に分解:
```
LCP = TTFB + リソース読み込み遅延 + リソースダウンロード時間 + 要素レンダリング時間
```

**分析方法**:
```javascript
// Performance APIでLCP詳細を取得
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime);
  console.log('LCP要素:', lastEntry.element);
}).observe({type: 'largest-contentful-paint', buffered: true});
```

---

### Step 3: 優先順位付けと実装

#### 優先度A（即実施）
1. **リソース読み込み遅延の排除**
   - LCP画像のpreload設定
   - fetchpriority属性の追加
   - 不要なlazyloadの削除

#### 優先度B（早期実施）
2. **TTFB改善**
   - CDN導入・最適化
   - サーバーキャッシュ強化

#### 優先度C（中長期）
3. **リソース最適化**
   - 画像形式の最新化（WebP, AVIF）
   - 画像圧縮
   - レスポンシブ画像対応

---

### Step 4: 継続的モニタリング

**フィールドデータ（実ユーザー測定）**:
```javascript
// web-vitals ライブラリ使用
import {onLCP} from 'web-vitals';

onLCP((metric) => {
  // 分析ツールに送信
  sendToAnalytics({
    name: metric.name,
    value: metric.value,
    id: metric.id,
  });
});
```

**KPI設定例**:
- 75パーセンタイル値 ≤ 2.5秒
- モバイル・デスクトップ別々に測定
- 週次/月次でトレンド分析

---

## 6. よくある間違いと対策

### ❌ 間違い1: LCP画像にlazyload適用
```html
<!-- NG: Above-the-foldの画像に遅延読み込み -->
<img src="hero.jpg" loading="lazy" alt="Hero">
```

### ✅ 正解: 優先読み込み設定
```html
<!-- OK: プリロード + 優先度設定 -->
<link rel="preload" as="image" href="hero.jpg" fetchpriority="high">
<img src="hero.jpg" alt="Hero">
```

---

### ❌ 間違い2: 画像最適化のみに注力
- 画像圧縮だけでは不十分
- リソース読み込み遅延が最大のボトルネック

### ✅ 正解: 全体的なアプローチ
1. リソース読み込み遅延排除（最優先）
2. TTFB改善
3. その後に画像最適化

---

### ❌ 間違い3: Labデータのみで判断
- Lighthouse等のLab測定だけでは不十分
- 実ユーザーの環境を反映していない

### ✅ 正解: Field + Lab両方で評価
- **Fieldデータ**: 実ユーザーの測定値（CrUX）
- **Labデータ**: 開発環境での測定（Lighthouse）
- 両方を組み合わせて総合判断

---

## 7. チェックリスト

### 基本設定
- [ ] LCP要素を特定済み
- [ ] 現在のLCP値を測定済み（Field + Lab）
- [ ] ボトルネック箇所を分析済み

### リソース読み込み
- [ ] LCP画像にpreload設定
- [ ] fetchpriority="high" 設定
- [ ] Above-the-fold画像のlazyload削除
- [ ] 不要なJavaScriptの遅延実行

### サーバー最適化
- [ ] CDN導入済み
- [ ] TTFB < 600ms 達成
- [ ] HTTP/2以上使用
- [ ] gzip/Brotli圧縮有効

### リソース最適化
- [ ] 次世代画像フォーマット使用（WebP, AVIF）
- [ ] レスポンシブ画像実装
- [ ] 画像サイズ最適化
- [ ] 未使用CSS削除

### モニタリング
- [ ] Web Vitals測定実装
- [ ] Real User Monitoring（RUM）導入
- [ ] 定期的なパフォーマンス測定
- [ ] bfcache対応確認

---

## 8. 参考リソース

### 公式ドキュメント
- [Largest Contentful Paint (LCP) - web.dev](https://web.dev/articles/lcp)
- [Optimize Largest Contentful Paint - web.dev](https://web.dev/articles/optimize-lcp)
- [Common misconceptions about LCP - web.dev](https://web.dev/blog/common-misconceptions-lcp)
- [Lighthouse LCP - Chrome Developers](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-largest-contentful-paint)

### 測定ツール
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Chrome User Experience Report](https://developers.google.com/web/tools/chrome-user-experience-report)
- [web-vitals JavaScript library](https://github.com/GoogleChrome/web-vitals)

---

## 9. まとめ

### 最重要ポイント
1. **目標値**: 2.5秒以内（75パーセンタイル）
2. **最優先施策**: リソース読み込み遅延の排除
3. **測定**: Field + Lab両方で継続的に評価
4. **誤解を解く**: 画像最適化だけでは不十分

### 戦略的アプローチ
```
計測 → 分析 → 優先順位付け → 実装 → 継続的モニタリング
```

LCP改善は単一施策では不十分です。**ページ読み込みプロセス全体を最適化**し、ユーザー体験の向上とSEO効果の両方を実現してください。

---

**Last Updated**: 2025-10-21
**Source**: web.dev official documentation
