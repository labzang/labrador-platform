"""팀 DTO (application/models/bases.teams + team_embeddings 기반)."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=False)
class TeamDTO:
    """팀 데이터 전송 객체 (임베딩 컬럼 포함)."""

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
    # 임베딩( RAG ) 컬럼
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None  # 768-dim
    embedding_created_at: Optional[datetime] = None
