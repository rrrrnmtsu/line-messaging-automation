"""
Airレジ売上データ分析システム - メインスクリプト
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api.client import AirRegiAPIClient
from src.data.fetcher import DataFetcher
from src.analysis.analyzer import SalesAnalyzer
from src.utils.logger import Logger


def main():
    """メイン処理"""
    # 環境変数読み込み
    load_dotenv('config/.env')

    logger = Logger('Main', os.getenv('LOG_DIR', './logs'))
    logger.info("=" * 60)
    logger.info("Airレジ売上データ分析システム 起動")
    logger.info("=" * 60)

    try:
        # 1. APIクライアント初期化
        logger.info("Step 1: APIクライアント初期化")
        client = AirRegiAPIClient()

        # 接続テスト
        logger.info("API接続テスト実行中...")
        # if client.test_connection():
        #     logger.info("API接続テスト成功")
        # else:
        #     logger.error("API接続テスト失敗")
        #     return

        # 2. データ取得
        logger.info("Step 2: データ取得")
        fetcher = DataFetcher(client)

        # 昨日のデータを取得
        yesterday = datetime.now() - timedelta(days=1)
        target_date_str = yesterday.strftime('%Y-%m-%d')

        logger.info(f"対象日: {target_date_str}")

        # 取引データ取得
        logger.info("取引データ取得中...")
        transaction_data = fetcher.fetch_daily_transactions(yesterday)

        # 精算データ取得
        logger.info("精算データ取得中...")
        settlement_data = fetcher.fetch_settlements(yesterday)

        # 3. データ分析
        logger.info("Step 3: データ分析")
        analyzer = SalesAnalyzer()

        # 取引データ読み込み
        transaction_file = f"transactions_{yesterday.strftime('%Y%m%d')}.json"
        df = analyzer.load_transaction_data(transaction_file)

        if df.empty:
            logger.warning("取引データが空のため、分析をスキップします")
            return

        # 各種分析実行
        logger.info("日次売上分析実行中...")
        daily_analysis = analyzer.analyze_daily_sales(df)

        logger.info("商品別売上分析実行中...")
        product_analysis = analyzer.analyze_product_sales(df)

        logger.info("支払方法別分析実行中...")
        payment_analysis = analyzer.analyze_payment_methods(df)

        # 4. レポート生成
        logger.info("Step 4: レポート生成")

        # サマリーレポート
        logger.info("サマリーレポート生成中...")
        summary_report = analyzer.generate_summary_report(
            daily_analysis,
            product_analysis,
            payment_analysis,
            target_date_str
        )

        # Excelレポート
        logger.info("Excelレポート生成中...")
        analyzer.export_to_excel(
            daily_analysis,
            product_analysis,
            payment_analysis,
            target_date_str
        )

        # 5. 結果表示
        logger.info("=" * 60)
        logger.info("分析結果サマリー")
        logger.info("=" * 60)
        logger.info(f"対象日: {target_date_str}")
        logger.info(f"総売上金額: ¥{daily_analysis.get('総売上金額', 0):,}")
        logger.info(f"取引件数: {daily_analysis.get('取引件数', 0)}件")
        logger.info(f"平均客単価: ¥{daily_analysis.get('平均客単価', 0):,}")
        logger.info("=" * 60)

        logger.info("処理完了")

    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


def run_weekly_analysis():
    """週次分析実行"""
    load_dotenv('config/.env')
    logger = Logger('WeeklyAnalysis', os.getenv('LOG_DIR', './logs'))

    logger.info("週次分析開始")

    try:
        client = AirRegiAPIClient()
        fetcher = DataFetcher(client)

        # 過去7日間のデータ取得
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=6)

        logger.info(f"期間: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

        all_data = fetcher.fetch_period_transactions(start_date, end_date)

        logger.info(f"週次分析完了: {len(all_data)}日分のデータを取得")

    except Exception as e:
        logger.error(f"週次分析エラー: {str(e)}")
        sys.exit(1)


def run_monthly_summary():
    """月次サマリー実行"""
    load_dotenv('config/.env')
    logger = Logger('MonthlySummary', os.getenv('LOG_DIR', './logs'))

    logger.info("月次サマリー開始")

    try:
        client = AirRegiAPIClient()
        fetcher = DataFetcher(client)

        # 先月のサマリー取得
        today = datetime.now()
        if today.month == 1:
            year = today.year - 1
            month = 12
        else:
            year = today.year
            month = today.month - 1

        logger.info(f"対象: {year}年{month}月")

        summary_data = fetcher.fetch_monthly_summary(year, month)

        logger.info("月次サマリー完了")

    except Exception as e:
        logger.error(f"月次サマリーエラー: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Airレジ売上データ分析システム')
    parser.add_argument(
        '--mode',
        choices=['daily', 'weekly', 'monthly'],
        default='daily',
        help='実行モード (daily: 日次, weekly: 週次, monthly: 月次)'
    )

    args = parser.parse_args()

    if args.mode == 'daily':
        main()
    elif args.mode == 'weekly':
        run_weekly_analysis()
    elif args.mode == 'monthly':
        run_monthly_summary()
