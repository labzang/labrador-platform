"""선수 도메인 엔티티.

헥사고날 도메인 계층: DB/인프라에 의존하지 않는 순수 엔티티.
"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional


@dataclass(frozen=False)
class PlayerEntity:
    """선수 도메인 엔티티."""

    id: int
    team_id: Optional[int] = None
    player_name: Optional[str] = None
    e_player_name: Optional[str] = None
    nickname: Optional[str] = None
    join_yyyy: Optional[str] = None
    position: Optional[str] = None
    back_no: Optional[int] = None
    nation: Optional[str] = None
    birth_date: Optional[date] = None
    solar: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None  # 768-dim
    embedding_created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.id is None:
            raise ValueError("id is required")
