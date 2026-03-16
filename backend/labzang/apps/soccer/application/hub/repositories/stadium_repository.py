"""ê²½ê¸°???°ì´??Repository.

?°ì´?°ë² ?´ìŠ¤ ?‘ê·¼ ë¡œì§???´ë‹¹?©ë‹ˆ??
"""
import logging
from typing import List, Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from labzang.apps.soccer.application.ports.output.stadium_repository_port import (
    StadiumRepositoryPort,
)
from labzang.apps.soccer.models.bases.stadiums import Stadium

logger = logging.getLogger(__name__)


class StadiumRepository(StadiumRepositoryPort):
    """ê²½ê¸°???°ì´??Repository.

    Neon ?°ì´?°ë² ?´ìŠ¤??stadiums ?Œì´ë¸”ì— ?€??CRUD ?‘ì—…???˜í–‰?©ë‹ˆ??
    """

    def __init__(self, session: AsyncSession):
        """StadiumRepository ì´ˆê¸°??

        Args:
            session: ?°ì´?°ë² ?´ìŠ¤ ?¸ì…˜
        """
        self.session = session
        logger.debug("[Repository] StadiumRepository ì´ˆê¸°??)

    async def find_by_id(self, stadium_id: int) -> Optional[Stadium]:
        """IDë¡?ê²½ê¸°?¥ì„ ì¡°íšŒ?©ë‹ˆ??

        Args:
            stadium_id: ê²½ê¸°??ID

        Returns:
            Stadium ê°ì²´ ?ëŠ” None
        """
        result = await self.session.execute(
            select(Stadium).where(Stadium.id == stadium_id)
        )
        return result.scalar_one_or_none()

    async def create(self, stadium_data: Dict[str, Any]) -> Stadium:
        """??ê²½ê¸°?¥ì„ ?ì„±?©ë‹ˆ??

        Args:
            stadium_data: ê²½ê¸°???°ì´???•ì…”?ˆë¦¬

        Returns:
            ?ì„±??Stadium ê°ì²´

        Raises:
            IntegrityError: ì¤‘ë³µ ???ëŠ” ?œì•½ ì¡°ê±´ ?„ë°˜ ??        """
        new_stadium = Stadium(**stadium_data)
        self.session.add(new_stadium)
        logger.debug(f"[Repository] ê²½ê¸°???ì„±: ID {stadium_data.get('id')}")
        return new_stadium

    async def update(self, stadium: Stadium, stadium_data: Dict[str, Any]) -> Stadium:
        """ê¸°ì¡´ ê²½ê¸°?¥ì„ ?…ë°?´íŠ¸?©ë‹ˆ??

        Args:
            stadium: ?…ë°?´íŠ¸??Stadium ê°ì²´
            stadium_data: ?…ë°?´íŠ¸???°ì´???•ì…”?ˆë¦¬

        Returns:
            ?…ë°?´íŠ¸??Stadium ê°ì²´
        """
        for key, value in stadium_data.items():
            if key != "id":  # ID???…ë°?´íŠ¸?˜ì? ?ŠìŒ
                setattr(stadium, key, value)
        logger.debug(f"[Repository] ê²½ê¸°???…ë°?´íŠ¸: ID {stadium.id}")
        return stadium

    async def upsert_batch(
        self,
        stadiums_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """?¬ëŸ¬ ê²½ê¸°?¥ì„ ?¼ê´„ upsert (insert or update) ?©ë‹ˆ??

        Args:
            stadiums_data: ê²½ê¸°???°ì´??ë¦¬ìŠ¤??
        Returns:
            ì²˜ë¦¬ ê²°ê³¼ ?•ì…”?ˆë¦¬
            {
                "inserted_count": ?½ì…??ê°œìˆ˜,
                "updated_count": ?…ë°?´íŠ¸??ê°œìˆ˜,
                "error_count": ?¤ë¥˜ ê°œìˆ˜,
                "errors": ?¤ë¥˜ ?ì„¸ ?•ë³´ ë¦¬ìŠ¤??            }
        """
        inserted_count = 0
        updated_count = 0
        error_count = 0
        errors = []

        for stadium_data in stadiums_data:
            try:
                stadium_id = stadium_data.get("id")
                if not stadium_id:
                    error_msg = "IDê°€ ?†ìŠµ?ˆë‹¤"
                    logger.warning(f"[Repository] {error_msg}: {stadium_data}")
                    error_count += 1
                    errors.append({"item": stadium_data, "error": error_msg})
                    continue

                # ê¸°ì¡´ ê²½ê¸°???•ì¸
                existing_stadium = await self.find_by_id(stadium_id)

                if existing_stadium:
                    # ?…ë°?´íŠ¸
                    await self.update(existing_stadium, stadium_data)
                    updated_count += 1
                    logger.debug(f"[Repository] ê²½ê¸°???…ë°?´íŠ¸: ID {stadium_id}")
                else:
                    # ?ˆë¡œ ?½ì…
                    await self.create(stadium_data)
                    inserted_count += 1
                    logger.debug(f"[Repository] ê²½ê¸°???½ì…: ID {stadium_id}")

            except IntegrityError as e:
                error_count += 1
                error_msg = f"ë¬´ê²°???œì•½ ì¡°ê±´ ?„ë°˜: {str(e)}"
                logger.error(f"[Repository] {error_msg}: ID {stadium_data.get('id')}", exc_info=True)
                errors.append({"item": stadium_data, "error": error_msg})
            except Exception as e:
                error_count += 1
                error_msg = f"ì²˜ë¦¬ ì¤??¤ë¥˜: {str(e)}"
                logger.error(
                    f"[Repository] {error_msg}: ID {stadium_data.get('id')}",
                    exc_info=True
                )
                errors.append({"item": stadium_data, "error": error_msg})

        return {
            "inserted_count": inserted_count,
            "updated_count": updated_count,
            "error_count": error_count,
            "errors": errors,
        }

    async def commit(self):
        """ë³€ê²½ì‚¬??„ ì»¤ë°‹?©ë‹ˆ??

        Raises:
            Exception: ì»¤ë°‹ ?¤íŒ¨ ??        """
        try:
            await self.session.commit()
            logger.debug("[Repository] ì»¤ë°‹ ?„ë£Œ")
        except Exception as e:
            await self.session.rollback()
            logger.error(f"[Repository] ì»¤ë°‹ ?¤íŒ¨, ë¡¤ë°±: {e}", exc_info=True)
            raise

