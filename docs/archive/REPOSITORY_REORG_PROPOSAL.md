# リポジトリ整理整頓の提案

現在、リポジトリのルートディレクトリに多数のプロジェクトフォルダが混在しており、視認性や管理のしやすさが低下しています。
以下の構成案にて整理することを提案します。

## 現状の課題
- ルートディレクトリにプロジェクト、ドキュメント、設定ファイルが混在している
- プロジェクトのカテゴリが不明確
- ObsidianのVaultとしての機能と、コードリポジトリとしての機能が混ざっている

## 提案するディレクトリ構成

プロジェクトをカテゴリごとに `projects/` ディレクトリ配下にグループ化し、システムファイルやドキュメントを分離します。

```
/Users/remma/project/
├── _system/                # システム設定、ワークフロー、スクリプト
│   ├── assets/
│   ├── scripts/
│   └── design-workflow/
├── docs/                   # ドキュメント全般
│   ├── MOCs/               # Obsidian MOC (Map of Content)
│   ├── claudecodedocs/
│   └── (その他のドキュメント)
├── lib/                    # 共有ライブラリ
│   └── lib/modules-library/
├── projects/               # 各プロジェクトをカテゴリ別に配置
│   ├── analytics/
│   │   └── projects/analytics/airregi-analytics/
│   ├── automation/
│   │   ├── projects/automation/dify-n8n-workflow/
│   │   ├── projects/automation/gas-automation/
│   │   ├── projects/automation/n8n-workspace/
│   │   ├── projects/automation/researchagent/
│   │   ├── projects/automation/test-taskmaster-demo/
│   │   └── projects/automation/twitter-gas-integration/
│   ├── communication/
│   │   ├── projects/communication/line-chat-logger/
│   │   ├── projects/communication/line-messaging/
│   │   └── projects/communication/lineworks-chat-logger/
│   ├── finance/
│   │   └── projects/finance/crypto-scalping/
│   ├── mobile/
│   │   ├── projects/mobile/ios_claudeworks/
│   │   └── projects/mobile/ios-claude-zapier-integration/
│   ├── scraping/
│   │   ├── projects/scraping/book_ocr/
│   │   └── projects/scraping/fc2-video-scraper/
│   └── integration/
│       ├── projects/integration/garoon-sheets-sync/
│       └── projects/integration/logic-pro-python-integration/
├── .obsidian/              # Obsidian設定（変更なし）
├── Home.md                 # エントリーポイント（ルート維持推奨）
├── README.md               # リポジトリ説明（ルート維持推奨）
└── codex.mcp.local.json    # 設定ファイル（ルート維持推奨）
```

## 実行手順

1. **ディレクトリ作成**: 新しいカテゴリフォルダを作成します。
2. **移動**: 既存のフォルダを新しい場所に移動します。
3. **リンク修正**:
    - `Home.md` や `README.md` 内のリンクを一括置換します。
    - Obsidianのリンクは自動追従する場合もありますが、スクリプト等で絶対パス/相対パスを指定している箇所は修正が必要です。

## 確認事項

- `modules-library` はGitサブモジュールでしょうか？（`.git`が含まれていたため、移動には注意が必要です）
- Obsidianのリンクが切れる可能性がありますが、Obsidian内でファイル移動を行えばリンクは自動更新されます。今回はファイルシステム上で移動するため、Obsidianを開いた際に再インデックスが必要になるか、リンク修正が必要になります。
- CI/CDや自動化スクリプトで、特定のパス（例: `~/project/projects/communication/line-messaging/...`）をハードコードしているものはありますか？

この構成で進めてよろしいでしょうか？
