"""선수(Player) Pydantic 모델."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class PlayerModel(BaseModel):
    """선수 정보를 전송하기 위한 Pydantic 모델.

    SQLAlchemy Player 모델의 transfer 객체입니다.
    """

    id: Optional[int] = Field(None, description="선수 고유 식별자")
    team_id: Optional[int] = Field(None, description="팀 ID")
    player_name: Optional[str] = Field(None, description="선수명", max_length=20)
    e_player_name: Optional[str] = Field(None, description="영문 선수명", max_length=40)
    nickname: Optional[str] = Field(None, description="별명", max_length=30)
    join_yyyy: Optional[str] = Field(None, description="입단년도", max_length=10)
    position: Optional[str] = Field(None, description="포지션", max_length=10)
    back_no: Optional[int] = Field(None, description="등번호")
    nation: Optional[str] = Field(None, description="국적", max_length=20)
    birth_date: Optional[date] = Field(None, description="생년월일")
    solar: Optional[str] = Field(None, description="양력/음력 구분", max_length=10)
    height: Optional[int] = Field(None, description="키 (cm)")
    weight: Optional[int] = Field(None, description="몸무게 (kg)")

    class Config:
        """Pydantic 설정."""

        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat() if v else None
        }


class PlayerCreateModel(BaseModel):
    """선수 생성 요청 모델."""

    team_id: Optional[int] = Field(None, description="팀 ID")
    player_name: Optional[str] = Field(None, description="선수명", max_length=20)
    e_player_name: Optional[str] = Field(None, description="영문 선수명", max_length=40)
    nickname: Optional[str] = Field(None, description="별명", max_length=30)
    join_yyyy: Optional[str] = Field(None, description="입단년도", max_length=10)
    position: Optional[str] = Field(None, description="포지션", max_length=10)
    back_no: Optional[int] = Field(None, description="등번호")
    nation: Optional[str] = Field(None, description="국적", max_length=20)
    birth_date: Optional[date] = Field(None, description="생년월일")
    solar: Optional[str] = Field(None, description="양력/음력 구분", max_length=10)
    height: Optional[int] = Field(None, description="키 (cm)")
    weight: Optional[int] = Field(None, description="몸무게 (kg)")


class PlayerUpdateModel(BaseModel):
    """선수 수정 요청 모델."""

    team_id: Optional[int] = Field(None, description="팀 ID")
    player_name: Optional[str] = Field(None, description="선수명", max_length=20)
    e_player_name: Optional[str] = Field(None, description="영문 선수명", max_length=40)
    nickname: Optional[str] = Field(None, description="별명", max_length=30)
    join_yyyy: Optional[str] = Field(None, description="입단년도", max_length=10)
    position: Optional[str] = Field(None, description="포지션", max_length=10)
    back_no: Optional[int] = Field(None, description="등번호")
    nation: Optional[str] = Field(None, description="국적", max_length=20)
    birth_date: Optional[date] = Field(None, description="생년월일")
    solar: Optional[str] = Field(None, description="양력/음력 구분", max_length=10)
    height: Optional[int] = Field(None, description="키 (cm)")
    weight: Optional[int] = Field(None, description="몸무게 (kg)")

