"""일정 DTO (application/models/bases.schedules + schedule_embeddings 기반)."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=False)
class ScheduleDTO:
    """일정 데이터 전송 객체 (임베딩 컬럼 포함)."""

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
    # 임베딩( RAG ) 컬럼
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None  # 768-dim
    embedding_created_at: Optional[datetime] = None
