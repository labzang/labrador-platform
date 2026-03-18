"""팀 도메인 엔티티.

헥사고날 도메인 계층: DB/인프라에 의존하지 않는 순수 엔티티.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=False)
class TeamEntity:
    """팀 도메인 엔티티."""

    id: int
    stadium_id: Optional[int] = None
    team_code: Optional[str] = None
    region_name: Optional[str] = None
    team_name: Optional[str] = None
    e_team_name: Optional[str] = None
    orig_yyyy: Optional[str] = None
    zip_code1: Optional[str] = None
    zip_code2: Optional[str] = None
    address: Optional[str] = None
    ddd: Optional[str] = None
    tel: Optional[str] = None
    fax: Optional[str] = None
    homepage: Optional[str] = None
    owner: Optional[str] = None
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None  # 768-dim
    embedding_created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.id is None:
            raise ValueError("id is required")
