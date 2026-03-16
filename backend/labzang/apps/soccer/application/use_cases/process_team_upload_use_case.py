"""?€ ?…ë¡œ??? ìŠ¤ì¼€?´ìŠ¤ (?…ë ¥ ?¬íŠ¸ êµ¬í˜„).

ì¶œë ¥ ?¬íŠ¸(TeamRepositoryPort)?ë§Œ ?˜ì¡´?˜ë©°, ?•ê·œ?????€?¥ì„ ?„ì„?©ë‹ˆ??
"""
import logging
from typing import Any, Dict, List

from labzang.apps.soccer.application.ports.input.process_team_upload_port import (
    ProcessTeamUploadInputPort,
)
from labzang.apps.soccer.application.ports.output.team_repository_port import (
    TeamRepositoryPort,
)

logger = logging.getLogger(__name__)


def _normalize_team_data(item: Dict[str, Any]) -> Dict[str, Any]:
    """?€ ?°ì´???•ê·œ??(?„ë©”??ê·œì¹™)."""
    normalized: Dict[str, Any] = {}
    if "id" in item:
        normalized["id"] = int(item["id"]) if item["id"] is not None else None
    if "stadium_id" in item:
        normalized["stadium_id"] = int(item["stadium_id"]) if item["stadium_id"] is not None else None
    if "team_code" in item:
        normalized["team_code"] = str(item["team_code"])[:10] if item["team_code"] else None
    if "region_name" in item:
        normalized["region_name"] = str(item["region_name"])[:10] if item["region_name"] else None
    if "team_name" in item:
        normalized["team_name"] = str(item["team_name"])[:40] if item["team_name"] else None
    if "e_team_name" in item:
        normalized["e_team_name"] = str(item["e_team_name"])[:50] if item["e_team_name"] else None
    if "orig_yyyy" in item:
        normalized["orig_yyyy"] = str(item["orig_yyyy"])[:10] if item["orig_yyyy"] else None
    if "zip_code1" in item:
        normalized["zip_code1"] = str(item["zip_code1"])[:10] if item["zip_code1"] else None
    if "zip_code2" in item:
        normalized["zip_code2"] = str(item["zip_code2"])[:10] if item["zip_code2"] else None
    if "address" in item:
        normalized["address"] = str(item["address"])[:80] if item["address"] else None
    if "ddd" in item:
        normalized["ddd"] = str(item["ddd"])[:10] if item["ddd"] else None
    if "tel" in item:
        normalized["tel"] = str(item["tel"])[:20] if item["tel"] else None
    if "fax" in item:
        normalized["fax"] = str(item["fax"])[:20] if item["fax"] else None
    if "homepage" in item:
        normalized["homepage"] = str(item["homepage"])[:100] if item["homepage"] else None
    if "owner" in item:
        normalized["owner"] = str(item["owner"])[:50] if item["owner"] else None
    return normalized


class ProcessTeamUploadUseCase(ProcessTeamUploadInputPort):
    """?€ ?…ë¡œ??? ìŠ¤ì¼€?´ìŠ¤. ì¶œë ¥ ?¬íŠ¸(?€?¥ì†Œ)?ë§Œ ?˜ì¡´."""

    def __init__(self, team_repository: TeamRepositoryPort) -> None:
        self._team_repository = team_repository

    async def execute(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """?€ JSONL ??ª©???•ê·œ?????€?¥ì†Œ???€??"""
        logger.info("[? ìŠ¤ì¼€?´ìŠ¤] ?€ ?…ë¡œ??ì²˜ë¦¬ ?œì‘: %sê°???ª©", len(items))
        normalized_items: List[Dict[str, Any]] = []
        for item in items:
            try:
                normalized_items.append(_normalize_team_data(item))
            except Exception as e:
                logger.error("?•ê·œ???¤íŒ¨ id=%s: %s", item.get("id"), e, exc_info=True)
        db_result = await self._team_repository.upsert_batch(normalized_items)
        await self._team_repository.commit()
        result = {
            "success": True,
            "method": "hexagonal_use_case",
            "total_items": len(items),
            "normalized_count": len(normalized_items),
            "database_result": db_result,
        }
        logger.info("[? ìŠ¤ì¼€?´ìŠ¤] ?€ ?…ë¡œ???„ë£Œ: ?½ì…=%s, ?…ë°?´íŠ¸=%s", db_result.get("inserted_count"), db_result.get("updated_count"))
        return result
