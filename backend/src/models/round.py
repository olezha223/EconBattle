from pydantic import BaseModel
from enum import Enum

class StatusEnum(str, Enum):
    WINNER = "winner"
    LOSER = "loser"
    TIE = "tie"

class RoundDTO(BaseModel):
    points_player_1: int
    points_player_2: int
    status_player_1: str
    status_player_2: str
