from pydantic import BaseModel


class Competition(BaseModel):
    played_games: list[int]
    name: str
    rules: int
    tasks: list[int]
    creator: int