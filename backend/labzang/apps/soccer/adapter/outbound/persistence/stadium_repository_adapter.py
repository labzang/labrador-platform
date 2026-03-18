# -*- coding: utf-8 -*-
"""경기장 저장소 출력 어댑터 (StadiumRepositoryPort 구현).

헥사고날: application 계층의 출력 포트만 구현하며,
세션 생성 후 hub.repositories.StadiumRepository에 위임합니다.
"""
import logging
from typing import Any, Dict, List, Optional

from labzang.core.database import AsyncSessionLocal
from labzang.apps.soccer.application.ports.output.stadium_repository_port import (
    StadiumRepositoryPort,
)
from labzang.apps.soccer.application.hub.repositories.stadium_repository import (
    StadiumRepository,
)

logger = logging.getLogger(__name__)


class StadiumRepositoryAdapter(StadiumRepositoryPort):
    """경기장 저장소 포트 어댑터. 세션 생성 후 기존 StadiumRepository에 위임."""

    async def find_by_id(self, stadium_id: int) -> Optional[Any]:
        async with AsyncSessionLocal() as session:
            repo = StadiumRepository(session)
            return await repo.find_by_id(stadium_id)

    async def upsert_batch(self, stadiums_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        async with AsyncSessionLocal() as session:
            repo = StadiumRepository(session)
            result = await repo.upsert_batch(stadiums_data)
            await repo.commit()
            return result

    async def commit(self) -> None:
        """세션은 upsert_batch 등에서 이미 커밋하므로 별도 커밋은 불필요. 호환용."""
        pass
