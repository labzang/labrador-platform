"""경기장 도메인 엔티티.

헥사고날 도메인 계층: DB/인프라에 의존하지 않는 순수 엔티티.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=False)
class StadiumEntity:
    """경기장 도메인 엔티티."""

    id: int
    stadium_code: Optional[str] = None
    stadium_name: Optional[str] = None
    hometeam_code: Optional[str] = None
    seat_count: Optional[int] = None
    address: Optional[str] = None
    ddd: Optional[str] = None
    tel: Optional[str] = None
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None  # 768-dim
    embedding_created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.id is None:
            raise ValueError("id is required")
