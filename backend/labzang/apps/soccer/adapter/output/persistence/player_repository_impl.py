# -*- coding: utf-8 -*-
"""Player repository output adapter (PlayerRepositoryPort implementation).

Hexagonal: implements only the application output port;
creates session and delegates to hub.repositories.PlayerRepository.
"""
import logging
from typing import Any, Dict, List, Optional

from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output.player_repository_port import (
    PlayerRepositoryPort,
)
from labzang.apps.soccer.application.hub.repositories.player_repository import (
    PlayerRepository,
)

logger = logging.getLogger(__name__)


class PlayerRepositoryImpl(PlayerRepositoryPort):
    """Player repository port implementation. Creates session and delegates to PlayerRepository."""

    async def find_by_id(self, player_id: int) -> Optional[Any]:
        async with AsyncSessionLocal() as session:
            repo = PlayerRepository(session)
            return await repo.find_by_id(player_id)

    async def upsert_batch(self, players_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        async with AsyncSessionLocal() as session:
            repo = PlayerRepository(session)
            result = await repo.upsert_batch(players_data)
            await repo.commit()
            return result

    async def commit(self) -> None:
        """No-op: session is already committed in upsert_batch etc. Kept for port compatibility."""
        pass
