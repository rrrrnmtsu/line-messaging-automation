"""
サンプルデータ分析スクリプト

生成されたサンプルデータを使用してシステムの動作確認を行います。
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.analysis.analyzer import SalesAnalyzer
from src.utils.logger import Logger


def main():
    """メイン処理"""
    load_dotenv('config/.env')

    logger = Logger('SampleDataAnalysis', os.getenv('LOG_DIR', './logs'))

    logger.info("=" * 60)
    logger.info("サンプルデータ分析開始")
    logger.info("=" * 60)

    try:
        analyzer = SalesAnalyzer()

        # 昨日のサンプルデータを分析
        yesterday = datetime.now() - timedelta(days=1)
        target_date_str = yesterday.strftime('%Y-%m-%d')
        transaction_file = f"transactions_{yesterday.strftime('%Y%m%d')}.json"

        logger.info(f"対象日: {target_date_str}")
        logger.info(f"対象ファイル: {transaction_file}")

        # データ読み込み
        logger.info("\n[1/4] データ読み込み中...")
        df = analyzer.load_transaction_data(transaction_file)

        if df.empty:
            logger.warning("データが空です。先にサンプルデータを生成してください。")
            logger.info("\nサンプルデータ生成コマンド:")
            logger.info("  python create_sample_data.py")
            return

        logger.info(f"データ読み込み完了: {len(df)}件")

        # 日次売上分析
        logger.info("\n[2/4] 日次売上分析実行中...")
        daily_analysis = analyzer.analyze_daily_sales(df)

        # 商品別売上分析
        logger.info("\n[3/4] 商品別売上分析実行中...")
        product_analysis = analyzer.analyze_product_sales(df)

        # 支払方法別分析
        logger.info("\n[4/4] 支払方法別分析実行中...")
        payment_analysis = analyzer.analyze_payment_methods(df)

        # レポート生成
        logger.info("\nレポート生成中...")

        # サマリーレポート
        summary_report = analyzer.generate_summary_report(
            daily_analysis,
            product_analysis,
            payment_analysis,
            target_date_str
        )

        # Excelレポート
        analyzer.export_to_excel(
            daily_analysis,
            product_analysis,
            payment_analysis,
            target_date_str
        )

        # 結果表示
        logger.info("\n" + "=" * 60)
        logger.info("分析結果サマリー")
        logger.info("=" * 60)
        logger.info(f"対象日: {target_date_str}")
        logger.info(f"総売上金額: ¥{daily_analysis.get('総売上金額', 0):,}")
        logger.info(f"取引件数: {daily_analysis.get('取引件数', 0)}件")
        logger.info(f"平均客単価: ¥{daily_analysis.get('平均客単価', 0):,}")
        logger.info(f"最大取引金額: ¥{daily_analysis.get('最大取引金額', 0):,}")
        logger.info(f"最小取引金額: ¥{daily_analysis.get('最小取引金額', 0):,}")

        if '時間帯別売上' in daily_analysis:
            logger.info("\n時間帯別売上TOP3:")
            hourly_sales = daily_analysis['時間帯別売上']
            sorted_hours = sorted(hourly_sales.items(), key=lambda x: x[1], reverse=True)[:3]
            for hour, amount in sorted_hours:
                logger.info(f"  {hour}時台: ¥{amount:,}")

        if not product_analysis.empty:
            logger.info("\n商品別売上TOP5:")
            top5 = product_analysis.head(5)
            for idx, (product_name, row) in enumerate(top5.iterrows(), 1):
                logger.info(f"  {idx}. {product_name}: ¥{int(row['売上金額']):,} ({int(row['販売回数'])}回)")

        if payment_analysis:
            logger.info("\n支払方法別:")
            for method, data in payment_analysis.items():
                logger.info(f"  {method}: ¥{data['金額']:,} ({data['構成比']}%)")

        logger.info("=" * 60)
        logger.info("\n生成ファイル:")
        logger.info(f"  - data/processed/summary_report_{target_date_str.replace('-', '')}.json")
        logger.info(f"  - reports/sales_report_{target_date_str.replace('-', '')}.xlsx")
        logger.info("\n分析完了！")

    except FileNotFoundError:
        logger.error("サンプルデータが見つかりません")
        logger.info("\nサンプルデータを生成してください:")
        logger.info("  python create_sample_data.py")
        sys.exit(1)

    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
