"""?€ ?°ì´??Repository.

?°ì´?°ë² ?´ìŠ¤ ?‘ê·¼ ë¡œì§???´ë‹¹?©ë‹ˆ??
"""
import logging
from typing import List, Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from labzang.apps.soccer.application.ports.output.team_repository_port import (
    TeamRepositoryPort,
)
from labzang.apps.soccer.models.bases.teams import Team

logger = logging.getLogger(__name__)


class TeamRepository(TeamRepositoryPort):
    """?€ ?°ì´??Repository.

    Neon ?°ì´?°ë² ?´ìŠ¤??teams ?Œì´ë¸”ì— ?€??CRUD ?‘ì—…???˜í–‰?©ë‹ˆ??
    """

    def __init__(self, session: AsyncSession):
        """TeamRepository ì´ˆê¸°??

        Args:
            session: ?°ì´?°ë² ?´ìŠ¤ ?¸ì…˜
        """
        self.session = session
        logger.debug("[Repository] TeamRepository ì´ˆê¸°??)

    async def find_by_id(self, team_id: int) -> Optional[Team]:
        """IDë¡??€??ì¡°íšŒ?©ë‹ˆ??

        Args:
            team_id: ?€ ID

        Returns:
            Team ê°ì²´ ?ëŠ” None
        """
        result = await self.session.execute(
            select(Team).where(Team.id == team_id)
        )
        return result.scalar_one_or_none()

    async def create(self, team_data: Dict[str, Any]) -> Team:
        """???€???ì„±?©ë‹ˆ??

        Args:
            team_data: ?€ ?°ì´???•ì…”?ˆë¦¬

        Returns:
            ?ì„±??Team ê°ì²´

        Raises:
            IntegrityError: ì¤‘ë³µ ???ëŠ” ?œì•½ ì¡°ê±´ ?„ë°˜ ??        """
        new_team = Team(**team_data)
        self.session.add(new_team)
        logger.debug(f"[Repository] ?€ ?ì„±: ID {team_data.get('id')}")
        return new_team

    async def update(self, team: Team, team_data: Dict[str, Any]) -> Team:
        """ê¸°ì¡´ ?€???…ë°?´íŠ¸?©ë‹ˆ??

        Args:
            team: ?…ë°?´íŠ¸??Team ê°ì²´
            team_data: ?…ë°?´íŠ¸???°ì´???•ì…”?ˆë¦¬

        Returns:
            ?…ë°?´íŠ¸??Team ê°ì²´
        """
        for key, value in team_data.items():
            if key != "id":  # ID???…ë°?´íŠ¸?˜ì? ?ŠìŒ
                setattr(team, key, value)
        logger.debug(f"[Repository] ?€ ?…ë°?´íŠ¸: ID {team.id}")
        return team

    async def upsert_batch(
        self,
        teams_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """?¬ëŸ¬ ?€???¼ê´„ upsert (insert or update) ?©ë‹ˆ??

        Args:
            teams_data: ?€ ?°ì´??ë¦¬ìŠ¤??
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

        for team_data in teams_data:
            try:
                team_id = team_data.get("id")
                if not team_id:
                    error_msg = "IDê°€ ?†ìŠµ?ˆë‹¤"
                    logger.warning(f"[Repository] {error_msg}: {team_data}")
                    error_count += 1
                    errors.append({"item": team_data, "error": error_msg})
                    continue

                # ê¸°ì¡´ ?€ ?•ì¸
                existing_team = await self.find_by_id(team_id)

                if existing_team:
                    # ?…ë°?´íŠ¸
                    await self.update(existing_team, team_data)
                    updated_count += 1
                    logger.debug(f"[Repository] ?€ ?…ë°?´íŠ¸: ID {team_id}")
                else:
                    # ?ˆë¡œ ?½ì…
                    await self.create(team_data)
                    inserted_count += 1
                    logger.debug(f"[Repository] ?€ ?½ì…: ID {team_id}")

            except IntegrityError as e:
                error_count += 1
                error_msg = f"ë¬´ê²°???œì•½ ì¡°ê±´ ?„ë°˜: {str(e)}"
                logger.error(f"[Repository] {error_msg}: ID {team_data.get('id')}", exc_info=True)
                errors.append({"item": team_data, "error": error_msg})
            except Exception as e:
                error_count += 1
                error_msg = f"ì²˜ë¦¬ ì¤??¤ë¥˜: {str(e)}"
                logger.error(
                    f"[Repository] {error_msg}: ID {team_data.get('id')}",
                    exc_info=True
                )
                errors.append({"item": team_data, "error": error_msg})

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

