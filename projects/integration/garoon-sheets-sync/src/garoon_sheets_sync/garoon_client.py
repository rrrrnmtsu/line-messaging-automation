import base64
import logging
from typing import Dict, Generator, List, Optional
from urllib.parse import urljoin, urlparse

import requests

from .config import GaroonConfig


class GaroonClient:
    """Garoon REST API クライアント"""

    def __init__(self, config: GaroonConfig, session: Optional[requests.Session] = None) -> None:
        self.config = config
        self.session = session or requests.Session()
        self.logger = logging.getLogger(__name__)

    def fetch_workflow_requests(
        self,
        limit: int = 500,
        range_start: Optional[str] = None,
        range_end: Optional[str] = None,
        statuses: Optional[List[str]] = None,
    ) -> Generator[Dict, None, None]:
        """ワークフロー申請をページングで取得"""

        offset = 0
        endpoint = urljoin(self.config.base_url.rstrip("/") + "/", "workflow/admin/requests")
        params: Dict[str, str] = {"limit": str(limit)}

        if range_start:
            params["rangeStartApprovedAt"] = range_start
        if range_end:
            params["rangeEndApprovedAt"] = range_end
        if statuses:
            params["status"] = ",".join(statuses)

        while True:
            params["offset"] = str(offset)
            response = self.session.get(endpoint, headers=self._build_headers(), params=params, timeout=60)
            response.raise_for_status()
            data = response.json()

            requests_data = data.get("requests", [])
            self.logger.debug("Fetched %s requests (offset=%s)", len(requests_data), offset)

            for item in requests_data:
                yield item

            if not data.get("hasNext"):
                break

            offset = int(data.get("offset", 0)) + len(requests_data)

    def download_file(self, file_id: str) -> bytes:
        """添付ファイルをダウンロード"""

        endpoint = urljoin(
            self.config.base_url.rstrip("/") + "/",
            f"workflow/admin/files/{file_id}",
        )
        response = self.session.get(endpoint, headers=self._build_headers(), timeout=120)
        response.raise_for_status()
        return response.content

    def _build_headers(self) -> Dict[str, str]:
        """認証ヘッダーを組み立てる"""

        headers = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }

        method = self.config.auth_method.lower()
        if method == "basic":
            if not self.config.username or not self.config.password:
                raise ValueError("basic認証には GAROON_USERNAME / GAROON_PASSWORD が必要です")
            token = base64.b64encode(f"{self.config.username}:{self.config.password}".encode("utf-8")).decode("utf-8")
            headers["X-Cybozu-Authorization"] = token
        elif method == "oauth":
            headers["Authorization"] = f"Bearer {self._get_oauth_access_token()}"
        else:
            raise NotImplementedError(f"未対応の認証方式です: {self.config.auth_method}")

        return headers

    def _get_oauth_access_token(self) -> str:
        """OAuth リフレッシュトークンからアクセストークンを取得"""

        if not self.config.oauth_client_id or not self.config.oauth_client_secret or not self.config.oauth_refresh_token:
            raise ValueError("oauth認証にはクライアント情報とリフレッシュトークンが必要です")

        domain = self._extract_domain(self.config.base_url)
        token_url = urljoin(domain, "/oauth2/token")
        response = self.session.post(
            token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.config.oauth_refresh_token,
                "client_id": self.config.oauth_client_id,
                "client_secret": self.config.oauth_client_secret,
            },
            timeout=30,
        )
        response.raise_for_status()
        token_payload = response.json()
        return token_payload["access_token"]

    @staticmethod
    def _extract_domain(base_url: str) -> str:
        """ベースURLからドメイン部分を抽出"""

        parsed = urlparse(base_url)
        return f"{parsed.scheme}://{parsed.netloc}"
