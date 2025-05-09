from datetime import datetime
from pydantic import BaseModel


class NewCompetition(BaseModel):
    name: str
    creator_id: str
    # settings
    max_players: int
    max_rounds: int
    round_time_in_seconds: int
    tasks_markup: dict[int, list[int]]

class CompetitionDTO(NewCompetition):
    id: int
    created_at: datetime

class CompetitionPreview(BaseModel):
    id: int
    name: str
    games_played: int
    unique_players: int
    created_at: datetime
