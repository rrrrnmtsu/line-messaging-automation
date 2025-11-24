import json
from pathlib import Path
from typing import Dict, Iterable, List

from google.oauth2 import credentials, service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .config import GoogleSheetsConfig

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class SheetsClient:
    """Google Sheets API クライアント"""

    def __init__(self, config: GoogleSheetsConfig) -> None:
        self.config = config
        self.service = build("sheets", "v4", credentials=self._load_credentials(), cache_discovery=False)

    def upsert_records(self, records: Iterable[Dict], headers: List[str]) -> None:
        """レコードをシートに書き戻す（全件更新）"""

        rows = [[record.get(header, "") for header in headers] for record in records]
        body = {"values": [headers] + rows}
        target_range = f"{self.config.worksheet_name}!A1"

        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.config.spreadsheet_id,
                range=target_range,
                valueInputOption="RAW",
                body=body,
            ).execute()
        except HttpError as error:
            raise RuntimeError(f"Google Sheets API 更新に失敗しました: {error}") from error

    def _load_credentials(self):
        """認証情報を読み込む"""

        if self.config.service_account_file:
            file_path = Path(self.config.service_account_file)
            if not file_path.exists():
                raise FileNotFoundError(f"サービスアカウントファイルが見つかりません: {file_path}")
            return service_account.Credentials.from_service_account_file(
                str(file_path),
                scopes=SCOPES,
            )

        if self.config.oauth_token_file:
            token_path = Path(self.config.oauth_token_file)
            if not token_path.exists():
                raise FileNotFoundError(f"OAuthトークンファイルが見つかりません: {token_path}")
            with token_path.open("r", encoding="utf-8") as file:
                token_data = json.load(file)
            return credentials.Credentials.from_authorized_user_info(token_data, scopes=SCOPES)

        raise ValueError("Google Sheets 認証情報が設定されていません")
