"""
データ取得モジュール
"""
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
from src.api.client import AirRegiAPIClient
from src.utils.logger import Logger


class DataFetcher:
    """データ取得クラス"""

    def __init__(self, client: Optional[AirRegiAPIClient] = None):
        """
        初期化

        Args:
            client: APIクライアント（省略時は新規作成）
        """
        self.client = client or AirRegiAPIClient()
        self.logger = Logger('DataFetcher', os.getenv('LOG_DIR', './logs'))
        self.raw_data_dir = os.getenv('RAW_DATA_DIR', './data/raw')

        # データディレクトリ作成
        Path(self.raw_data_dir).mkdir(parents=True, exist_ok=True)

        self.logger.info("DataFetcher初期化完了")

    def fetch_daily_transactions(
        self,
        target_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        日次取引データ取得

        Args:
            target_date: 対象日付（省略時は昨日）

        Returns:
            取引データ
        """
        if not target_date:
            target_date = datetime.now() - timedelta(days=1)

        self.logger.info(f"日次取引データ取得開始: {target_date.strftime('%Y-%m-%d')}")

        try:
            data = self.client.get_transactions(
                start_date=target_date,
                end_date=target_date
            )

            # データ保存
            self._save_raw_data(
                data,
                f"transactions_{target_date.strftime('%Y%m%d')}.json"
            )

            self.logger.info(f"日次取引データ取得完了: {len(data.get('transactions', []))}件")

            return data

        except Exception as e:
            self.logger.error(f"日次取引データ取得エラー: {str(e)}")
            raise

    def fetch_period_transactions(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        期間指定取引データ取得

        Args:
            start_date: 開始日
            end_date: 終了日

        Returns:
            取引データリスト
        """
        self.logger.info(
            f"期間取引データ取得開始: {start_date.strftime('%Y-%m-%d')} ~ "
            f"{end_date.strftime('%Y-%m-%d')}"
        )

        all_data = []
        current_date = start_date

        while current_date <= end_date:
            try:
                daily_data = self.fetch_daily_transactions(current_date)
                all_data.append(daily_data)

            except Exception as e:
                self.logger.warning(
                    f"{current_date.strftime('%Y-%m-%d')}のデータ取得失敗: {str(e)}"
                )

            current_date += timedelta(days=1)

        self.logger.info(f"期間取引データ取得完了: {len(all_data)}日分")

        return all_data

    def fetch_monthly_summary(
        self,
        year: int,
        month: int
    ) -> Dict[str, Any]:
        """
        月次サマリーデータ取得

        Args:
            year: 年
            month: 月

        Returns:
            月次サマリーデータ
        """
        self.logger.info(f"月次サマリーデータ取得開始: {year}年{month}月")

        start_date = datetime(year, month, 1)

        # 月末日を計算
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)

        try:
            data = self.client.get_sales_summary(
                start_date=start_date,
                end_date=end_date
            )

            # データ保存
            self._save_raw_data(
                data,
                f"summary_{year}{month:02d}.json"
            )

            self.logger.info(f"月次サマリーデータ取得完了")

            return data

        except Exception as e:
            self.logger.error(f"月次サマリーデータ取得エラー: {str(e)}")
            raise

    def fetch_settlements(
        self,
        target_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        精算データ取得

        Args:
            target_date: 対象日付（省略時は昨日）

        Returns:
            精算データ
        """
        if not target_date:
            target_date = datetime.now() - timedelta(days=1)

        self.logger.info(f"精算データ取得開始: {target_date.strftime('%Y-%m-%d')}")

        try:
            data = self.client.get_settlements(date=target_date)

            # データ保存
            self._save_raw_data(
                data,
                f"settlement_{target_date.strftime('%Y%m%d')}.json"
            )

            self.logger.info(f"精算データ取得完了")

            return data

        except Exception as e:
            self.logger.error(f"精算データ取得エラー: {str(e)}")
            raise

    def _save_raw_data(self, data: Dict[str, Any], filename: str):
        """
        生データ保存

        Args:
            data: データ
            filename: ファイル名
        """
        filepath = os.path.join(self.raw_data_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.logger.info(f"データ保存完了: {filepath}")

        except Exception as e:
            self.logger.error(f"データ保存エラー: {str(e)}")
            raise
