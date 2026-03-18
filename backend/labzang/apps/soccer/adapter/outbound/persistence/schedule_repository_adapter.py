# -*- coding: utf-8 -*-
"""Schedule repository output adapter (ScheduleRepositoryPort implementation).

Hexagonal: implements only the application output port;
creates session and delegates to hub.repositories.ScheduleRepository.
"""
import logging
from typing import Any, Dict, List, Optional

from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output.schedule_repository_port import (
    ScheduleRepositoryPort,
)
from labzang.apps.soccer.application.hub.repositories.schedule_repository import (
    ScheduleRepository,
)

logger = logging.getLogger(__name__)


class ScheduleRepositoryAdapter(ScheduleRepositoryPort):
    """Schedule repository port adapter. Creates session and delegates to ScheduleRepository."""

    async def find_by_id(self, schedule_id: int) -> Optional[Any]:
        async with AsyncSessionLocal() as session:
            repo = ScheduleRepository(session)
            return await repo.find_by_id(schedule_id)

    async def upsert_batch(self, schedules_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        async with AsyncSessionLocal() as session:
            repo = ScheduleRepository(session)
            result = await repo.upsert_batch(schedules_data)
            await repo.commit()
            return result

    async def commit(self) -> None:
        """No-op: session is already committed in upsert_batch etc. Kept for port compatibility."""
        pass
