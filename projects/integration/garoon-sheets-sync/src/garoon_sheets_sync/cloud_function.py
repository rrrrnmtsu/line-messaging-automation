import json
import logging
from typing import Any, Dict, List, Optional

from .config import load_config
from .sync import execute_sync


def _parse_statuses(value: Any, fallback: Optional[List[str]]) -> Optional[List[str]]:
    """リクエストパラメーターからステータス配列を構築"""

    if value is None:
        return fallback
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return fallback


def garoon_sync(request):
    """Google Cloud Functions / Cloud Run 用エントリーポイント"""

    logging.basicConfig(level=logging.INFO)

    try:
        payload: Dict[str, Any] = request.get_json(silent=True) or {}
    except Exception:  # noqa: BLE001
        payload = {}

    env_path = payload.get("env", ".env")
    config = load_config(env_path)

    range_start = payload.get("rangeStart") or config.garoon.range_start
    range_end = payload.get("rangeEnd") or config.garoon.range_end
    statuses = _parse_statuses(payload.get("statuses"), config.garoon.statuses)
    limit = int(payload.get("limit", 500))
    dry_run = bool(payload.get("dryRun", False))
    output_path = payload.get("outputPath")

    result = execute_sync(
        config,
        range_start=range_start,
        range_end=range_end,
        statuses=statuses,
        limit=limit,
        dry_run=dry_run,
        output_path=output_path,
    )

    response_body = {
        "syncedAt": result.synced_at,
        "recordCount": result.record_count,
        "dryRun": result.dry_run,
        "sheetUpdated": result.sheet_updated,
        "records": result.records,
    }

    return (
        json.dumps(response_body, ensure_ascii=False),
        200,
        {"Content-Type": "application/json; charset=utf-8"},
    )
