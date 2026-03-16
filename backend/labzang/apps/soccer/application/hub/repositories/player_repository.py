"""? ìˆ˜ ?°ì´??Repository.

?°ì´?°ë² ?´ìŠ¤ ?‘ê·¼ ë¡œì§???´ë‹¹?©ë‹ˆ??
"""
import logging
from typing import List, Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from labzang.apps.soccer.application.ports.output.player_repository_port import (
    PlayerRepositoryPort,
)
from labzang.apps.soccer.models.bases.players import Player

logger = logging.getLogger(__name__)


class PlayerRepository(PlayerRepositoryPort):
    """? ìˆ˜ ?°ì´??Repository.

    Neon ?°ì´?°ë² ?´ìŠ¤??players ?Œì´ë¸”ì— ?€??CRUD ?‘ì—…???˜í–‰?©ë‹ˆ??
    """

    def __init__(self, session: AsyncSession):
        """PlayerRepository ì´ˆê¸°??

        Args:
            session: ?°ì´?°ë² ?´ìŠ¤ ?¸ì…˜
        """
        self.session = session
        logger.debug("[Repository] PlayerRepository ì´ˆê¸°??)

    async def find_by_id(self, player_id: int) -> Optional[Player]:
        """IDë¡?? ìˆ˜ë¥?ì¡°íšŒ?©ë‹ˆ??

        Args:
            player_id: ? ìˆ˜ ID

        Returns:
            Player ê°ì²´ ?ëŠ” None
        """
        result = await self.session.execute(
            select(Player).where(Player.id == player_id)
        )
        return result.scalar_one_or_none()

    async def create(self, player_data: Dict[str, Any]) -> Player:
        """??? ìˆ˜ë¥??ì„±?©ë‹ˆ??

        Args:
            player_data: ? ìˆ˜ ?°ì´???•ì…”?ˆë¦¬

        Returns:
            ?ì„±??Player ê°ì²´

        Raises:
            IntegrityError: ì¤‘ë³µ ???ëŠ” ?œì•½ ì¡°ê±´ ?„ë°˜ ??        """
        new_player = Player(**player_data)
        self.session.add(new_player)
        logger.debug(f"[Repository] ? ìˆ˜ ?ì„±: ID {player_data.get('id')}")
        return new_player

    async def update(self, player: Player, player_data: Dict[str, Any]) -> Player:
        """ê¸°ì¡´ ? ìˆ˜ë¥??…ë°?´íŠ¸?©ë‹ˆ??

        Args:
            player: ?…ë°?´íŠ¸??Player ê°ì²´
            player_data: ?…ë°?´íŠ¸???°ì´???•ì…”?ˆë¦¬

        Returns:
            ?…ë°?´íŠ¸??Player ê°ì²´
        """
        for key, value in player_data.items():
            if key != "id":  # ID???…ë°?´íŠ¸?˜ì? ?ŠìŒ
                setattr(player, key, value)
        logger.debug(f"[Repository] ? ìˆ˜ ?…ë°?´íŠ¸: ID {player.id}")
        return player

    async def upsert_batch(
        self,
        players_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """?¬ëŸ¬ ? ìˆ˜ë¥??¼ê´„ upsert (insert or update) ?©ë‹ˆ??

        Args:
            players_data: ? ìˆ˜ ?°ì´??ë¦¬ìŠ¤??
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

        for player_data in players_data:
            try:
                player_id = player_data.get("id")
                if not player_id:
                    error_msg = "IDê°€ ?†ìŠµ?ˆë‹¤"
                    logger.warning(f"[Repository] {error_msg}: {player_data}")
                    error_count += 1
                    errors.append({"item": player_data, "error": error_msg})
                    continue

                # ê¸°ì¡´ ? ìˆ˜ ?•ì¸
                existing_player = await self.find_by_id(player_id)

                if existing_player:
                    # ?…ë°?´íŠ¸
                    await self.update(existing_player, player_data)
                    updated_count += 1
                    logger.debug(f"[Repository] ? ìˆ˜ ?…ë°?´íŠ¸: ID {player_id}")
                else:
                    # ?ˆë¡œ ?½ì…
                    await self.create(player_data)
                    inserted_count += 1
                    logger.debug(f"[Repository] ? ìˆ˜ ?½ì…: ID {player_id}")

            except IntegrityError as e:
                error_count += 1
                error_msg = f"ë¬´ê²°???œì•½ ì¡°ê±´ ?„ë°˜: {str(e)}"
                logger.error(f"[Repository] {error_msg}: ID {player_data.get('id')}", exc_info=True)
                errors.append({"item": player_data, "error": error_msg})
            except Exception as e:
                error_count += 1
                error_msg = f"ì²˜ë¦¬ ì¤??¤ë¥˜: {str(e)}"
                logger.error(
                    f"[Repository] {error_msg}: ID {player_data.get('id')}",
                    exc_info=True
                )
                errors.append({"item": player_data, "error": error_msg})

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

