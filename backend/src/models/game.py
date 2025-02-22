from enum import Enum


class EventType(Enum):
    START_ROUND = "round_start"
    GAME_END = "game_end"
    ROUND_RESULT = "round_result"