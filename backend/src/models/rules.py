from typing import Any

from pydantic import BaseModel


class RulesDTO(BaseModel):
    max_players: int
    max_rounds: int
    round_time_in_seconds: int
    tasks_markup: dict[str, Any]