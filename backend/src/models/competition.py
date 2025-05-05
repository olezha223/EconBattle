from pydantic import BaseModel


class CompetitionDTO(BaseModel):
    name: str
    creator_id: int
    # settings
    max_players: int
    max_rounds: int
    round_time_in_seconds: int
    tasks_markup: dict[str, list[int]]
