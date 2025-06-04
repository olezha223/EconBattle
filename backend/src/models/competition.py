from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Round(BaseModel):
    tasks: list[int] = Field(..., max_length=50)
    time_limit: int = Field(60, gt=0, lt=3000)

class NewCompetition(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    creator_id: str = Field(...)
    # settings
    max_rounds: int = Field(..., gt=0, le=30)
    tasks_markup: dict[str, Round] = Field(..., examples=[
        {
            "1": {
                "tasks": [
                    18,
                    19,
                    20
                ],
                "time_limit": 60
            }
        },
    ])

class CompetitionDTO(NewCompetition):
    id: int
    created_at: datetime

class CompetitionDetailedDTO(CompetitionDTO):
    creator_name: str
    picture: str
    max_time: int
    mean_task_difficulty: float
    percent_of_correct: float

class CompetitionPreview(BaseModel):
    id: int
    name: str
    games_played: int
    unique_players: int
    created_at: datetime
    creator_id: str
    creator_name: str
    picture: str
    mean_task_difficulty: float
