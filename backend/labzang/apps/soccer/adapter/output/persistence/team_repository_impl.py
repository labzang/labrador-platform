# -*- coding: utf-8 -*-
"""Team repository output adapter (TeamRepositoryPort implementation).

Hexagonal: implements only the application output port;
creates session and delegates to hub.repositories.TeamRepository.
"""
import logging
from typing import Any, Dict, List, Optional

from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output.team_repository_port import (
    TeamRepositoryPort,
)
from labzang.apps.soccer.application.hub.repositories.team_repository import (
    TeamRepository,
)

logger = logging.getLogger(__name__)


class TeamRepositoryImpl(TeamRepositoryPort):
    """Team repository port implementation. Creates session and delegates to TeamRepository."""

    async def find_by_id(self, team_id: int) -> Optional[Any]:
        async with AsyncSessionLocal() as session:
            repo = TeamRepository(session)
            return await repo.find_by_id(team_id)

    async def find_all(self) -> List[Any]:
        async with AsyncSessionLocal() as session:
            repo = TeamRepository(session)
            return await repo.find_all()

    async def create(self, team_data: Dict[str, Any]) -> Any:
        async with AsyncSessionLocal() as session:
            repo = TeamRepository(session)
            entity = await repo.create(team_data)
            await repo.commit()
            return entity

    async def update(self, team: Any, team_data: Dict[str, Any]) -> Any:
        team_id = getattr(team, "id", None) or team_data.get("id")
        if team_id is None:
            raise ValueError("update: team or team_data must have 'id'")
        async with AsyncSessionLocal() as session:
            repo = TeamRepository(session)
            existing = await repo.find_by_id(team_id)
            if not existing:
                raise ValueError(f"Team not found: id={team_id}")
            updated = await repo.update(existing, team_data)
            await repo.commit()
            return updated

    async def delete(self, team_id: int) -> bool:
        async with AsyncSessionLocal() as session:
            repo = TeamRepository(session)
            ok = await repo.delete(team_id)
            if ok:
                await repo.commit()
            return ok

    async def upsert_batch(self, teams_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        async with AsyncSessionLocal() as session:
            repo = TeamRepository(session)
            result = await repo.upsert_batch(teams_data)
            await repo.commit()
            return result

    async def commit(self) -> None:
        """No-op: session is already committed in upsert_batch etc. Kept for port compatibility."""
        pass
