---
title: "FC2動画スクレイピングツール - 使用方法"
type: documentation
status: active
created: "2025-10-08"
updated: "2025-10-08"
tags:
  - "project/fc2-video-scraper"
---

# FC2動画スクレイピングツール - 使用方法

## 現状の問題

FC2動画は**非常に強力なボット検出システム**を実装しており、Seleniumを使った自動スクレイピングがブロックされます。

## 推奨される使用方法

### 方法1: 手動ダウンロード + HTMLパーサー（推奨）

1. **ブラウザでFC2動画を検索**
   - https://video.fc2.com/a/ にアクセス
   - 「素人」などのキーワードで検索
   - 検索結果ページを表示

2. **HTMLファイルとして保存**
   - ブラウザで右クリック →「名前を付けてページを保存」
   - 「ウェブページ、完全」を選択
   - ファイル名: `fc2_search_result.html`

3. **HTMLパーサーで解析**
   ```bash
   python html_parser.py fc2_search_result.html
   ```

4. **出力**
   - `output/fc2_videos_YYYYMMDD_HHMMSS.csv` に結果が保存されます

### 方法2: 高度版スクレイパー（成功率低）

FC2のボット検出をすり抜ける可能性は低いですが、試す場合:

```bash
# ヘッドレスモードOFF（ブラウザが表示される）
python scraper_advanced.py
```

**注意**:
- ほぼ確実にエラーページにリダイレクトされます
- CAPTCHA等が表示される可能性があります
- 成功率は非常に低いです

## HTMLパーサーの詳細使用方法

### 基本的な使い方

```bash
# HTMLファイルを解析
python html_parser.py <HTMLファイルパス>

# 出力先を指定
python html_parser.py fc2_search.html output/custom_output.csv
```

### 複数ページの処理

1. ブラウザで検索結果の各ページを保存:
   - `page1.html`
   - `page2.html`
   - `page3.html`

2. すべてのページを解析:
   ```bash
   python html_parser.py page1.html output/page1.csv
   python html_parser.py page2.html output/page2.csv
   python html_parser.py page3.html output/page3.csv
   ```

3. 必要に応じてCSVファイルを統合

## 出力CSVフォーマット

| カラム | 内容 |
|--------|------|
| No | 連番 |
| Title | 動画タイトル |
| URL | 動画URL |
| Thumbnail | サムネイル画像URL |
| Parsed_At | 解析日時 |

## トラブルシューティング

### HTMLパーサーで動画が見つからない

**原因**:
- JavaScriptで動的に読み込まれるコンテンツ
- 保存方法が「HTMLのみ」になっている

**解決策**:
1. ブラウザでページを完全に読み込み（スクロールして全コンテンツ表示）
2. 「名前を付けてページを保存」→「ウェブページ、完全」を選択
3. 再度HTMLパーサーを実行

### Seleniumスクレイパーがエラーページに飛ばされる

**原因**: FC2のボット検出システム

**解決策**:
- 手動ダウンロード + HTMLパーサー方式を使用してください
- 自動化は現状困難です

## 法的・倫理的注意事項

- **FC2利用規約を必ず確認**してください
- スクレイピングが禁止されている場合は実行しないでください
- 取得したデータの二次利用には十分注意してください
- 個人的な調査・研究目的に限定してください
- サーバーに過度な負荷をかけないようにしてください

## 代替案

### 公式API（存在する場合）
FC2が公式APIを提供している場合は、そちらを利用することを強く推奨します。

### RSS Feed
FC2が提供するRSSフィードがあれば、そちらから情報を取得する方が安全です。

### 検索エンジンAPI
Google Custom Search API等を使ってFC2動画を検索する方法もあります（精度は低いですが）。

## まとめ

**現時点での最適な方法**:
1. ブラウザで手動検索
2. HTMLとして保存
3. `html_parser.py` で解析
4. CSVを取得

この方法であれば、FC2のボット検出に引っかからず、確実にデータを取得できます。
