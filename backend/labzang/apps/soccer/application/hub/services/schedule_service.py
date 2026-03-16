"""?? ??? ??????? ?? ?????"""
import logging
from typing import List, Dict, Any, Optional

from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output import ScheduleRepositoryPort
from labzang.apps.soccer.hub.repositories.schedule_repository import ScheduleRepository

logger = logging.getLogger(__name__)


class ScheduleService:
    """?? ??? ??????? ?? ????? ????? ?????

    JSONL ??????? schedules ????? ?????? ?? ?? ????????????
    """

    def __init__(self, schedule_repository: Optional[ScheduleRepositoryPort] = None):
        self._schedule_repository = schedule_repository
        logger.info("[ScheduleService] initialized (port=%s)", "injected" if schedule_repository else "default")

    def _normalize_schedule_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """?? ??? ??????? ?????????.

        Args:
            item: ??? ?? ??? ?????
        Returns:
            ?????? ?? ??? ?????        """
        normalized = {}

        # ??? ?? ?????????        if "id" in item:
            normalized["id"] = int(item["id"]) if item["id"] is not None else None

        if "stadium_id" in item:
            normalized["stadium_id"] = int(item["stadium_id"]) if item["stadium_id"] is not None else None

        if "hometeam_id" in item:
            normalized["hometeam_id"] = int(item["hometeam_id"]) if item["hometeam_id"] is not None else None

        if "awayteam_id" in item:
            normalized["awayteam_id"] = int(item["awayteam_id"]) if item["awayteam_id"] is not None else None

        if "stadium_code" in item:
            normalized["stadium_code"] = str(item["stadium_code"])[:10] if item["stadium_code"] else None

        if "sche_date" in item:
            normalized["sche_date"] = str(item["sche_date"])[:10] if item["sche_date"] else None

        if "gubun" in item:
            normalized["gubun"] = str(item["gubun"])[:10] if item["gubun"] else None

        if "hometeam_code" in item:
            normalized["hometeam_code"] = str(item["hometeam_code"])[:10] if item["hometeam_code"] else None

        if "awayteam_code" in item:
            normalized["awayteam_code"] = str(item["awayteam_code"])[:10] if item["awayteam_code"] else None

        if "home_score" in item:
            normalized["home_score"] = int(item["home_score"]) if item["home_score"] is not None else None

        if "away_score" in item:
            normalized["away_score"] = int(item["away_score"]) if item["away_score"] is not None else None

        return normalized

    async def _save_schedules_to_database(
        self,
        normalized_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """?????? ?? ??? ??????? Repository????? ???????????????????.

        Args:
            normalized_items: ?????? ?? ??? ?????????
        Returns:
            ?????? ??????
        """
        if self._schedule_repository:
            logger.info("[ScheduleService] Saving via injected repository...")
            db_result = await self._schedule_repository.upsert_batch(normalized_items)
            await self._schedule_repository.commit()
        else:
            async with AsyncSessionLocal() as session:
                repository = ScheduleRepository(session)
                logger.info("[ScheduleService] Saving via default repository...")
                db_result = await repository.upsert_batch(normalized_items)
                await repository.commit()
        logger.info(
            "[ScheduleService] DB done: inserted=%s updated=%s errors=%s",
            db_result.get("inserted_count", 0),
            db_result.get("updated_count", 0),
            db_result.get("error_count", 0),
        )
        return db_result

    async def process_schedules(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """?? ??? ??????? ?? ????? ????? ???????????????????

        Args:
            items: ?????? ??? ?????????
        Returns:
            ?? ?? ??????
        """
        logger.info(f"[????? ?? ?? ?? ???: {len(items)}??????")

        # 1. ??????????        logger.info("[????? ?????????????...")
        normalized_items = []
        for item in items:
            try:
                normalized = self._normalize_schedule_data(item)
                normalized_items.append(normalized)
            except Exception as e:
                logger.error(f"[????? ?????????????: {item.get('id', 'unknown')} - {e}", exc_info=True)

        logger.info(f"[????? ????????: {len(normalized_items)}??????")

        # 2. Repository????? ???????????????        logger.info("[????? Repository????? ????????? ???????...")
        db_result = await self._save_schedules_to_database(normalized_items)

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

