# 日本語OCR OSSの調査・比較レポート

**調査日時**: 2025年11月16日
**対象ツール**: Tesseract OCR、EasyOCR、PaddleOCR

---

## エグゼクティブサマリー

### 推奨事項（一言まとめ）
**PaddleOCR** を Tesseract の代替・併用ツールとして推奨します。理由は以下の通りです：

1. **日本語精度が最高**: 日本語テキスト認識精度が3つのツール中で最も優れている
2. **処理速度とのバランス**: CPU環境でもTesseractより若干遅い程度で実用的
3. **積極的な開発**: 最新版では13%の精度改善（PP-OCRv5）
4. **macOS ARM64対応**: M1/M2 Macでの動作確認事例あり

**ただし請求書・領収書処理には注意**:
- 完全自動化には限界あり（複雑なレイアウト、手書き混在時）
- 前処理（二値化、傾き補正）の実装が必須
- Google Cloud Vision等のクラウドサービスとの併用も検討値

---

## 主要OCRツール比較表

| 項目 | Tesseract | EasyOCR | PaddleOCR |
|------|-----------|---------|-----------|
| **GitHub Stars** | 70.9k | 28.4k | 64k+ |
| **最新リリース** | v5.5.1 (2025/5/25) | v1.7.2 (2024/9/24) | v3.3.0 (2025/10/16) |
| **ライセンス** | Apache 2.0 | Apache 2.0 | Apache 2.0 |
| **開発活動** | 活発 | 活発 | 非常に活発 |
| **プロジェクト規模** | 6,575 commits / 189 contributors | - | 積極的更新 |

### 日本語対応

| 項目 | Tesseract | EasyOCR | PaddleOCR |
|------|-----------|---------|-----------|
| **日本語対応** | 可 (言語データ必須) | 可 (80+言語) | 可 (PP-OCRv5で5言語支援) |
| **日本語精度** | ⭐⭐ 低 | ⭐⭐⭐ 中〜高 | ⭐⭐⭐⭐ **最高** |
| **複雑文字対応** | 弱い | 中程度 | 強い |
| **ドキュメント** | 日本語情報少ない | 多言語対応 | 日本語README完備 |

### 処理性能

#### CPU環境での処理速度（秒単位）

**小画像 (555x418px)**:
- Tesseract: 0.85秒（最速）
- PaddleOCR: 1.52秒
- EasyOCR: 3.90秒

**大画像 (2132x1113px)**:
- Tesseract: 7.42秒
- PaddleOCR: 9.60秒
- EasyOCR: 51.34秒

#### GPU環境での処理速度

EasyOCRは GPU で大幅高速化:
- 小画像: 0.12秒（CPU比32倍高速）
- 大画像: 1.62秒（CPU比32倍高速）

### 日本語テキスト認識精度

実際のテスト結果（標準画質）:

| ツール | 精度 (標準テキスト) | 精度 (大きなテキスト) | 備考 |
|--------|------------------|------------------|------|
| **PaddleOCR** | ⭐⭐⭐⭐ 90点以上 | ⭐⭐⭐⭐⭐ 95-100点 | **推奨** |
| **EasyOCR** | ⭐⭐⭐⭐ 85-95点 | ⭐⭐⭐⭐⭐ 95点以上 | 次点推奨 |
| **Tesseract** | ⭐⭐ 30-70点 | ⭐⭐⭐ 70-85点 | 前処理で改善可 |

### インストール難易度とモデルサイズ

| 項目 | Tesseract | EasyOCR | PaddleOCR |
|------|-----------|---------|-----------|
| **インストール難易度** | ⭐ 最も簡単 (brew等) | ⭐⭐ 簡単 (pip) | ⭐⭐⭐ 中程度 |
| **基本モデルサイズ** | 小 (言語ファイル) | ~14MB | ~20MB |
| **初回起動時間** | 即座 | 数秒（GPU対応） | 数秒 |
| **メモリ使用量** | 低 | 中 | 中 |

---

## 各ツールの詳細評価

### 1. PaddleOCR

**概要**:
Baidu PaddlePaddleフレームワークベースのOCRツールキット。100+言語対応で、特にアジア言語に最適化。

**メリット**:
- ✅ 日本語精度が最も高い（PP-OCRv5で13%精度向上）
- ✅ 処理速度が実用的（CPU環境でも9.6秒/大画像）
- ✅ 複数テキストタイプ対応（簡体字中国語、繁体字中国語、英語、日本語、ピンイン）
- ✅ 活発な開発（最新版 v3.3.0は2025/10リリース）
- ✅ 日本語ドキュメント完備
- ✅ OSS中で最高の精度

**デメリット**:
- ❌ MacOS ARM64での互換性問題が報告されている
- ❌ 初期セットアップが少し複雑
- ❌ 大規模前処理には向かない可能性

**インストール (macOS ARM64)**:
```bash
# 方法1: 基本インストール (CPU版)
pip install paddlepaddle paddleocr

# 方法2: 推奨 (Python 3.9.6が最も安定)
python3.9 -m pip install paddlepaddle==2.5.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
python3.9 -m pip install paddleocr

# 使用例
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='japan')
result = ocr.ocr('image.jpg', cls=True)
```

**実装コード例**:
```python
from paddleocr import PaddleOCR
import cv2

# 初期化（初回は自動的にモデルをダウンロード）
ocr = PaddleOCR(use_angle_cls=True, lang='japan')

# 画像の読み込み
image_path = 'invoice.jpg'

# OCR実行
result = ocr.ocr(image_path, cls=True)

# 結果処理
for line in result:
    for word_info in line:
        text = word_info[1][0]
        confidence = word_info[1][1]
        print(f"{text} ({confidence:.2%})")
```

**GitHub**: https://github.com/PaddlePaddle/PaddleOCR
**メンテナンス**: ⭐⭐⭐⭐⭐ 非常に活発（毎月更新あり）

---

### 2. EasyOCR

**概要**:
80+言語対応の使いやすいOCRライブラリ。CRAFT検出 + CRNN認識のアーキテクチャ。

**メリット**:
- ✅ インストール最も簡単（`pip install easyocr`）
- ✅ GPUで大幅高速化（32倍高速）
- ✅ API設計がシンプル
- ✅ macOS ARM64での互換性報告あり
- ✅ カスタムモデル訓練対応
- ✅ Hugging Face Spacesで無料試行可能

**デメリット**:
- ❌ CPU環境では非常に遅い（51秒/大画像）
- ❌ 日本語精度がPaddleOCRより劣る
- ❌ GPU必須での実用性
- ❌ 前処理なしで精度不足

**インストール (macOS ARM64)**:
```bash
# 標準インストール
pip install easyocr

# または
pip install easyocr opencv-python

# GPU版 (別途CUDA設定が必要)
pip install easyocr torch torchvision

# 使用例
import easyocr
reader = easyocr.Reader(['ja'])  # 日本語モデルをロード
result = reader.readtext('image.jpg')
```

**実装コード例**:
```python
import easyocr
import cv2

# リーダー初期化（初回は自動ダウンロード）
reader = easyocr.Reader(['ja'])

# 画像読み込み
image = cv2.imread('invoice.jpg')

# OCR実行
result = reader.readtext('invoice.jpg')

# 結果処理
texts = []
for (bbox, text, confidence) in result:
    print(f"{text} ({confidence:.2%})")
    texts.append(text)

# テキスト抽出
extracted_text = '\n'.join(texts)
print(extracted_text)
```

**GitHub**: https://github.com/JaidedAI/EasyOCR
**統計**: ⭐ 28.4k stars / 3.5k forks / 114 contributors
**メンテナンス**: ⭐⭐⭐ 活発（v1.7.2は2024年9月リリース）

---

### 3. Tesseract OCR

**概要**:
30年以上の歴史を持つ、最も確立されたOCRエンジン。100+言語対応。

**メリット**:
- ✅ CPU処理が最速（0.85秒/小画像）
- ✅ 最も広く採用・信頼されている
- ✅ インストール簡単（macOSではbrewで一行）
- ✅ メモリ使用量が少ない
- ✅ カスタマイズ性が高い

**デメリット**:
- ❌ 日本語精度が低い（特に複雑文字）
- ❌ 前処理が必須
- ❌ CJK言語に弱い
- ❌ ニューラルネットワークベースではない
- ❌ 開発スピードが遅い

**インストール (macOS)**:
```bash
# Homebrewで簡単インストール
brew install tesseract

# 日本語言語データをインストール
brew install tesseract-lang

# Python バインディング
pip install pytesseract

# 使用例
import pytesseract
text = pytesseract.image_to_string('image.jpg', lang='jpn')
```

**実装コード例**:
```python
import pytesseract
import cv2

# 画像読み込み
image = cv2.imread('invoice.jpg')

# 前処理（二値化が重要）
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# OCR実行
text = pytesseract.image_to_string(binary, lang='jpn')

# 日本語のみ抽出する場合
text = pytesseract.image_to_string(binary, lang='jpn+eng')

print(text)
```

**GitHub**: https://github.com/tesseract-ocr/tesseract
**統計**: ⭐ 70.9k stars / 10.4k forks / 189 contributors
**最新版**: v5.5.1 (2025年5月)
**メンテナンス**: ⭐⭐⭐⭐ 活発（定期的なリリース）

---

## 請求書・領収書OCR処理での実践的比較

### ユースケース: 建設関連の請求書（混合レイアウト）

#### 1. 単純な請求書（均一フォーマット）
- **推奨**: **PaddleOCR** (精度95%以上)
- **次点**: EasyOCR（GPU使用時）
- **回避**: Tesseract単体

#### 2. 複雑なレイアウト（手書き混在）
- **推奨**: EasyOCR + 前処理
- **次点**: PaddleOCR + 前処理
- **クラウド検討**: Google Cloud Vision

#### 3. 大量バッチ処理（効率重視）
- **推奨**: Tesseract（CPU処理で高速）
- **次点**: PaddleOCR（精度とのバランス）
- **GPU環境**: EasyOCR

#### 実装上の注意点

**前処理が必須**:
```python
import cv2
import numpy as np

def preprocess_image(image_path):
    """OCR精度向上の前処理"""
    img = cv2.imread(image_path)

    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ノイズ除去
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # 二値化
    binary = cv2.threshold(denoised, 0, 255,
                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # 傾き補正（オプション）
    # ... (複雑なため省略)

    return binary

# 前処理でPaddleOCRの精度が30点→90点に向上した報告例あり
```

**精度向上の工夫**:
- 画像をリサイズ（300-400 dpi相当）
- ノイズ除去（fastNlMeansDenoising）
- 傾き補正（affine変換）
- 明度調整（CLAHE処理）

---

## インストール手順（macOS ARM64対応）

### Option A: PaddleOCR推奨セットアップ

```bash
# 1. Python 3.9.6 推奨（最も安定）
# （システムPythonまたはpyenvで3.9.6を使用）

# 2. 仮想環境作成
python3.9 -m venv ocr_env
source ocr_env/bin/activate

# 3. PaddleOCR インストール
pip install --upgrade pip
pip install paddlepaddle==2.5.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
pip install paddleocr

# 4. 日本語モデルの動作確認
python3 << 'EOF'
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='japan')
print("✅ PaddleOCR ready")
EOF
```

### Option B: EasyOCR セットアップ

```bash
# 1. 仮想環境作成
python3 -m venv easyocr_env
source easyocr_env/bin/activate

# 2. EasyOCR インストール
pip install --upgrade pip
pip install easyocr opencv-python

# 3. 動作確認
python3 << 'EOF'
import easyocr
reader = easyocr.Reader(['ja'])
print("✅ EasyOCR ready")
EOF
```

### Option C: Tesseract セットアップ

```bash
# 1. Homebrew でインストール
brew install tesseract tesseract-lang

# 2. Python バインディング
pip install pytesseract

# 3. 動作確認
python3 << 'EOF'
import pytesseract
print(pytesseract.get_tesseract_version())
EOF
```

### Option D: 複合環境（すべてのツールを試す）

```bash
# メインの仮想環境
python3 -m venv ocr_multi
source ocr_multi/bin/activate

# インストール
pip install --upgrade pip
pip install paddlepaddle paddleocr easyocr pytesseract opencv-python numpy pillow

# Tesseract インストール（別途）
brew install tesseract tesseract-lang

# テスト
python3 test_all_ocr.py
```

---

## ライセンス・コンプライアンス

| ツール | ライセンス | 商用利用 | 改変配布 |
|--------|-----------|--------|---------|
| **PaddleOCR** | Apache 2.0 | ✅ 可 | ✅ 可（表示義務） |
| **EasyOCR** | Apache 2.0 | ✅ 可 | ✅ 可（表示義務） |
| **Tesseract** | Apache 2.0 | ✅ 可 | ✅ 可（表示義務） |

**全て商用利用可能です。ただし修正版配布時はライセンス表示が必須。**

---

## 推奨実装パターン

### パターン1: 精度最優先（推奨）

```python
# PaddleOCR単体 + 前処理
from paddleocr import PaddleOCR
import cv2

ocr = PaddleOCR(use_angle_cls=True, lang='japan')

def extract_text(image_path):
    # 前処理
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # OCR
    result = ocr.ocr(image_path, cls=True)

    # テキスト抽出
    texts = [word_info[1][0] for line in result for word_info in line]
    return ' '.join(texts)
```

### パターン2: バランス型（実用的）

```python
# PaddleOCR + Tesseract フォールバック
from paddleocr import PaddleOCR
import pytesseract
import cv2

paddle_ocr = PaddleOCR(use_angle_cls=True, lang='japan')

def extract_text_fallback(image_path):
    try:
        # 1. PaddleOCR で試行（高精度）
        result = paddle_ocr.ocr(image_path, cls=True)
        texts = [word[1][0] for line in result for word in line]

        if len(texts) > 5:  # 十分なテキスト抽出
            return ' '.join(texts), 'paddle'
    except:
        pass

    # 2. Tesseract でフォールバック（高速）
    text = pytesseract.image_to_string(image_path, lang='jpn')
    return text, 'tesseract'
```

### パターン3: 高速バッチ処理（大量データ）

```python
# Tesseract + 前処理（速度最優先）
import pytesseract
from concurrent.futures import ProcessPoolExecutor
import cv2

def process_image_batch(image_paths):
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_single, image_paths))
    return results

def process_single(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(binary, lang='jpn')
    return text
```

---

## トラブルシューティング

### PaddleOCR に関する問題

**問題 1: macOS M1 で "RuntimeError: Illegal instruction"**
```
解決: Python 3.9.6 を使用し、Intel版ではなく ARM64版を確認
pip install python==3.9.6
```

**問題 2: 初回起動で "モデルダウンロード中" で止まる**
```
解決: インターネット接続確認、Paddleバージョンを固定
pip install paddlepaddle==2.5.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```

**問題 3: メモリ不足エラー**
```python
# モデル最適化オプション
ocr = PaddleOCR(use_gpu=False, det_model_dir='cpu', rec_model_dir='cpu')
```

### EasyOCR に関する問題

**問題 1: GPU が認識されない**
```
解決: CUDA と cuDNN のバージョン確認
pip install torch torchvision torchaudio
```

**問題 2: CPU では遅すぎる**
```
解決: より小さいモデルを使用（該当モデルがあれば）
または GPU の導入を検討
```

### Tesseract に関する問題

**問題 1: "tessdata directory not found"**
```bash
解決: brew で再インストール
brew reinstall tesseract tesseract-lang
```

**問題 2: 日本語が認識されない**
```bash
解決: 言語ファイル確認
tessdata=$(brew --prefix)/share/tessdata
ls $tessdata | grep jpn
```

---

## 最終推奨事項

### シナリオ別選択ガイド

| シナリオ | 推奨ツール | 理由 |
|--------|-----------|------|
| **日本語精度最優先** | PaddleOCR | 精度90%以上、開発活発 |
| **複雑レイアウト・手書き** | EasyOCR + GPU | 検出精度が高い |
| **CPU環境で速度重視** | Tesseract | 圧倒的に高速 |
| **バランス型（実用）** | PaddleOCR | 精度と速度のバランス最良 |
| **AWS/GCP統合** | PaddleOCR | 拡張性最高 |
| **商用品質必須** | Google Cloud Vision | 精度・信頼性最高 |

### 当面の実装方針

**短期（1～2週間）**:
1. PaddleOCR のインストール・検証（Python 3.9.6環境）
2. 実際の請求書画像での精度テスト
3. 前処理パイプラインの構築

**中期（1ヶ月）**:
1. EasyOCR との並行テスト（複雑レイアウト対応確認）
2. パフォーマンス計測（処理時間、メモリ）
3. エラーハンドリング・フォールバック実装

**長期（3～6ヶ月）**:
1. 本格運用環境への統合
2. 必要に応じてクラウド API への段階的移行検討
3. カスタムモデル訓練（特殊フォーマット対応）

---

## 参考資料

### GitHub リポジトリ
- **PaddleOCR**: https://github.com/PaddlePaddle/PaddleOCR
- **EasyOCR**: https://github.com/JaidedAI/EasyOCR
- **Tesseract**: https://github.com/tesseract-ocr/tesseract

### 日本語ベンチマーク記事
- Zenn: 日本語対応オープンソースOCRの比較
  https://zenn.dev/piment/articles/254dde3ecf7f10
- Buddypia: EasyOCRとPaddleOCRの比較
  https://buddypia.com/2022/12/15/easyocr%E3%81%A8paddleocr%E3%81%AE%E6%AF%94%E8%BC%83/

### 公式ドキュメント
- PaddleOCR 日本語README:
  https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_i18n/README_日本語.md
- EasyOCR 公式サイト: https://www.jaided.ai/easyocr/
- Tesseract ドキュメント: https://tesseract-ocr.github.io/tessdoc/

---

**レポート作成**: Claude Code
**最終更新**: 2025-11-16
