"""팀 저장소 출력 포트 (헥사고날 드리븐 포트).

애플리케이션 계층은 이 인터페이스만 의존하고,
실제 구현은 adapter/output/persistence에 둡니다.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class TeamRepositoryPort(ABC):
    """팀 저장소 포트."""

    @abstractmethod
    async def find_by_id(self, team_id: int) -> Optional[Any]:
        """ID로 팀 조회."""
        ...

    @abstractmethod
    async def upsert_batch(self, teams_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """여러 팀 일괄 upsert."""
        ...

    @abstractmethod
    async def commit(self) -> None:
        """변경사항 커밋."""
        ...
