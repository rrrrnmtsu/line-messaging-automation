# 日本語OCR OSSの調査・比較レポート

**作成日**: 2025年11月16日
**対象プラットフォーム**: macOS ARM64 (M1/M2)
**言語**: 日本語

---

## 📋 このレポートについて

このディレクトリには、日本語対応のOCR (Optical Character Recognition) オープンソースソフトウェアの包括的な調査・比較結果が含まれています。

### 主な対象ツール
1. **PaddleOCR** - Baidu PaddlePaddleベース（推奨）
2. **EasyOCR** - JaidedAI開発（次点推奨）
3. **Tesseract OCR** - 最も古い確立されたツール

---

## 📁 ファイル構成

### 1. **docs/research_report.md** (メインレポート)
- **内容**: 詳細な比較分析、推奨事項、実装パターン
- **分量**: 約600行
- **用途**: 戦略判断、実装方針決定時に参照

**主要セクション**:
- エグゼクティブサマリー（一言推奨事項）
- 主要OCRツール比較表
- 各ツールの詳細評価
- 請求書・領収書OCR処理での実践的比較
- インストール手順（macOS ARM64対応）
- トラブルシューティング
- 最終推奨事項とシナリオ別選択ガイド

**👉 最初に読むべきファイル**

### 2. **data/tools_comparison.json** (構造化データ)
- **内容**: 比較データをJSON形式で構造化
- **用途**: プログラマティックアクセス、ダッシュボード作成
- **データ形式**:
  - Repository statistics
  - Performance benchmarks
  - Implementation recommendations
  - Community insights

**活用例**:
```python
import json

with open('data/tools_comparison.json') as f:
    data = json.load(f)

# リポジトリ統計の取得
for repo in data['repositories']:
    print(f"{repo['name']}: {repo['stats']['stars']} stars")

# パフォーマンスベンチマーク
bench = data['performance_benchmark']['test_image_large']
print(f"PaddleOCR CPU時間: {bench['paddleocr_cpu_seconds']}秒")
```

### 3. **src/implementation_examples.py** (実装コード)
- **内容**: PaddleOCR, EasyOCR, Tesseractの実装例とユーティリティ
- **用途**: 実装の参考コード、テンプレート
- **主要クラス**:
  - `PaddleOCRHandler` - PaddleOCR操作
  - `EasyOCRHandler` - EasyOCR操作
  - `TesseractOCRHandler` - Tesseract操作
  - `MultiEngineOCR` - フォールバック実装
  - `InvoiceOCRProcessor` - 請求書処理

**使用方法**:
```python
from src.implementation_examples import MultiEngineOCR

ocr = MultiEngineOCR()
text, engine = ocr.extract_text_with_fallback('invoice.jpg')
print(f"Extracted by {engine}: {text}")
```

### 4. **src/setup_macos.sh** (セットアップスクリプト)
- **内容**: macOS環境の自動セットアップ
- **用途**: 仮想環境構築、OCRツールのインストール
- **機能**:
  - macOS/ARM64チェック
  - Homebrew確認
  - Python 3.9.6 インストール
  - 仮想環境作成
  - PaddleOCR, EasyOCR, Tesseract のインストール
  - 動作確認

**実行方法**:
```bash
chmod +x src/setup_macos.sh
./src/setup_macos.sh
```

---

## 🎯 クイックスタート

### 最も簡単な方法（推奨）

#### ステップ1: セットアップスクリプトの実行
```bash
# スクリプトに実行権限を付与
chmod +x src/setup_macos.sh

# スクリプト実行
./src/setup_macos.sh
```

スクリプトが以下を自動的に実行します：
- Python 3.9.6 のインストール（pyenv経由）
- 仮想環境の作成
- PaddleOCR/EasyOCR/Tesseract のインストール

#### ステップ2: 仮想環境の有効化
```bash
source ~/ocr_env/bin/activate
```

#### ステップ3: テスト実行
```bash
python3 src/implementation_examples.py
```

---

## 📊 推奨事項（一言まとめ）

| 用途 | 推奨ツール | 理由 |
|------|-----------|------|
| **日本語精度最優先** | **PaddleOCR** | 精度90%以上、開発活発 |
| **複雑レイアウト・手書き** | **EasyOCR** (+ GPU) | 検出精度が高い |
| **CPU環境で速度重視** | **Tesseract** | 圧倒的に高速 |
| **バランス型（実用）** | **PaddleOCR** | 精度と速度のバランス最良 |
| **請求書・領収書処理** | **PaddleOCR** + 前処理 | 複雑レイアウト対応 |

---

## 🔍 性能比較（CPU環境）

### 処理速度

**小画像 (555x418px)**:
- Tesseract: **0.85秒** (最速)
- PaddleOCR: 1.52秒
- EasyOCR: 3.90秒

**大画像 (2132x1113px)**:
- Tesseract: **7.42秒** (最速)
- PaddleOCR: 9.60秒
- EasyOCR: 51.34秒 (非実用的)

### 日本語精度

**標準テキスト**:
- Tesseract: ⭐⭐ (30-70点, 前処理で改善)
- EasyOCR: ⭐⭐⭐⭐ (85-95点)
- **PaddleOCR**: ⭐⭐⭐⭐⭐ (90%以上, **推奨**)

**大きなテキスト**:
- Tesseract: ⭐⭐⭐ (70-85点)
- EasyOCR: ⭐⭐⭐⭐⭐ (95点以上)
- **PaddleOCR**: ⭐⭐⭐⭐⭐ (95-100点, **推奨**)

---

## 💻 インストール手順

### 方法A: 自動セットアップ（推奨）
```bash
chmod +x src/setup_macos.sh
./src/setup_macos.sh
```

### 方法B: 手動セットアップ（PaddleOCR）

```bash
# Python 3.9.6 の使用（最も安定）
# pyenv を使用している場合
pyenv global 3.9.6

# 仮想環境作成
python3.9 -m venv ocr_env
source ocr_env/bin/activate

# インストール
pip install --upgrade pip
pip install paddlepaddle==2.5.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
pip install paddleocr

# テスト
python3 << 'EOF'
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='japan')
print("✅ PaddleOCR ready")
EOF
```

### 方法C: 手動セットアップ（EasyOCR）

```bash
# 仮想環境作成
python3 -m venv easyocr_env
source easyocr_env/bin/activate

# インストール
pip install --upgrade pip
pip install easyocr opencv-python

# テスト
python3 << 'EOF'
import easyocr
reader = easyocr.Reader(['ja'])
print("✅ EasyOCR ready")
EOF
```

### 方法D: 手動セットアップ（Tesseract）

```bash
# Homebrew でインストール
brew install tesseract tesseract-lang

# Python バインディング
pip install pytesseract

# テスト
python3 -c "import pytesseract; print(pytesseract.get_tesseract_version())"
```

---

## 🚀 実装パターン

### パターン1: 高精度重視（推奨）

```python
from src.implementation_examples import PaddleOCRHandler

handler = PaddleOCRHandler()
text = handler.extract_text('invoice.jpg')
print(text)
```

**利点**: 最高の日本語精度
**欠点**: 初期セットアップが少し複雑
**推奨用途**: 請求書・領収書、正式文書

### パターン2: バランス型（実用的）

```python
from src.implementation_examples import MultiEngineOCR

ocr = MultiEngineOCR()
text, engine = ocr.extract_text_with_fallback('document.jpg')
print(f"Extracted by {engine}: {text}")
```

**利点**: 複数エンジンの自動フォールバック
**欠点**: セットアップが複雑
**推奨用途**: 本番環境、信頼性重視

### パターン3: 高速バッチ処理

```python
from src.implementation_examples import TesseractOCRHandler

handler = TesseractOCRHandler()
text = handler.extract_text('document.jpg', preprocess=True)
print(text)
```

**利点**: 最速（CPU）、シンプル
**欠点**: 日本語精度が低い
**推奨用途**: 大量バッチ処理、速度優先

### パターン4: 請求書処理

```python
from src.implementation_examples import InvoiceOCRProcessor

processor = InvoiceOCRProcessor()
result = processor.process_invoice('invoice.jpg')
print(result)
# {'raw_text': '...',  'engine': 'paddle', 'invoice_number': '...', ...}
```

**利点**: 請求書向けに最適化
**推奨用途**: 請求書・領収書の自動処理

---

## 🔧 トラブルシューティング

### PaddleOCR

**問題: "Illegal instruction" エラー on M1/M2**
```
解決: Python 3.9.6 を使用してください
pyenv install 3.9.6
pyenv global 3.9.6
```

**問題: 初回起動で "モデルダウンロード中" で止まる**
```
解決: インターネット接続を確認し、Paddleバージョンを固定してください
pip install paddlepaddle==2.5.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```

### EasyOCR

**問題: CPU 処理が遅すぎる (50+ 秒)**
```
解決: GPU の導入を検討するか、別のツールを使用してください
# GPU版
pip install torch torchvision  # CUDA環境下で
reader = easyocr.Reader(['ja'], gpu=True)
```

### Tesseract

**問題: "tessdata directory not found"**
```bash
解決: 再インストール
brew reinstall tesseract tesseract-lang
```

---

## 📈 パフォーマンスチューニング

### 画像前処理による精度向上

```python
from src.implementation_examples import ImagePreprocessor

# 基本前処理
preprocessor = ImagePreprocessor()
processed = preprocessor.basic_preprocessing('invoice.jpg')

# 複雑な文書向け高度な前処理
advanced = preprocessor.advanced_preprocessing('invoice.jpg')
```

**前処理の効果**:
- Tesseract: 30点 → 70点 (2倍以上)
- PaddleOCR: 90点 → 95点以上
- EasyOCR: 85点 → 95点以上

### GPU 加速（EasyOCR）

```python
import easyocr

# GPU を使用（32倍高速）
reader = easyocr.Reader(['ja'], gpu=True)
```

**処理時間**:
- CPU: 51秒 (大画像)
- GPU: 1.6秒 (32倍高速)

---

## 🔗 参考資料

### 公式リポジトリ

- **PaddleOCR**: https://github.com/PaddlePaddle/PaddleOCR
- **EasyOCR**: https://github.com/JaidedAI/EasyOCR
- **Tesseract**: https://github.com/tesseract-ocr/tesseract

### 日本語ベンチマーク

- Zenn: [日本語対応オープンソースOCRの比較](https://zenn.dev/piment/articles/254dde3ecf7f10)
- Buddypia: [EasyOCRとPaddleOCRの比較](https://buddypia.com/2022/12/15/easyocr%E3%81%A8paddleocr%E3%81%AE%E6%AF%94%E8%BC%83/)

### 公式ドキュメント

- PaddleOCR 日本語README: https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_i18n/README_日本語.md
- EasyOCR 公式: https://www.jaided.ai/easyocr/
- Tesseract 公式: https://tesseract-ocr.github.io/tessdoc/

---

## 📝 ファイル一覧と用途

| ファイル | 用途 | 推奨読者 |
|--------|------|--------|
| `docs/research_report.md` | 詳細な分析と推奨事項 | 意思決定者、PM |
| `data/tools_comparison.json` | 構造化データ | エンジニア、データ分析 |
| `src/implementation_examples.py` | 実装コード例 | エンジニア |
| `src/setup_macos.sh` | 環境セットアップ | すべてのユーザー |
| `README.md` | このファイル（ガイド） | 全員 |

---

## 📞 サポート・質問

### よくある質問

**Q: どのツールを選べばいい？**
> A: 日本語精度重視なら **PaddleOCR**。複雑なレイアウトなら **EasyOCR** (GPU必須)。速度重視なら **Tesseract** (精度が低い点に注意)。

**Q: macOS M1 で動きますか？**
> A: はい。PaddleOCR と EasyOCR は ARM64 対応です。Python 3.9.6 を推奨。

**Q: GPU なしで実用的？**
> A: PaddleOCR と Tesseract は CPU でも実用的。EasyOCR は GPU 必須。

**Q: 請求書・領収書の処理に最適？**
> A: **PaddleOCR** + 画像前処理（二値化、ノイズ除去）。複雑なレイアウトは EasyOCR も検討。

---

## ✅ 次のステップ

1. **セットアップ**: `src/setup_macos.sh` を実行
2. **テスト**: 実装例でテスト実行
3. **評価**: 実際の請求書画像で精度テスト
4. **本運用**: 本格実装へ

---

## 📊 プロジェクト統計

| メトリクス | 値 |
|-----------|-----|
| 調査したリポジトリ | 3個 |
| 参照した記事・資料 | 12個 |
| 比較項目 | 15項目 |
| 実装コード例 | 15パターン |
| 対応プラットフォーム | macOS (Intel/ARM64) |

---

**最終更新**: 2025年11月16日
**レポート作成者**: Claude Code (AI Technical Researcher)
**ライセンス**: このレポートは参考資料です。実装にはOSSのライセンス（Apache 2.0）に従ってください。
