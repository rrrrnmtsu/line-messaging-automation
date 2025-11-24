#!/usr/bin/env python3
"""
日本語OCR実装例 - PaddleOCR, EasyOCR, Tesseractの使用方法
macOS ARM64環境での実装パターン
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# 1. PaddleOCR 実装例
# ============================================================================

class PaddleOCRHandler:
    """PaddleOCRの実装ハンドラー（日本語対応）"""

    def __init__(self, use_angle_cls: bool = True):
        """
        初期化（初回はモデルを自動ダウンロード）

        Args:
            use_angle_cls: 傾き補正を使用するか
        """
        try:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang='japan')
            logger.info("✅ PaddleOCR initialized successfully")
        except ImportError:
            logger.error("❌ PaddleOCR not installed. Run: pip install paddleocr")
            raise

    def extract_text(self, image_path: str) -> str:
        """
        画像からテキストを抽出
        """
        try:
            result = self.ocr.ocr(image_path, cls=True)

            texts = []
            for line in result:
                for word_info in line:
                    text = word_info[1][0]
                    confidence = word_info[1][1]

                    # 信頼度が一定以上のみを抽出
                    if confidence > 0.3:
                        texts.append(text)
                        logger.debug(f"Text: {text} (confidence: {confidence:.2%})")

            return ' '.join(texts)

        except Exception as e:
            logger.error(f"Error in PaddleOCR extraction: {e}")
            raise

    def extract_text_with_confidence(self, image_path: str) -> List[Tuple[str, float]]:
        """
        テキストと信頼度をペアで抽出
        """
        result = self.ocr.ocr(image_path, cls=True)

        text_confidence_pairs = []
        for line in result:
            for word_info in line:
                text = word_info[1][0]
                confidence = word_info[1][1]
                text_confidence_pairs.append((text, confidence))

        return text_confidence_pairs


# ============================================================================
# 2. EasyOCR 実装例
# ============================================================================

class EasyOCRHandler:
    """EasyOCRの実装ハンドラー（日本語対応）"""

    def __init__(self):
        """初期化（初回はモデルを自動ダウンロード）"""
        try:
            import easyocr
            self.reader = easyocr.Reader(['ja'], gpu=False)  # CPU版, gpu=Trueで高速化可能
            logger.info("✅ EasyOCR initialized successfully")
        except ImportError:
            logger.error("❌ EasyOCR not installed. Run: pip install easyocr opencv-python")
            raise

    def extract_text(self, image_path: str) -> str:
        """
        画像からテキストを抽出
        """
        try:
            result = self.reader.readtext(image_path)

            texts = []
            for (bbox, text, confidence) in result:
                if confidence > 0.3:  # 信頼度フィルター
                    texts.append(text)
                    logger.debug(f"Text: {text} (confidence: {confidence:.2%})")

            return ' '.join(texts)

        except Exception as e:
            logger.error(f"Error in EasyOCR extraction: {e}")
            raise

    def extract_with_bbox(self, image_path: str) -> List[Tuple[np.ndarray, str, float]]:
        """
        テキストと座標情報を抽出
        """
        result = self.reader.readtext(image_path)
        return [(bbox, text, conf) for (bbox, text, conf) in result if conf > 0.3]


# ============================================================================
# 3. Tesseract OCR 実装例
# ============================================================================

class TesseractOCRHandler:
    """Tesseract OCRの実装ハンドラー（日本語対応）"""

    def __init__(self):
        """初期化"""
        try:
            import pytesseract
            self.pytesseract = pytesseract
            logger.info("✅ Tesseract OCR initialized")
        except ImportError:
            logger.error("❌ Tesseract not installed. Run: brew install tesseract tesseract-lang && pip install pytesseract")
            raise

    def extract_text(self, image_path: str, preprocess: bool = True) -> str:
        """
        画像からテキストを抽出（前処理オプション付き）

        Args:
            image_path: 画像ファイルパス
            preprocess: 前処理を行うか（推奨: True）
        """
        try:
            if preprocess:
                image = self._preprocess_image(image_path)
                # 前処理後の画像を一時ファイルに保存（pytesseractの制限）
                temp_path = '/tmp/tesseract_input.png'
                cv2.imwrite(temp_path, image)
                text = self.pytesseract.image_to_string(temp_path, lang='jpn')
            else:
                text = self.pytesseract.image_to_string(image_path, lang='jpn')

            return text

        except Exception as e:
            logger.error(f"Error in Tesseract extraction: {e}")
            raise

    @staticmethod
    def _preprocess_image(image_path: str) -> np.ndarray:
        """
        前処理パイプライン（Tesseract精度向上の重要なステップ）
        """
        img = cv2.imread(image_path)

        # グレースケール化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ノイズ除去（重要）
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # 二値化（Otsu's method）
        binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return binary


# ============================================================================
# 4. 画像前処理ユーティリティ
# ============================================================================

class ImagePreprocessor:
    """OCR精度向上のための画像前処理"""

    @staticmethod
    def basic_preprocessing(image_path: str) -> np.ndarray:
        """
        基本的な前処理パイプライン
        """
        img = cv2.imread(image_path)

        # グレースケール化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ノイズ除去
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # 二値化
        binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return binary

    @staticmethod
    def advanced_preprocessing(image_path: str) -> np.ndarray:
        """
        高度な前処理パイプライン（複雑な文書用）
        """
        img = cv2.imread(image_path)

        # グレースケール化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ノイズ除去（複数パス）
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # 適応的ヒストグラム均等化（明るさ調整）
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)

        # 二値化
        binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # 膨張・収縮で小ノイズを除去
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        return morph

    @staticmethod
    def resize_for_ocr(image_path: str, target_dpi: int = 300) -> np.ndarray:
        """
        OCR推奨解像度にリサイズ（300-400 DPI相当）
        """
        img = cv2.imread(image_path)
        height, width = img.shape[:2]

        # 簡易的なスケーリング（実際のDPI情報から計算する場合は修正が必要）
        scale_factor = 1.5
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        return resized


# ============================================================================
# 5. マルチエンジンフォールバック実装
# ============================================================================

class MultiEngineOCR:
    """複数OCRエンジンのフォールバック実装"""

    def __init__(self):
        """複数エンジンを初期化"""
        self.engines = {}

        # PaddleOCRを試す
        try:
            self.engines['paddle'] = PaddleOCRHandler()
            logger.info("✅ PaddleOCR available")
        except Exception as e:
            logger.warning(f"⚠️ PaddleOCR unavailable: {e}")

        # EasyOCRを試す
        try:
            self.engines['easy'] = EasyOCRHandler()
            logger.info("✅ EasyOCR available")
        except Exception as e:
            logger.warning(f"⚠️ EasyOCR unavailable: {e}")

        # Tesseractを試す
        try:
            self.engines['tesseract'] = TesseractOCRHandler()
            logger.info("✅ Tesseract available")
        except Exception as e:
            logger.warning(f"⚠️ Tesseract unavailable: {e}")

    def extract_text_with_fallback(self, image_path: str, min_length: int = 5) -> Tuple[str, str]:
        """
        複数エンジンでテキスト抽出。失敗時は次のエンジンを試す

        Returns:
            (extracted_text, engine_name) のタプル
        """
        # PaddleOCR優先（最も精度が高い）
        if 'paddle' in self.engines:
            try:
                text = self.engines['paddle'].extract_text(image_path)
                if len(text) > min_length:
                    logger.info(f"✅ Used PaddleOCR (extracted {len(text)} chars)")
                    return text, 'paddle'
            except Exception as e:
                logger.warning(f"PaddleOCR failed: {e}, trying EasyOCR")

        # EasyOCR次点
        if 'easy' in self.engines:
            try:
                text = self.engines['easy'].extract_text(image_path)
                if len(text) > min_length:
                    logger.info(f"✅ Used EasyOCR (extracted {len(text)} chars)")
                    return text, 'easy'
            except Exception as e:
                logger.warning(f"EasyOCR failed: {e}, trying Tesseract")

        # Tesseract最後の砦（高速だが精度低い）
        if 'tesseract' in self.engines:
            try:
                text = self.engines['tesseract'].extract_text(image_path, preprocess=True)
                logger.info(f"✅ Used Tesseract (extracted {len(text)} chars)")
                return text, 'tesseract'
            except Exception as e:
                logger.error(f"All OCR engines failed: {e}")

        return "", "none"


# ============================================================================
# 6. 請求書/領収書OCR処理の実装例
# ============================================================================

class InvoiceOCRProcessor:
    """請求書・領収書専用のOCR処理"""

    def __init__(self):
        """初期化"""
        self.ocr = MultiEngineOCR()
        self.preprocessor = ImagePreprocessor()

    def process_invoice(self, image_path: str) -> dict:
        """
        請求書を処理してメタデータを抽出

        Returns:
            {
                'raw_text': '抽出されたテキスト',
                'engine': '使用されたエンジン名',
                'invoice_number': '請求書番号（抽出試行）',
                'date': '日付（抽出試行）',
                'amount': '金額（抽出試行）'
            }
        """
        logger.info(f"Processing invoice: {image_path}")

        # 前処理
        preprocessed = self.preprocessor.basic_preprocessing(image_path)
        temp_path = '/tmp/invoice_preprocessed.png'
        cv2.imwrite(temp_path, preprocessed)

        # OCR実行
        text, engine = self.ocr.extract_text_with_fallback(temp_path)

        # 簡単なパターンマッチングで情報抽出
        import re

        result = {
            'raw_text': text,
            'engine': engine,
            'invoice_number': self._extract_invoice_number(text),
            'date': self._extract_date(text),
            'amount': self._extract_amount(text)
        }

        logger.info(f"Extraction complete. Found: {result['invoice_number']}, {result['date']}, {result['amount']}")
        return result

    @staticmethod
    def _extract_invoice_number(text: str) -> Optional[str]:
        """請求書番号を抽出"""
        # 正規表現で請求書番号を検索
        match = re.search(r'請求書番号[：:]\s*([A-Z0-9\-]+)', text)
        return match.group(1) if match else None

    @staticmethod
    def _extract_date(text: str) -> Optional[str]:
        """日付を抽出"""
        match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', text)
        return match.group(1) if match else None

    @staticmethod
    def _extract_amount(text: str) -> Optional[str]:
        """金額を抽出"""
        match = re.search(r'合計[：:]\s*([0-9,]+)円', text)
        return match.group(1) if match else None


# ============================================================================
# 7. 使用例
# ============================================================================

def main():
    """使用例のメイン関数"""

    print("=" * 80)
    print("日本語OCR実装例")
    print("=" * 80)

    # テスト画像があるか確認
    test_image = "/path/to/test/image.jpg"

    if not Path(test_image).exists():
        print(f"\n⚠️ テスト画像が見つかりません: {test_image}")
        print("\n【実装例】以下のようにして使用します:\n")

        # パターン1: PaddleOCR
        print("1. PaddleOCR の使用例:")
        print("""
    from implementation_examples import PaddleOCRHandler

    handler = PaddleOCRHandler()
    text = handler.extract_text('invoice.jpg')
    print(text)
        """)

        # パターン2: EasyOCR
        print("\n2. EasyOCR の使用例:")
        print("""
    from implementation_examples import EasyOCRHandler

    handler = EasyOCRHandler()
    text = handler.extract_text('invoice.jpg')
    print(text)
        """)

        # パターン3: マルチエンジンフォールバック
        print("\n3. マルチエンジンフォールバック:")
        print("""
    from implementation_examples import MultiEngineOCR

    ocr = MultiEngineOCR()
    text, engine = ocr.extract_text_with_fallback('invoice.jpg')
    print(f"Extracted by {engine}: {text}")
        """)

        # パターン4: 請求書処理
        print("\n4. 請求書OCR処理:")
        print("""
    from implementation_examples import InvoiceOCRProcessor

    processor = InvoiceOCRProcessor()
    result = processor.process_invoice('invoice.jpg')
    print(result)
        """)
        return

    # テスト画像がある場合の実行例
    print(f"\nテスト画像を処理中: {test_image}\n")

    # パターン1: 単一エンジン（PaddleOCR）
    try:
        print("【PaddleOCR での処理】")
        handler = PaddleOCRHandler()
        text = handler.extract_text(test_image)
        print(f"抽出されたテキスト: {text[:100]}...\n")
    except Exception as e:
        print(f"❌ PaddleOCR 処理失敗: {e}\n")

    # パターン2: マルチエンジンフォールバック
    try:
        print("【マルチエンジンフォールバック】")
        ocr = MultiEngineOCR()
        text, engine = ocr.extract_text_with_fallback(test_image)
        print(f"使用エンジン: {engine}")
        print(f"抽出されたテキスト: {text[:100]}...\n")
    except Exception as e:
        print(f"❌ OCR 処理失敗: {e}\n")

    # パターン3: 請求書処理
    try:
        print("【請求書OCR処理】")
        processor = InvoiceOCRProcessor()
        result = processor.process_invoice(test_image)
        print(f"結果: {result}\n")
    except Exception as e:
        print(f"❌ 請求書処理失敗: {e}\n")


if __name__ == "__main__":
    main()
