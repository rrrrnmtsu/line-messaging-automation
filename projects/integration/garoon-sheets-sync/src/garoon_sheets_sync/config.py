import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv


@dataclass
class GaroonConfig:
    """Garoon API 接続設定"""

    base_url: str
    auth_method: str
    username: Optional[str]
    password: Optional[str]
    oauth_client_id: Optional[str]
    oauth_client_secret: Optional[str]
    oauth_refresh_token: Optional[str]
    statuses: List[str]
    range_start: Optional[str]
    range_end: Optional[str]


@dataclass
class GoogleSheetsConfig:
    """Google Sheets 接続設定"""

    spreadsheet_id: str
    worksheet_name: str
    service_account_file: Optional[str]
    oauth_token_file: Optional[str]


@dataclass
class AppConfig:
    """アプリ全体の設定"""

    garoon: GaroonConfig
    sheets: GoogleSheetsConfig


def load_config(env_file: str = ".env") -> AppConfig:
    """環境変数から設定を読み込む"""

    if os.path.exists(env_file):
        # dotenvが存在すれば読み込む
        load_dotenv(env_file)

    statuses_value = os.getenv("GAROON_STATUSES", "COMPLETED")
    statuses = [value.strip() for value in statuses_value.split(",") if value.strip()]

    garoon = GaroonConfig(
        base_url=os.environ["GAROON_BASE_URL"],
        auth_method=os.getenv("GAROON_AUTH_METHOD", "basic"),
        username=os.getenv("GAROON_USERNAME"),
        password=os.getenv("GAROON_PASSWORD"),
        oauth_client_id=os.getenv("GAROON_OAUTH_CLIENT_ID"),
        oauth_client_secret=os.getenv("GAROON_OAUTH_CLIENT_SECRET"),
        oauth_refresh_token=os.getenv("GAROON_OAUTH_REFRESH_TOKEN"),
        statuses=statuses,
        range_start=os.getenv("GAROON_RANGE_START"),
        range_end=os.getenv("GAROON_RANGE_END"),
    )

    sheets = GoogleSheetsConfig(
        spreadsheet_id=os.environ["GOOGLE_SPREADSHEET_ID"],
        worksheet_name=os.getenv("GOOGLE_WORKSHEET_NAME", "Workflow"),
        service_account_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"),
        oauth_token_file=os.getenv("GOOGLE_OAUTH_TOKEN_FILE"),
    )

    return AppConfig(garoon=garoon, sheets=sheets)
