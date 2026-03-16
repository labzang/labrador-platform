"""팀 도메인 엔티티.

헥사고날 도메인 계층: DB/인프라에 의존하지 않는 순수 엔티티.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=False)
class TeamEntity:
    """팀 도메인 엔티티."""

    id: int
    team_name: Optional[str] = None
    team_code: Optional[str] = None
    region_name: Optional[str] = None
    e_team_name: Optional[str] = None
    stadium_id: Optional[int] = None
    orig_yyyy: Optional[str] = None
    address: Optional[str] = None
    homepage: Optional[str] = None
    owner: Optional[str] = None

    def __post_init__(self) -> None:
        if self.id is None:
            raise ValueError("id is required")
