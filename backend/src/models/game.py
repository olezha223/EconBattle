from enum import Enum
from pydantic import BaseModel

class EventType(Enum):
    START_ROUND = "round_start"
    GAME_END = "game_end"
    ROUND_RESULT = "round_result"


class GameDTO(BaseModel):
    competition_id: int
    player_1: str
    player_2: str
    rounds: list[int]
    status_player_1: str
    status_player_2: str
    rating_difference_player_1: int
    rating_difference_player_2: int