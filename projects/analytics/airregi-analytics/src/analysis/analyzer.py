"""
データ分析モジュール
"""
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.utils.logger import Logger


class SalesAnalyzer:
    """売上分析クラス"""

    def __init__(self):
        """初期化"""
        self.logger = Logger('SalesAnalyzer', os.getenv('LOG_DIR', './logs'))
        self.raw_data_dir = os.getenv('RAW_DATA_DIR', './data/raw')
        self.processed_data_dir = os.getenv('PROCESSED_DATA_DIR', './data/processed')

        Path(self.processed_data_dir).mkdir(parents=True, exist_ok=True)

        self.logger.info("SalesAnalyzer初期化完了")

    def load_transaction_data(self, filename: str) -> pd.DataFrame:
        """
        取引データ読み込み

        Args:
            filename: ファイル名

        Returns:
            DataFrameオブジェクト
        """
        filepath = os.path.join(self.raw_data_dir, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 取引データをDataFrameに変換
            transactions = data.get('transactions', [])

            if not transactions:
                self.logger.warning(f"取引データが空です: {filename}")
                return pd.DataFrame()

            df = pd.DataFrame(transactions)

            # 日時型変換
            if 'transaction_datetime' in df.columns:
                df['transaction_datetime'] = pd.to_datetime(df['transaction_datetime'])

            self.logger.info(f"取引データ読み込み完了: {len(df)}件")

            return df

        except Exception as e:
            self.logger.error(f"データ読み込みエラー: {str(e)}")
            raise

    def analyze_daily_sales(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        日次売上分析

        Args:
            df: 取引データ

        Returns:
            分析結果
        """
        if df.empty:
            return {}

        try:
            analysis = {
                '総売上金額': int(df['amount'].sum()) if 'amount' in df.columns else 0,
                '取引件数': len(df),
                '平均客単価': int(df['amount'].mean()) if 'amount' in df.columns else 0,
                '最大取引金額': int(df['amount'].max()) if 'amount' in df.columns else 0,
                '最小取引金額': int(df['amount'].min()) if 'amount' in df.columns else 0,
            }

            # 時間帯別分析
            if 'transaction_datetime' in df.columns:
                df['hour'] = df['transaction_datetime'].dt.hour
                hourly_sales = df.groupby('hour')['amount'].sum().to_dict()
                analysis['時間帯別売上'] = {int(k): int(v) for k, v in hourly_sales.items()}

            self.logger.info("日次売上分析完了")

            return analysis

        except Exception as e:
            self.logger.error(f"日次売上分析エラー: {str(e)}")
            raise

    def analyze_product_sales(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        商品別売上分析

        Args:
            df: 取引データ

        Returns:
            商品別分析DataFrame
        """
        if df.empty or 'product_name' not in df.columns:
            return pd.DataFrame()

        try:
            product_analysis = df.groupby('product_name').agg({
                'amount': ['sum', 'count', 'mean'],
                'quantity': 'sum'
            }).round(0)

            product_analysis.columns = ['売上金額', '販売回数', '平均単価', '販売数量']
            product_analysis = product_analysis.sort_values('売上金額', ascending=False)

            self.logger.info(f"商品別売上分析完了: {len(product_analysis)}商品")

            return product_analysis

        except Exception as e:
            self.logger.error(f"商品別売上分析エラー: {str(e)}")
            raise

    def analyze_payment_methods(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        支払方法別分析

        Args:
            df: 取引データ

        Returns:
            支払方法別分析
        """
        if df.empty or 'payment_method' not in df.columns:
            return {}

        try:
            payment_analysis = df.groupby('payment_method').agg({
                'amount': ['sum', 'count']
            }).round(0)

            payment_analysis.columns = ['金額', '件数']

            result = {
                method: {
                    '金額': int(row['金額']),
                    '件数': int(row['件数']),
                    '構成比': round(row['金額'] / df['amount'].sum() * 100, 1)
                }
                for method, row in payment_analysis.iterrows()
            }

            self.logger.info("支払方法別分析完了")

            return result

        except Exception as e:
            self.logger.error(f"支払方法別分析エラー: {str(e)}")
            raise

    def generate_summary_report(
        self,
        daily_analysis: Dict[str, Any],
        product_analysis: pd.DataFrame,
        payment_analysis: Dict[str, Any],
        target_date: str
    ) -> Dict[str, Any]:
        """
        サマリーレポート生成

        Args:
            daily_analysis: 日次分析
            product_analysis: 商品別分析
            payment_analysis: 支払方法別分析
            target_date: 対象日付

        Returns:
            サマリーレポート
        """
        report = {
            '対象日': target_date,
            '生成日時': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '日次サマリー': daily_analysis,
            '商品別TOP10': product_analysis.head(10).to_dict() if not product_analysis.empty else {},
            '支払方法別': payment_analysis
        }

        # レポート保存
        report_filename = f"summary_report_{target_date.replace('-', '')}.json"
        report_path = os.path.join(self.processed_data_dir, report_filename)

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            self.logger.info(f"サマリーレポート生成完了: {report_path}")

        except Exception as e:
            self.logger.error(f"レポート保存エラー: {str(e)}")

        return report

    def export_to_excel(
        self,
        daily_analysis: Dict[str, Any],
        product_analysis: pd.DataFrame,
        payment_analysis: Dict[str, Any],
        target_date: str
    ):
        """
        Excel形式でエクスポート

        Args:
            daily_analysis: 日次分析
            product_analysis: 商品別分析
            payment_analysis: 支払方法別分析
            target_date: 対象日付
        """
        excel_filename = f"sales_report_{target_date.replace('-', '')}.xlsx"
        excel_path = os.path.join(os.getenv('REPORT_DIR', './reports'), excel_filename)

        try:
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                # 日次サマリー
                daily_df = pd.DataFrame([daily_analysis]).T
                daily_df.columns = ['値']
                daily_df.to_excel(writer, sheet_name='日次サマリー')

                # 商品別売上
                if not product_analysis.empty:
                    product_analysis.to_excel(writer, sheet_name='商品別売上')

                # 支払方法別
                if payment_analysis:
                    payment_df = pd.DataFrame(payment_analysis).T
                    payment_df.to_excel(writer, sheet_name='支払方法別')

            self.logger.info(f"Excelレポート生成完了: {excel_path}")

        except Exception as e:
            self.logger.error(f"Excelエクスポートエラー: {str(e)}")
            raise
