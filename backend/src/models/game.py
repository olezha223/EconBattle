from datetime import datetime
from enum import Enum
from pydantic import BaseModel

from src.models.round import RoundDTO


class EventType(Enum):
    START_ROUND = "round_start"
    GAME_END = "game_end"
    ROUND_RESULT = "round_result"


class NewGame(BaseModel):
    """Схема создаваемой игры в процессе матча"""
    competition_id: int
    player_1: str
    player_2: str
    rounds: list[int]
    status_player_1: str
    status_player_2: str
    rating_difference_player_1: int
    rating_difference_player_2: int
    score_player_1: int
    score_player_2: int

class GameDTO(NewGame):
    """Схема игры + поле из бд"""
    created_at: datetime

class GameDTOExtended(GameDTO):
    """Статистика игр"""
    round_data: list[RoundDTO]
    competition_name: str
    creator_name: str
