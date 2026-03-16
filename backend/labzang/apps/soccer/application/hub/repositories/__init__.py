"""Soccer ?�메??Repository 모듈."""

from labzang.apps.soccer.hub.repositories.player_repository import PlayerRepository
from labzang.apps.soccer.hub.repositories.schedule_repository import ScheduleRepository
from labzang.apps.soccer.hub.repositories.stadium_repository import StadiumRepository
from labzang.apps.soccer.hub.repositories.team_repository import TeamRepository

__all__ = [
    "PlayerRepository",
    "ScheduleRepository",
    "StadiumRepository",
    "TeamRepository",
]
