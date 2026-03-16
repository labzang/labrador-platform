"""??????????? ?? ?????"""
import logging
from typing import List, Dict, Any, Optional

from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output import StadiumRepositoryPort
from labzang.apps.soccer.hub.repositories.stadium_repository import StadiumRepository

logger = logging.getLogger(__name__)


class StadiumService:
    """??????????? ?? ????? ????? ?????

    JSONL ??????? stadiums ????? ?????? ?? ?? ????????????
    """

    def __init__(self, stadium_repository: Optional[StadiumRepositoryPort] = None):
        self._stadium_repository = stadium_repository
        logger.info("[StadiumService] initialized (port=%s)", "injected" if stadium_repository else "default")

    def _normalize_stadium_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """??????????? ?????????.

        Args:
            item: ??? ?????????
        Returns:
            ?????? ?????????        """
        normalized = {}

        # ??? ?? ?????????        if "id" in item:
            normalized["id"] = int(item["id"]) if item["id"] is not None else None

        if "stadium_code" in item:
            normalized["stadium_code"] = str(item["stadium_code"])[:10] if item["stadium_code"] else None

        # statdium_name (????) ??? stadium_name ???        if "stadium_name" in item:
            normalized["stadium_name"] = str(item["stadium_name"])[:40] if item["stadium_name"] else None
        elif "statdium_name" in item:
            # ??? ?????? ??? ??????????? ???            normalized["stadium_name"] = str(item["statdium_name"])[:40] if item["statdium_name"] else None

        if "hometeam_code" in item:
            normalized["hometeam_code"] = str(item["hometeam_code"])[:10] if item["hometeam_code"] else None

        if "seat_count" in item:
            normalized["seat_count"] = int(item["seat_count"]) if item["seat_count"] is not None else None

        if "address" in item:
            normalized["address"] = str(item["address"])[:60] if item["address"] else None

        if "ddd" in item:
            normalized["ddd"] = str(item["ddd"])[:10] if item["ddd"] else None

        if "tel" in item:
            normalized["tel"] = str(item["tel"])[:20] if item["tel"] else None

        return normalized

    async def _save_stadiums_to_database(
        self,
        normalized_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """?????? ??????????? Repository????? ???????????????????.

        Args:
            normalized_items: ?????? ?????????????
        Returns:
            ?????? ??????
        """
        if self._stadium_repository:
            logger.info("[StadiumService] Saving via injected repository...")
            db_result = await self._stadium_repository.upsert_batch(normalized_items)
            await self._stadium_repository.commit()
        else:
            async with AsyncSessionLocal() as session:
                repository = StadiumRepository(session)
                logger.info("[StadiumService] Saving via default repository...")
                db_result = await repository.upsert_batch(normalized_items)
                await repository.commit()
        logger.info(
            "[StadiumService] DB done: inserted=%s updated=%s errors=%s",
            db_result.get("inserted_count", 0),
            db_result.get("updated_count", 0),
            db_result.get("error_count", 0),
        )
        return db_result

    async def process_stadiums(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """??????????? ?? ????? ????? ???????????????????

        Args:
            items: ?????????????????
        Returns:
            ?? ?? ??????
        """
        logger.info(f"[????? ?? ?? ?? ???: {len(items)}??????")

        # 1. ??????????        logger.info("[????? ?????????????...")
        normalized_items = []
        for item in items:
            try:
                normalized = self._normalize_stadium_data(item)
                normalized_items.append(normalized)
            except Exception as e:
                logger.error(f"[????? ?????????????: {item.get('id', 'unknown')} - {e}", exc_info=True)

        logger.info(f"[????? ????????: {len(normalized_items)}??????")

        # 2. Repository????? ???????????????        logger.info("[????? Repository????? ????????? ???????...")
        db_result = await self._save_stadiums_to_database(normalized_items)

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

