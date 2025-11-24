# Google Drive デザインファイル管理セットアップガイド

## 所要時間: 10分

---

## ステップ1: Google Drive フォルダ作成

### 1-1. メインフォルダ作成

Google Driveにアクセスして、以下のフォルダを作成:

```
📂 project-design-files
```

### 1-2. カテゴリフォルダ作成

`project-design-files/` 内に以下のフォルダを作成:

```
📂 project-design-files/
├── 📁 01_branding
├── 📁 02_ui-design
├── 📁 03_marketing
├── 📁 04_web-assets
└── 📁 archived
```

### 1-3. サブフォルダ作成

各カテゴリフォルダ内に以下を作成:

#### 01_branding/
```
📁 01_branding/
├── 📁 logo
├── 📁 color-palette
└── 📁 typography
```

#### 02_ui-design/
```
📁 02_ui-design/
├── 📁 mockups
├── 📁 components
└── 📁 icons
```

#### 03_marketing/
```
📁 03_marketing/
├── 📁 banners
├── 📁 social-media
└── 📁 print
```

#### 04_web-assets/
```
📁 04_web-assets/
├── 📁 hero-images
├── 📁 backgrounds
└── 📁 illustrations
```

#### archived/
```
📁 archived/
└── 📁 2025-01
```

---

## ステップ2: _INDEX.md ファイル配置

各カテゴリフォルダに `_INDEX.md` を作成（Google Docsまたはテキストファイル）:

### テンプレート

```markdown
# デザインファイル一覧

## 最終更新: YYYY-MM-DD

| ファイル名 | バージョン | ステータス | 作成日 | 最終更新 | 備考 |
|-----------|-----------|-----------|-------|---------|------|
| （ファイルがまだありません） | - | - | - | - | - |

## 書き出し先（Git Repository）
- （まだありません）

## Google Drive リンク
https://drive.google.com/drive/folders/xxxxx

## 関連ドキュメント
- デザインガイドライン: `docs/design-guidelines.md`
```

**配置場所**:
- `01_branding/_INDEX.md`
- `02_ui-design/_INDEX.md`
- `03_marketing/_INDEX.md`
- `04_web-assets/_INDEX.md`

---

## ステップ3: 共有リンク取得

### 3-1. フォルダ共有設定

1. `project-design-files/` フォルダを右クリック
2. 「共有」→「リンクを取得」
3. 権限設定:
   - **編集者**: デザイナー、クリエイター
   - **閲覧者（コメント可）**: クライアント、ステークホルダー
   - **閲覧者**: 開発者

### 3-2. リンクURLをコピー

例: `https://drive.google.com/drive/folders/1A2B3C4D5E6F7G8H9I0J`

---

## ステップ4: Git Repository に assets フォルダ作成

プロジェクトルートで以下を実行（自動実行済み）:

```bash
mkdir -p assets/images/{branding,ui,marketing,web}
touch assets/ASSET_INDEX.md
```

---

## ステップ5: README.md 更新

プロジェクトの `README.md` に以下を追加:

```markdown
## デザインファイル

### Google Drive
デザインファイル（PSD/AI等）はGoogle Driveで管理しています。

- **メインフォルダ**: [project-design-files](https://drive.google.com/drive/folders/xxxxx)
  - ブランディング素材: [01_branding](https://drive.google.com/drive/folders/xxxxx)
  - UI デザイン: [02_ui-design](https://drive.google.com/drive/folders/xxxxx)
  - マーケティング素材: [03_marketing](https://drive.google.com/drive/folders/xxxxx)
  - Web素材: [04_web-assets](https://drive.google.com/drive/folders/xxxxx)

### 命名規則
詳細は [DESIGN_FILE_MANAGEMENT.md](./DESIGN_FILE_MANAGEMENT.md) を参照

### アクセス権限
デザインファイルの閲覧・編集権限が必要な場合は、プロジェクトリーダーに連絡してください。
```

---

## ステップ6: デザインガイドライン作成（オプション）

`docs/design-guidelines.md` を作成して、デザイン仕様を文書化:

```markdown
# デザインガイドライン

## ブランドカラー
- Primary: #1A73E8
- Secondary: #34A853
- Accent: #FBBC04

## タイポグラフィ
- 見出し: Noto Sans JP Bold
- 本文: Noto Sans JP Regular

## ロゴ使用規則
- 最小サイズ: 48px × 48px
- 余白: 上下左右 16px以上
- 背景色: 白または #F5F5F5 推奨

## デザインファイル保管場所
Google Drive: [リンク]
```

---

## チェックリスト

セットアップ完了確認:

- [ ] Google Drive に `project-design-files/` フォルダを作成
- [ ] カテゴリ別サブフォルダを作成（01_branding等）
- [ ] `archived/2025-01/` フォルダを作成
- [ ] 各フォルダに `_INDEX.md` を配置
- [ ] 共有リンクを取得
- [ ] Git Repository に `assets/images/` フォルダを作成
- [ ] `README.md` にGoogle Driveリンクを追加
- [ ] チームメンバーに命名規則を共有

---

## トラブルシューティング

### Q: Google Driveのフォルダが多すぎて管理しづらい
**A**: 必要なカテゴリのみ作成してください。最小構成:
```
📂 project-design-files/
├── 📁 design
└── 📁 archived
```

### Q: _INDEX.md の更新が面倒
**A**: 重要なプロジェクトのみ更新、小規模プロジェクトは省略可

---

**作成日**: 2025-01-10
**所要時間**: 約10分
