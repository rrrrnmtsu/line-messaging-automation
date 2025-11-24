# デザインファイル管理規則

## 基本方針

### 管理場所
- **元ファイル（PSD/AI等）**: Google Drive
- **書き出し画像（PNG/JPG/SVG等）**: Git Repository
- **デザイン仕様書**: Git Repository（Markdown形式）

---

## Google Drive ディレクトリ構造

```
📂 Google Drive/
└── 📁 project-design-files/
    ├── 📁 01_branding/
    │   ├── logo/
    │   ├── color-palette/
    │   └── typography/
    ├── 📁 02_ui-design/
    │   ├── mockups/
    │   ├── components/
    │   └── icons/
    ├── 📁 03_marketing/
    │   ├── banners/
    │   ├── social-media/
    │   └── print/
    ├── 📁 04_web-assets/
    │   ├── hero-images/
    │   ├── backgrounds/
    │   └── illustrations/
    ├── 📁 archived/
    │   └── YYYY-MM/
    └── 📄 _INDEX.md
```

---

## ファイル命名規則

### 基本フォーマット

```
[カテゴリ]_[プロジェクト名]_[内容]_[バージョン]_[ステータス].[拡張子]

例:
branding_logo_primary_v1.2_final.ai
ui_dashboard_header_v2.0_wip.psd
marketing_banner_summer-sale_v1.0_approved.psd
```

### 命名規則詳細

#### 1. カテゴリ（必須）
| カテゴリ | 説明 | 例 |
|---------|------|-----|
| `branding` | ロゴ・ブランディング素材 | `branding_logo_` |
| `ui` | UIデザイン・モックアップ | `ui_dashboard_` |
| `marketing` | マーケティング素材 | `marketing_banner_` |
| `web` | Webサイト用素材 | `web_hero-image_` |
| `print` | 印刷物 | `print_flyer_` |
| `social` | SNS用素材 | `social_instagram-post_` |
| `icon` | アイコンセット | `icon_navigation_` |
| `illust` | イラスト | `illust_character_` |

#### 2. プロジェクト名（任意）
- 複数プロジェクトがある場合に使用
- ケバブケース（`-`区切り）推奨

```
ui_airregi-analytics_dashboard_v1.0.psd
marketing_line-logger_banner_v1.0.ai
```

#### 3. 内容（必須）
- ファイルの具体的な内容を簡潔に記述
- ケバブケース推奨
- 日本語不可（英語のみ）

```
✅ Good:
- header-navigation
- user-profile-card
- cta-button-primary

❌ Bad:
- ヘッダーナビゲーション
- design1
- untitled-2
```

#### 4. バージョン（必須）

**セマンティックバージョニング採用**:
```
v[メジャー].[マイナー]

例:
v1.0 - 初稿
v1.1 - マイナー修正（色調整、微調整）
v2.0 - 大幅変更（レイアウト変更、コンセプト変更）
```

**バージョンアップ基準**:
- **メジャー更新（v1.0 → v2.0）**:
  - レイアウト・構造の大幅変更
  - デザインコンセプトの変更
  - クライアント/ステークホルダーレビュー後の大改修

- **マイナー更新（v1.0 → v1.1）**:
  - 色・フォントの微調整
  - テキスト修正
  - 軽微なレイアウト調整

#### 5. ステータス（必須）

| ステータス | 説明 | 使用タイミング |
|-----------|------|---------------|
| `wip` | Work In Progress - 作業中 | デザイン作業中 |
| `review` | レビュー待ち | 確認依頼時 |
| `feedback` | フィードバック反映中 | 修正指示受領後 |
| `approved` | 承認済み | クライアント/上長承認後 |
| `final` | 最終版（確定） | 納品・実装確定版 |
| `archived` | アーカイブ | 不採用案・過去版 |

#### 6. 拡張子

| 拡張子 | ツール | 用途 |
|-------|--------|------|
| `.psd` | Photoshop | 写真加工、UI詳細デザイン |
| `.ai` | Illustrator | ロゴ、ベクター素材 |
| `.sketch` | Sketch | UI/UXデザイン |
| `.fig` | Figma | UI/UXデザイン（ローカル保存時） |
| `.xd` | Adobe XD | プロトタイピング |
| `.indd` | InDesign | 印刷物レイアウト |

---

## 命名例

### ✅ 良い例

```
branding_logo_primary_v1.0_wip.ai
branding_logo_primary_v1.1_review.ai
branding_logo_primary_v1.2_approved.ai
branding_logo_primary_v1.2_final.ai

ui_dashboard_header_v1.0_wip.psd
ui_dashboard_header_v2.0_feedback.psd
ui_dashboard_header_v2.1_final.psd

marketing_banner_summer-sale_v1.0_review.psd
marketing_banner_summer-sale_v1.1_approved.psd

web_hero-image_top-page_v1.0_final.psd

social_instagram-post_campaign-01_v1.0_approved.psd
```

### ❌ 悪い例

```
❌ デザイン最終版2.psd          （日本語、バージョン不明確）
❌ logo_final_FINAL_v3.ai       （finalが重複、バージョン矛盾）
❌ untitled-1.psd                （内容不明）
❌ design-0324.ai                （日付のみ、内容不明）
❌ バナー修正版.psd              （日本語、バージョン不明）
```

---

## バージョン管理ワークフロー

### 1. 新規デザイン作成時

```
1. ファイル作成
   branding_logo_primary_v1.0_wip.ai

2. 初稿完成 → レビュー依頼
   branding_logo_primary_v1.0_review.ai

3. フィードバック反映
   branding_logo_primary_v1.1_feedback.ai

4. 承認取得
   branding_logo_primary_v1.1_approved.ai

5. 最終版確定
   branding_logo_primary_v1.1_final.ai
```

### 2. 既存デザイン修正時

```
元ファイル:
branding_logo_primary_v1.1_final.ai

↓ 大幅リニューアルの場合
branding_logo_primary_v2.0_wip.ai
branding_logo_primary_v2.0_review.ai
branding_logo_primary_v2.0_final.ai

↓ 軽微な修正の場合
branding_logo_primary_v1.2_wip.ai
branding_logo_primary_v1.2_final.ai
```

### 3. 不採用案のアーカイブ

```
元ファイル:
ui_dashboard_header_v2.0_wip.psd

↓ 不採用が決定した場合
archived/2025-01/ui_dashboard_header_v2.0_archived.psd
```

---

## Google Drive 運用ルール

### ファイル保存場所

#### 現行版（作業中・最新版）
```
📁 project-design-files/
└── 📁 01_branding/
    └── 📁 logo/
        ├── branding_logo_primary_v1.2_final.ai      ← 最終版
        ├── branding_logo_primary_v1.1_approved.ai   ← 承認済み旧版（参考用）
        └── branding_logo_primary_v2.0_wip.ai        ← 次バージョン作業中
```

#### アーカイブ（過去版・不採用案）
```
📁 archived/
└── 📁 2025-01/
    ├── branding_logo_primary_v1.0_wip.ai
    ├── branding_logo_primary_v1.0_review.ai
    └── ui_dashboard_header_v1.0_archived.psd
```

### アーカイブルール

**以下の場合にアーカイブ**:
1. 新しいメジャーバージョンが確定した場合（旧バージョンを月次でアーカイブ）
2. 不採用が決定したデザイン案
3. 3ヶ月以上更新がないWIP/Review状態のファイル

**アーカイブ手順**:
```
1. archived/YYYY-MM/ フォルダを作成
2. 対象ファイルを移動
3. ステータスを _archived に変更（不採用案のみ）
4. _INDEX.md を更新
```

---

## 書き出しファイル管理（Git Repository）

### ディレクトリ構造

```
📁 project/ (Git)
└── 📁 assets/
    ├── 📁 images/
    │   ├── 📁 branding/
    │   │   ├── logo-primary.png
    │   │   ├── logo-primary.svg
    │   │   └── logo-secondary.png
    │   ├── 📁 ui/
    │   │   ├── header-background.jpg
    │   │   └── hero-image.png
    │   └── 📁 marketing/
    │       └── banner-summer-sale.jpg
    └── 📄 ASSET_INDEX.md
```

### 書き出しファイル命名規則

**シンプル化（バージョン番号不要）**:
```
[カテゴリ]-[内容].[拡張子]

例:
logo-primary.png
logo-primary.svg
header-background.jpg
banner-summer-sale.jpg
icon-search.svg
```

**理由**:
- Git自体がバージョン管理するため、ファイル名にバージョン番号は不要
- 実装時のパス指定がシンプルになる
- 更新時は同名ファイルで上書き

---

## _INDEX.md 管理

各ディレクトリに `_INDEX.md` を配置して、ファイル一覧と概要を記録

### テンプレート

```markdown
# デザインファイル一覧

## 最終更新: YYYY-MM-DD

| ファイル名 | バージョン | ステータス | 作成日 | 最終更新 | 備考 |
|-----------|-----------|-----------|-------|---------|------|
| branding_logo_primary_v1.2_final.ai | v1.2 | final | 2025-01-01 | 2025-01-15 | メインロゴ確定版 |
| branding_logo_primary_v2.0_wip.ai | v2.0 | wip | 2025-01-20 | 2025-01-25 | リニューアル案作成中 |

## 書き出し先（Git Repository）
- `assets/images/branding/logo-primary.png` (300x300, 透過PNG)
- `assets/images/branding/logo-primary.svg` (ベクター)

## Google Drive リンク
https://drive.google.com/drive/folders/xxxxx

## 関連ドキュメント
- デザインガイドライン: `docs/design-guidelines.md`
- ブランドガイド: `docs/brand-guide.md`
```

---

## Git Repository でのデザイン管理

### docs/design-guidelines.md（推奨）

デザイン仕様をMarkdownで記録:

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

## ファイル共有・権限管理

### Google Drive 権限設定

| 役割 | 権限 | 対象者 |
|-----|------|--------|
| **オーナー** | 完全アクセス（編集・削除・共有） | プロジェクトリーダー |
| **編集者** | 編集・コメント | デザイナー、クリエイター |
| **閲覧者（コメント可）** | 閲覧・コメント | クライアント、ステークホルダー |
| **閲覧者** | 閲覧のみ | 開発者、マーケター（参照用） |

### 共有リンク管理

**プロジェクトREADME.mdに記載**:
```markdown
## デザインファイル

### Google Drive
- ブランディング素材: [リンク]
- UI デザイン: [リンク]
- マーケティング素材: [リンク]

### アクセス権限
デザインファイルの閲覧・編集権限が必要な場合は、
プロジェクトリーダーに連絡してください。
```

---

## バックアップ・災害対策

### 自動バックアップ（Google Drive標準機能）
- Google Driveは自動的にバージョン履歴を保持（30日間）
- 誤削除・上書きの場合は「バージョン履歴」から復元可能

### ローカルバックアップ（推奨）
- 重要なファイルは月次でローカルHDDにもバックアップ
- Time Machine等でMac全体のバックアップも併用

### アーカイブポリシー
- 確定版（final）は必ず `archived/YYYY-MM/` に月次アーカイブ
- 3ヶ月以上未更新のWIP/Reviewファイルも自動アーカイブ

---

## チェックリスト

### デザイン作成時
- [ ] ファイル名が命名規則に従っているか
- [ ] バージョン番号が正しいか
- [ ] ステータスが適切か
- [ ] Google Driveの正しいフォルダに保存されているか
- [ ] _INDEX.md を更新したか

### レビュー依頼時
- [ ] ステータスを `_review` に変更
- [ ] 共有リンクを関係者に送付
- [ ] 期限を明記（例: 3営業日以内）

### 承認・確定時
- [ ] ステータスを `_approved` または `_final` に変更
- [ ] 書き出しファイルをGitにコミット
- [ ] ASSET_INDEX.md を更新
- [ ] _INDEX.md を更新

### アーカイブ時
- [ ] archived/YYYY-MM/ に移動
- [ ] ステータスを `_archived` に変更（不採用案）
- [ ] _INDEX.md を更新

---

## トラブルシューティング

### Q1: 同じファイル名で複数バージョンが存在する
**A**: バージョン番号とステータスで区別してください

```
✅ 正しい管理:
branding_logo_primary_v1.2_final.ai     ← 確定版
branding_logo_primary_v2.0_wip.ai       ← 次バージョン作業中
```

### Q2: 「final」が複数ある
**A**: 基本的に1つのプロジェクトに対して1つの「final」のみ

```
❌ 避けるべき:
logo_v1.0_final.ai
logo_v1.0_final_real.ai
logo_v1.0_final_FINAL.ai

✅ 正しい運用:
branding_logo_primary_v1.0_final.ai  （過去版）
branding_logo_primary_v2.0_final.ai  ← 最新の確定版
```

### Q3: ファイル名が長すぎる
**A**: プロジェクト名を省略、または短縮形を使用

```
❌ 長すぎる:
ui_airregi-analytics-dashboard-system_header-navigation-component_v1.0_wip.psd

✅ 改善:
ui_airregi_header-nav_v1.0_wip.psd
```

---

## 運用開始チェックリスト

- [ ] Google Drive に `project-design-files/` フォルダを作成
- [ ] カテゴリ別サブフォルダを作成（01_branding等）
- [ ] `archived/` フォルダを作成
- [ ] 各フォルダに `_INDEX.md` を配置
- [ ] Git Repository に `assets/images/` フォルダを作成
- [ ] Git Repository に `docs/design-guidelines.md` を作成
- [ ] README.md にGoogle Driveリンクを追加
- [ ] チームメンバーに命名規則を共有

---

**策定日**: 2025-01-10
**最終更新**: 2025-01-10
**管理者**: プロジェクトリーダー
