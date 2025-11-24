"""
Airレジ Webhookサーバー

Airレジからのデータを受信し、保存・分析を行うWebhookサーバー
"""
import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.webhook.auth import verify_airregi_auth, log_request
from src.webhook.handler import WebhookHandler
from src.utils.logger import Logger

# 環境変数読み込み
load_dotenv('config/.env')

# Flaskアプリ初期化
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ロガー初期化
logger = Logger('WebhookServer', os.getenv('LOG_DIR', './logs'))

# ハンドラー初期化
handler = WebhookHandler()


@app.route('/health', methods=['GET'])
def health_check():
    """ヘルスチェックエンドポイント"""
    logger.info("ヘルスチェック")
    return jsonify({
        "status": "ok",
        "service": "Airレジ Webhook Server",
        "version": "1.0.0"
    })


@app.route('/webhook/airregi/transactions', methods=['POST'])
@log_request()
@verify_airregi_auth
def receive_transactions():
    """
    取引データ受信エンドポイント

    Airレジからの取引データを受信し、処理します。
    """
    try:
        logger.info("取引データ受信")

        # リクエストボディ取得
        if not request.is_json:
            logger.warning("Content-Type が application/json ではありません")
            return jsonify({"error": "Content-Type must be application/json"}), 400

        payload = request.get_json()

        if not payload:
            logger.warning("ペイロードが空です")
            return jsonify({"error": "Empty payload"}), 400

        logger.info(f"ペイロードサイズ: {len(str(payload))} bytes")

        # データ処理
        result = handler.process_transaction_data(payload)

        # 分析処理トリガー（非同期推奨）
        handler.trigger_analysis(result['filename'])

        return jsonify(result), 200

    except ValueError as e:
        logger.error(f"バリデーションエラー: {str(e)}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500


@app.route('/webhook/airregi/settlements', methods=['POST'])
@log_request()
@verify_airregi_auth
def receive_settlements():
    """
    精算データ受信エンドポイント

    Airレジからの精算データを受信し、処理します。
    """
    try:
        logger.info("精算データ受信")

        # リクエストボディ取得
        if not request.is_json:
            logger.warning("Content-Type が application/json ではありません")
            return jsonify({"error": "Content-Type must be application/json"}), 400

        payload = request.get_json()

        if not payload:
            logger.warning("ペイロードが空です")
            return jsonify({"error": "Empty payload"}), 400

        logger.info(f"ペイロードサイズ: {len(str(payload))} bytes")

        # データ処理
        result = handler.process_settlement_data(payload)

        # 分析処理トリガー（非同期推奨）
        handler.trigger_analysis(result['filename'])

        return jsonify(result), 200

    except ValueError as e:
        logger.error(f"バリデーションエラー: {str(e)}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500


@app.route('/webhook/airregi', methods=['POST'])
@log_request()
@verify_airregi_auth
def receive_generic():
    """
    汎用Webhookエンドポイント

    データタイプを自動判別して処理します。
    """
    try:
        logger.info("汎用Webhook受信")

        # リクエストボディ取得
        if not request.is_json:
            logger.warning("Content-Type が application/json ではありません")
            return jsonify({"error": "Content-Type must be application/json"}), 400

        payload = request.get_json()

        if not payload:
            logger.warning("ペイロードが空です")
            return jsonify({"error": "Empty payload"}), 400

        logger.info(f"ペイロードサイズ: {len(str(payload))} bytes")

        # データタイプ判別（実際の仕様に合わせて調整）
        data_type = payload.get('type', 'unknown')

        if data_type == 'transaction' or 'transactions' in payload:
            result = handler.process_transaction_data(payload)
        elif data_type == 'settlement' or 'settlement' in payload:
            result = handler.process_settlement_data(payload)
        else:
            # 不明なタイプでも一旦保存
            logger.warning(f"不明なデータタイプ: {data_type}")
            result = handler.process_transaction_data(payload)

        # 分析処理トリガー（非同期推奨）
        handler.trigger_analysis(result['filename'])

        return jsonify(result), 200

    except ValueError as e:
        logger.error(f"バリデーションエラー: {str(e)}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(error):
    """404エラーハンドラー"""
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドラー"""
    logger.error(f"500 Internal Server Error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Airレジ Webhookサーバー 起動")
    logger.info("=" * 60)

    # 設定情報表示
    api_key = os.getenv('AIRREGI_API_KEY', '')
    logger.info(f"APIキー: {api_key[:10]}... (先頭10文字)")

    # 開発環境での起動
    port = int(os.getenv('WEBHOOK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'

    logger.info(f"ポート: {port}")
    logger.info(f"デバッグモード: {debug}")
    logger.info("")
    logger.info("利用可能なエンドポイント:")
    logger.info("  GET  /health")
    logger.info("  POST /webhook/airregi/transactions")
    logger.info("  POST /webhook/airregi/settlements")
    logger.info("  POST /webhook/airregi")
    logger.info("=" * 60)

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
