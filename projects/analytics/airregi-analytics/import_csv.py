"""
Airレジ CSVインポートスクリプト

Airレジからエクスポートした売上CSVファイルをインポートし、分析・レポート生成を行います。
"""
import os
import sys
import argparse
from datetime import datetime
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.analysis.analyzer import SalesAnalyzer
from src.utils.logger import Logger


class CSVImporter:
    """CSVインポートクラス"""

    def __init__(self):
        """初期化"""
        load_dotenv('config/.env')
        self.logger = Logger('CSVImporter', os.getenv('LOG_DIR', './logs'))
        self.raw_data_dir = os.getenv('RAW_DATA_DIR', './data/raw')
        Path(self.raw_data_dir).mkdir(parents=True, exist_ok=True)

        self.logger.info("CSVImporter初期化完了")

    def import_csv(self, csv_file: str, data_type: str = 'transactions'):
        """
        CSVファイルをインポート

        Args:
            csv_file: CSVファイルパス
            data_type: データタイプ (transactions, settlement)

        Returns:
            インポート結果
        """
        try:
            self.logger.info(f"CSVインポート開始: {csv_file}")

            # ファイル存在確認
            if not os.path.exists(csv_file):
                raise FileNotFoundError(f"ファイルが見つかりません: {csv_file}")

            # CSVファイル読み込み
            df = pd.read_csv(csv_file, encoding='utf-8-sig')  # BOM付きUTF-8対応
            self.logger.info(f"CSVファイル読み込み完了: {len(df)}行")

            # データ検証
            self._validate_dataframe(df, data_type)

            # JSON形式に変換して保存
            json_file = self._save_as_json(df, data_type)

            self.logger.info(f"CSVインポート完了: {json_file}")

            return {
                "status": "success",
                "rows": len(df),
                "json_file": json_file
            }

        except Exception as e:
            self.logger.error(f"CSVインポートエラー: {str(e)}")
            raise

    def _validate_dataframe(self, df: pd.DataFrame, data_type: str):
        """
        DataFrameのバリデーション

        Args:
            df: pandas DataFrame
            data_type: データタイプ
        """
        if df.empty:
            raise ValueError("データが空です")

        self.logger.info(f"カラム: {df.columns.tolist()}")

    def _save_as_json(self, df: pd.DataFrame, data_type: str) -> str:
        """
        DataFrameをJSON形式で保存

        Args:
            df: pandas DataFrame
            data_type: データタイプ

        Returns:
            保存したファイルパス
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"imported_{data_type}_{timestamp}.json"
        filepath = os.path.join(self.raw_data_dir, filename)

        # Airレジデータ構造に変換
        data = {
            "imported_at": datetime.now().isoformat(),
            "source": "csv_import",
            "data_type": data_type,
            "transactions": df.to_dict('records')
        }

        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

        self.logger.info(f"JSON保存完了: {filepath}")

        return filepath


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='Airレジ CSVインポート')
    parser.add_argument('--file', '-f', required=True, help='CSVファイルパス')
    parser.add_argument('--type', '-t', default='transactions',
                        choices=['transactions', 'settlement'],
                        help='データタイプ')
    parser.add_argument('--analyze', '-a', action='store_true',
                        help='インポート後に分析を実行')

    args = parser.parse_args()

    logger = Logger('Main', os.getenv('LOG_DIR', './logs'))

    logger.info("=" * 60)
    logger.info("Airレジ CSVインポート 開始")
    logger.info("=" * 60)
    logger.info(f"ファイル: {args.file}")
    logger.info(f"タイプ: {args.type}")

    try:
        # CSVインポート
        importer = CSVImporter()
        result = importer.import_csv(args.file, args.type)

        logger.info(f"インポート成功: {result['rows']}行")
        logger.info(f"保存先: {result['json_file']}")

        # 分析実行
        if args.analyze:
            logger.info("\n分析を開始します...")

            analyzer = SalesAnalyzer()

            # JSON to DataFrame
            import json
            with open(result['json_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)

            df = pd.DataFrame(data['transactions'])

            if not df.empty:
                # 日次売上分析
                logger.info("日次売上分析実行中...")
                daily_analysis = analyzer.analyze_daily_sales(df)

                # 商品別売上分析
                logger.info("商品別売上分析実行中...")
                product_analysis = analyzer.analyze_product_sales(df)

                # 支払方法別分析
                logger.info("支払方法別分析実行中...")
                payment_analysis = analyzer.analyze_payment_methods(df)

                # レポート生成
                target_date_str = datetime.now().strftime('%Y-%m-%d')
                summary_report = analyzer.generate_summary_report(
                    daily_analysis,
                    product_analysis,
                    payment_analysis,
                    target_date_str
                )

                analyzer.export_to_excel(
                    daily_analysis,
                    product_analysis,
                    payment_analysis,
                    target_date_str
                )

                logger.info("\n分析完了！")
                logger.info(f"総売上金額: ¥{daily_analysis.get('総売上金額', 0):,}")
                logger.info(f"取引件数: {daily_analysis.get('取引件数', 0)}件")

        logger.info("=" * 60)
        logger.info("処理完了")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"エラー: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
