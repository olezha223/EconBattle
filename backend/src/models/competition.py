from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Round(BaseModel):
    tasks: list[int] = []
    time_limit: int = 60

class NewCompetition(BaseModel):
    name: str
    creator_id: str
    # settings
    max_rounds: int
    tasks_markup: dict[str, Round]

class CompetitionDTO(NewCompetition):
    id: int
    created_at: datetime

class CompetitionDetailedDTO(CompetitionDTO):
    creator_name: str
    picture: str
    max_time: int

class CompetitionPreview(BaseModel):
    id: int
    name: str
    games_played: int
    unique_players: int
    created_at: datetime
    creator_id: str
    creator_name: str
    picture: str
