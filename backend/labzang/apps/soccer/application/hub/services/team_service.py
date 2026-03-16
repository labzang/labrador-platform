"""? ?? ?? ???. ????: TeamRepositoryPort ?? ??."""
import logging
from typing import List, Dict, Any, Optional

from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output.team_repository_port import (
    TeamRepositoryPort,
)
from labzang.apps.soccer.hub.repositories.team_repository import TeamRepository

logger = logging.getLogger(__name__)


class TeamService:
    """? ??? ?? ?? ??. ?? ?? ? ?????/????? ??? ?? ??."""

    def __init__(self, team_repository: Optional[TeamRepositoryPort] = None):
        """team_repository? None?? ???? session+TeamRepository ?? (?? ??)."""
        self._team_repository = team_repository
        logger.info("[???] TeamService ???")

    def _normalize_team_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """?? ??????? ?????????.

        Args:
            item: ??? ?? ?????
        Returns:
            ?????? ?? ?????        """
        normalized = {}

        # ??? ?? ?????????        if "id" in item:
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

    async def _save_teams_to_database(
        self,
        normalized_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """?????? ?? ??????? Repository????? ???????????????????.

        Args:
            normalized_items: ?????? ?? ?????????
        Returns:
            ?????? ??????
        """
        if self._team_repository is not None:
            db_result = await self._team_repository.upsert_batch(normalized_items)
            await self._team_repository.commit()
        else:
            async with AsyncSessionLocal() as session:
                repository = TeamRepository(session)
                logger.info("[???] Repository? ?? ?????? ?? ??...")
                db_result = await repository.upsert_batch(normalized_items)
                await repository.commit()
                logger.info(
                    f"[???] ?????? ?? ??: "
                    f"?? {db_result['inserted_count']}?, "
                    f"???? {db_result['updated_count']}?, "
                    f"?? {db_result['error_count']}?"
                )
        return db_result

    async def process_teams(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """?? ??????? ?? ????? ????? ???????????????????

        Args:
            items: ?????? ?????????
        Returns:
            ?? ?? ??????
        """
        logger.info(f"[????? ?? ?? ?? ???: {len(items)}??????")

        # 1. ??????????        logger.info("[????? ?????????????...")
        normalized_items = []
        for item in items:
            try:
                normalized = self._normalize_team_data(item)
                normalized_items.append(normalized)
            except Exception as e:
                logger.error(f"[????? ?????????????: {item.get('id', 'unknown')} - {e}", exc_info=True)

        logger.info(f"[????? ????????: {len(normalized_items)}??????")

        # 2. Repository????? ???????????????        logger.info("[????? Repository????? ????????? ???????...")
        db_result = await self._save_teams_to_database(normalized_items)

        result = {
            "success": True,
            "method": "rule_based",
            "total_items": len(items),
            "normalized_count": len(normalized_items),
            "database_result": db_result,
        }

        logger.info(
            f"[????? ?? ?? ?? ???: "
            f"??{len(items)}?? ??? {db_result['inserted_count']}?? "
            f"?????? {db_result['updated_count']}?? ??? {db_result['error_count']}??
        )
        return result

