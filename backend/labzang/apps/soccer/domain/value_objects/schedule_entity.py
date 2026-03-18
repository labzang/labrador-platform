"""일정 도메인 엔티티.

헥사고날 도메인 계층: DB/인프라에 의존하지 않는 순수 엔티티.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=False)
class ScheduleEntity:
    """일정 도메인 엔티티."""

    id: int
    stadium_id: Optional[int] = None
    hometeam_id: Optional[int] = None
    awayteam_id: Optional[int] = None
    stadium_code: Optional[str] = None
    sche_date: Optional[str] = None
    gubun: Optional[str] = None
    hometeam_code: Optional[str] = None
    awayteam_code: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None  # 768-dim
    embedding_created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.id is None:
            raise ValueError("id is required")
