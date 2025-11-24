import argparse
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .config import AppConfig, load_config
from .garoon_client import GaroonClient
from .sheets_client import SheetsClient

DEFAULT_HEADERS = [
    "requestId",
    "subject",
    "status",
    "statusLabel",
    "createdAt",
    "approvedAt",
    "applicantName",
    "applicantCode",
    "approvers",
    "fileRefs",
]


@dataclass
class SyncResult:
    """同期処理の結果"""

    synced_at: str
    record_count: int
    dry_run: bool
    sheet_updated: bool
    records: List[Dict[str, Optional[str]]]
    output_path: Optional[str]


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析"""

    parser = argparse.ArgumentParser(description="Garoon ワークフローを Google Sheets に同期")
    parser.add_argument("--env", default=".env", help="環境変数ファイルのパス")
    parser.add_argument("--range-start", dest="range_start", help="承認日時の開始 (RFC3339)")
    parser.add_argument("--range-end", dest="range_end", help="承認日時の終了 (RFC3339)")
    parser.add_argument("--statuses", nargs="*", help="取得するステータス (複数指定可)")
    parser.add_argument("--limit", type=int, default=500, help="1リクエストあたりの件数 (1-1000)")
    parser.add_argument(
        "--output",
        default="shared/results/codex/latest_sync.json",
        help="同期結果JSONの出力先 (書き出しなしは空文字)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Sheetsを更新せずに処理を終了")
    return parser.parse_args()


def normalize_request(request: Dict) -> Dict[str, Optional[str]]:
    """Garoon申請のJSONをフラット化"""

    status = request.get("status", {})
    applicant = request.get("applicant", {})

    approver_names: List[str] = []
    for step in request.get("steps", []):
        users = step.get("users") or step.get("stepUsers") or []
        for user in users:
            name = user.get("name") or user.get("userName")
            if name:
                approver_names.append(name)

    file_refs: List[str] = []
    for item in request.get("items", []):
        if item.get("type") == "FILE":
            files = item.get("values") or item.get("value") or []
            for file_obj in files:
                file_id = file_obj.get("id") or file_obj.get("fileId")
                file_name = file_obj.get("name") or file_obj.get("fileName")
                if file_id:
                    label = f"{file_id}:{file_name}" if file_name else file_id
                    file_refs.append(label)

    return {
        "requestId": request.get("id") or request.get("requestId"),
        "subject": request.get("subject"),
        "status": status.get("type"),
        "statusLabel": status.get("label"),
        "createdAt": request.get("createdAt"),
        "approvedAt": status.get("completedAt") or status.get("updatedAt"),
        "applicantName": applicant.get("name"),
        "applicantCode": applicant.get("code"),
        "approvers": "; ".join(approver_names),
        "fileRefs": "; ".join(file_refs),
    }


def write_result_json(result: SyncResult) -> None:
    """同期結果をJSONで保存"""

    if not result.output_path:
        return

    output = Path(result.output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "synced_at": result.synced_at,
        "record_count": result.record_count,
        "dry_run": result.dry_run,
        "sheet_updated": result.sheet_updated,
        "records": result.records,
    }

    with output.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def execute_sync(
    config: AppConfig,
    *,
    range_start: Optional[str],
    range_end: Optional[str],
    statuses: Optional[List[str]],
    limit: int,
    dry_run: bool,
    output_path: Optional[str],
) -> SyncResult:
    """Garoon→Sheets同期処理を実行"""

    garoon_client = GaroonClient(config.garoon)
    sheets_client = None
    if not dry_run:
        sheets_client = SheetsClient(config.sheets)

    records: List[Dict[str, Optional[str]]] = []
    for request in garoon_client.fetch_workflow_requests(
        limit=limit,
        range_start=range_start,
        range_end=range_end,
        statuses=statuses,
    ):
        normalized = normalize_request(request)
        records.append(normalized)

    sheet_updated = False
    if records and not dry_run and sheets_client:
        sheets_client.upsert_records(records, headers=DEFAULT_HEADERS)
        sheet_updated = True

    synced_at = datetime.now(timezone.utc).isoformat()
    result = SyncResult(
        synced_at=synced_at,
        record_count=len(records),
        dry_run=dry_run,
        sheet_updated=sheet_updated,
        records=records,
        output_path=output_path,
    )

    write_result_json(result)
    return result


def main() -> None:
    """エントリーポイント"""

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = parse_args()

    config = load_config(args.env)

    range_start = args.range_start or config.garoon.range_start
    range_end = args.range_end or config.garoon.range_end
    statuses = args.statuses or config.garoon.statuses
    output_path = args.output or None

    result = execute_sync(
        config,
        range_start=range_start,
        range_end=range_end,
        statuses=statuses,
        limit=args.limit,
        dry_run=args.dry_run,
        output_path=output_path,
    )

    logging.info("取得件数: %s", result.record_count)
    if result.sheet_updated:
        logging.info("Google Sheets を更新しました")
    elif result.record_count == 0:
        logging.info("条件に一致する申請はありませんでした")
    else:
        logging.info("ドライランのためシート更新をスキップしました")

    if result.output_path:
        logging.info("結果を %s に出力しました", result.output_path)


if __name__ == "__main__":
    main()
