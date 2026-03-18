"""경기장 DTO (application/models/bases.stadiums + stadium_embeddings 기반)."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=False)
class StadiumDTO:
    """경기장 데이터 전송 객체 (임베딩 컬럼 포함)."""

    id: int
    stadium_code: Optional[str] = None
    stadium_name: Optional[str] = None
    hometeam_code: Optional[str] = None
    seat_count: Optional[int] = None
    address: Optional[str] = None
    ddd: Optional[str] = None
    tel: Optional[str] = None
    # 임베딩( RAG ) 컬럼
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None  # 768-dim
    embedding_created_at: Optional[datetime] = None
