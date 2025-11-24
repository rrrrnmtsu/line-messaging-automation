"""
Airレジ APIクライアント
"""
import os
import requests
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
from src.utils.logger import Logger


class AirRegiAPIClient:
    """Airレジ APIクライアント"""

    def __init__(self, api_key: Optional[str] = None, api_token: Optional[str] = None):
        """
        初期化

        Args:
            api_key: APIキー（省略時は環境変数から取得）
            api_token: APIトークン（省略時は環境変数から取得）
        """
        load_dotenv('config/.env')

        self.api_key = api_key or os.getenv('AIRREGI_API_KEY')
        self.api_token = api_token or os.getenv('AIRREGI_API_TOKEN')
        self.base_url = os.getenv('AIRREGI_API_BASE_URL', 'https://api.airregi.jp/v1')

        self.logger = Logger('AirRegiAPI', os.getenv('LOG_DIR', './logs'))

        if not self.api_key or not self.api_token:
            raise ValueError("APIキーとトークンが設定されていません")

        self.session = requests.Session()
        self.session.headers.update(self._get_auth_headers())

        self.logger.info("Airレジ APIクライアント初期化完了")

    def _get_auth_headers(self) -> Dict[str, str]:
        """
        認証ヘッダーを取得

        Returns:
            認証ヘッダー辞書
        """
        return {
            'X-API-Key': self.api_key,
            'X-API-Token': self.api_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        APIリクエスト実行

        Args:
            method: HTTPメソッド
            endpoint: エンドポイント
            params: クエリパラメータ
            data: リクエストボディ
            max_retries: 最大リトライ回数

        Returns:
            レスポンスデータ
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        for attempt in range(max_retries):
            try:
                self.logger.info(f"API Request: {method} {url}")

                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=30
                )

                # レート制限対応
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    self.logger.warning(f"レート制限: {retry_after}秒待機")
                    time.sleep(retry_after)
                    continue

                response.raise_for_status()

                result = response.json()
                self.logger.info(f"API Response: {response.status_code}")

                return result

            except requests.exceptions.RequestException as e:
                self.logger.error(f"APIリクエストエラー (試行 {attempt + 1}/{max_retries}): {str(e)}")

                if attempt == max_retries - 1:
                    raise

                time.sleep(2 ** attempt)  # 指数バックオフ

        raise Exception("APIリクエスト失敗")

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GETリクエスト"""
        return self._request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POSTリクエスト"""
        return self._request('POST', endpoint, data=data)

    def get_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        取引情報取得

        Args:
            start_date: 開始日時
            end_date: 終了日時

        Returns:
            取引データ
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)
        if not end_date:
            end_date = datetime.now()

        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }

        self.logger.info(f"取引情報取得: {params['start_date']} ~ {params['end_date']}")

        return self.get('transactions', params=params)

    def get_sales_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        売上サマリー取得

        Args:
            start_date: 開始日時
            end_date: 終了日時

        Returns:
            売上サマリーデータ
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()

        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }

        self.logger.info(f"売上サマリー取得: {params['start_date']} ~ {params['end_date']}")

        return self.get('sales/summary', params=params)

    def get_settlements(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        精算情報取得

        Args:
            date: 対象日付

        Returns:
            精算データ
        """
        if not date:
            date = datetime.now()

        params = {'date': date.strftime('%Y-%m-%d')}

        self.logger.info(f"精算情報取得: {params['date']}")

        return self.get('settlements', params=params)

    def test_connection(self) -> bool:
        """
        接続テスト

        Returns:
            接続成功: True、失敗: False
        """
        try:
            # ヘルスチェックまたは簡単なエンドポイントを試行
            self.logger.info("API接続テスト開始")
            result = self.get('health')
            self.logger.info("API接続テスト成功")
            return True
        except Exception as e:
            self.logger.error(f"API接続テスト失敗: {str(e)}")
            return False
