"""
Airレジ API接続テストスクリプト
"""
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api.client import AirRegiAPIClient
from src.utils.logger import Logger


def test_api_connection():
    """API接続テスト"""
    load_dotenv('config/.env')

    logger = Logger('APITest', os.getenv('LOG_DIR', './logs'))

    logger.info("=" * 60)
    logger.info("Airレジ API接続テスト")
    logger.info("=" * 60)

    try:
        # APIクライアント初期化
        logger.info("APIクライアント初期化中...")
        client = AirRegiAPIClient()

        # 環境変数確認
        api_key = os.getenv('AIRREGI_API_KEY')
        api_token = os.getenv('AIRREGI_API_TOKEN')
        base_url = os.getenv('AIRREGI_API_BASE_URL')

        logger.info(f"APIキー: {api_key[:10]}... (先頭10文字)")
        logger.info(f"APIトークン: {api_token[:10]}... (先頭10文字)")
        logger.info(f"ベースURL: {base_url}")

        # 接続テスト
        logger.info("\n接続テスト実行中...")
        logger.info("注意: 実際のエンドポイントが不明なため、エラーが発生する可能性があります")

        # エンドポイント候補をテスト
        test_endpoints = [
            'health',
            'status',
            'ping',
            'transactions',
            'sales/summary'
        ]

        success_count = 0

        for endpoint in test_endpoints:
            try:
                logger.info(f"\nエンドポイントテスト: /{endpoint}")
                response = client.get(endpoint)
                logger.info(f"✓ {endpoint}: 成功")
                logger.info(f"  レスポンス: {response}")
                success_count += 1

            except Exception as e:
                logger.warning(f"✗ {endpoint}: {str(e)}")

        logger.info("\n" + "=" * 60)
        logger.info(f"テスト結果: {success_count}/{len(test_endpoints)} エンドポイント成功")
        logger.info("=" * 60)

        if success_count > 0:
            logger.info("API接続テスト部分的に成功")
            return True
        else:
            logger.warning("すべてのエンドポイントでエラーが発生しました")
            logger.info("\n推奨アクション:")
            logger.info("1. Airレジの公式ドキュメントで正しいエンドポイントを確認")
            logger.info("2. APIキー・トークンが正しく設定されているか確認")
            logger.info("3. ネットワーク接続を確認")
            return False

    except Exception as e:
        logger.error(f"テスト中にエラーが発生: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    result = test_api_connection()
    sys.exit(0 if result else 1)
