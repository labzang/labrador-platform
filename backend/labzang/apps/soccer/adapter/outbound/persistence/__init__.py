"""????? ??? ???."""
from labzang.apps.soccer.adapter.outbound.persistence.player_repository_adapter import (
    PlayerRepositoryAdapter,
)
from labzang.apps.soccer.adapter.outbound.persistence.schedule_repository_adapter import (
    ScheduleRepositoryAdapter,
)
from labzang.apps.soccer.adapter.outbound.persistence.stadium_repository_adapter import (
    StadiumRepositoryAdapter,
)
from labzang.apps.soccer.adapter.outbound.persistence.team_repository_adapter import (
    TeamRepositoryAdapter,
)

__all__ = [
    "PlayerRepositoryAdapter",
    "ScheduleRepositoryAdapter",
    "StadiumRepositoryAdapter",
    "TeamRepositoryAdapter",
]
