"""
Webhook認証ミドルウェア
"""
import os
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv
from src.utils.logger import Logger

load_dotenv('config/.env')

logger = Logger('WebhookAuth', os.getenv('LOG_DIR', './logs'))


def verify_airregi_auth(f):
    """
    Airレジからのリクエストを認証するデコレーター

    Args:
        f: デコレート対象の関数

    Returns:
        認証後の関数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 環境変数から認証情報取得
        expected_api_key = os.getenv('AIRREGI_API_KEY')
        expected_api_token = os.getenv('AIRREGI_API_TOKEN')

        if not expected_api_key or not expected_api_token:
            logger.error("認証情報が環境変数に設定されていません")
            return jsonify({"error": "Server configuration error"}), 500

        # リクエストヘッダーから認証情報取得
        # 注: 実際の仕様に合わせて調整が必要
        api_key = request.headers.get('X-API-Key') or request.json.get('api_key')
        api_token = request.headers.get('X-API-Token') or request.json.get('api_token')

        # 認証チェック
        if not api_key or not api_token:
            logger.warning(f"認証情報なしのリクエスト: {request.remote_addr}")
            return jsonify({"error": "Authentication required"}), 401

        if api_key != expected_api_key or api_token != expected_api_token:
            logger.warning(f"認証失敗: {request.remote_addr}")
            return jsonify({"error": "Invalid credentials"}), 403

        logger.info(f"認証成功: {request.remote_addr}")

        return f(*args, **kwargs)

    return decorated_function


def log_request():
    """
    リクエスト情報をログに記録するデコレーター

    Returns:
        ログ記録後の関数
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logger.info(f"Webhook受信: {request.method} {request.path}")
            logger.info(f"送信元: {request.remote_addr}")
            logger.info(f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}")

            # Content-Typeチェック
            content_type = request.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                logger.warning(f"不正なContent-Type: {content_type}")

            return f(*args, **kwargs)

        return decorated_function
    return decorator
