"""DTO (Data Transfer Object) - application/models/bases 필드 기반 (임베딩 컬럼 포함)."""
from labzang.apps.soccer.application.dtos.player_dto import PlayerDTO
from labzang.apps.soccer.application.dtos.schedule_dto import ScheduleDTO
from labzang.apps.soccer.application.dtos.stadium_dto import StadiumDTO
from labzang.apps.soccer.application.dtos.team_dto import TeamDTO

__all__ = [
    "PlayerDTO",
    "ScheduleDTO",
    "StadiumDTO",
    "TeamDTO",
]
