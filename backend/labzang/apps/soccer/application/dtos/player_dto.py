"""선수 DTO (application/models/bases.players + player_embeddings 기반)."""
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional


@dataclass(frozen=False)
class PlayerDTO:
    """선수 데이터 전송 객체 (임베딩 컬럼 포함)."""

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
    # 임베딩( RAG ) 컬럼
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None  # 768-dim
    embedding_created_at: Optional[datetime] = None
