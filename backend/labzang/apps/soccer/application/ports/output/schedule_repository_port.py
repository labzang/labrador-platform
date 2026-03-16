"""일정 저장소 출력 포트 (헥사고날 드리븐 포트)."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ScheduleRepositoryPort(ABC):
    """일정 저장소 포트."""

    @abstractmethod
    async def find_by_id(self, schedule_id: int) -> Optional[Any]:
        """ID로 일정 조회."""
        ...

    @abstractmethod
    async def upsert_batch(self, schedules_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """여러 일정 일괄 upsert."""
        ...

    @abstractmethod
    async def commit(self) -> None:
        """변경사항 커밋."""
        ...
