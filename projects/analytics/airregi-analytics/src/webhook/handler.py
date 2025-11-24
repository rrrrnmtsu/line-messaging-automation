"""
Webhookデータハンドラー
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from src.utils.logger import Logger


class WebhookHandler:
    """Webhookデータ処理クラス"""

    def __init__(self):
        """初期化"""
        self.logger = Logger('WebhookHandler', os.getenv('LOG_DIR', './logs'))
        self.raw_data_dir = os.getenv('RAW_DATA_DIR', './data/raw')
        Path(self.raw_data_dir).mkdir(parents=True, exist_ok=True)

        self.logger.info("WebhookHandler初期化完了")

    def process_transaction_data(self, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        取引データ処理

        Args:
            payload: Airレジから受信したデータ

        Returns:
            処理結果
        """
        try:
            self.logger.info("取引データ処理開始")

            # データの基本検証
            if not self._validate_payload(payload):
                raise ValueError("無効なデータ形式")

            # データ保存
            filename = self._save_webhook_data(payload, 'transaction')

            self.logger.info(f"取引データ処理完了: {filename}")

            return {
                "status": "success",
                "message": "Data processed successfully",
                "filename": filename
            }

        except Exception as e:
            self.logger.error(f"取引データ処理エラー: {str(e)}")
            raise

    def process_settlement_data(self, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        精算データ処理

        Args:
            payload: Airレジから受信したデータ

        Returns:
            処理結果
        """
        try:
            self.logger.info("精算データ処理開始")

            # データの基本検証
            if not self._validate_payload(payload):
                raise ValueError("無効なデータ形式")

            # データ保存
            filename = self._save_webhook_data(payload, 'settlement')

            self.logger.info(f"精算データ処理完了: {filename}")

            return {
                "status": "success",
                "message": "Settlement data processed successfully",
                "filename": filename
            }

        except Exception as e:
            self.logger.error(f"精算データ処理エラー: {str(e)}")
            raise

    def _validate_payload(self, payload: Dict[str, Any]) -> bool:
        """
        ペイロードの基本検証

        Args:
            payload: 検証対象データ

        Returns:
            検証結果
        """
        if not isinstance(payload, dict):
            self.logger.error("ペイロードがdict型ではありません")
            return False

        # 必須フィールドのチェック（実際の仕様に合わせて調整）
        # required_fields = ['transaction_id', 'timestamp', 'data']
        # for field in required_fields:
        #     if field not in payload:
        #         self.logger.error(f"必須フィールドが不足: {field}")
        #         return False

        return True

    def _save_webhook_data(self, payload: Dict[str, Any], data_type: str) -> str:
        """
        Webhookデータをファイル保存

        Args:
            payload: 保存対象データ
            data_type: データタイプ (transaction, settlement等)

        Returns:
            保存したファイル名
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"webhook_{data_type}_{timestamp}.json"
        filepath = os.path.join(self.raw_data_dir, filename)

        try:
            # メタデータ追加
            data_with_meta = {
                "received_at": datetime.now().isoformat(),
                "data_type": data_type,
                "payload": payload
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_with_meta, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Webhookデータ保存: {filepath}")

            return filename

        except Exception as e:
            self.logger.error(f"ファイル保存エラー: {str(e)}")
            raise

    def trigger_analysis(self, filename: str):
        """
        分析処理のトリガー

        Args:
            filename: 分析対象ファイル名
        """
        try:
            self.logger.info(f"分析処理トリガー: {filename}")

            # TODO: 実際の分析処理を呼び出し
            # from src.analysis.analyzer import SalesAnalyzer
            # analyzer = SalesAnalyzer()
            # analyzer.analyze(filename)

            self.logger.info("分析処理完了")

        except Exception as e:
            self.logger.error(f"分析処理エラー: {str(e)}")
            # 分析エラーでもWebhook受信は成功として扱う
