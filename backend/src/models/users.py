from pydantic import BaseModel, Field
from fastapi import WebSocket


class UserDTO(BaseModel):
    id: int
    username: str
    student_rating: int = Field(default=1000)
    teacher_rating: int = Field(default=1000)

class UserExtended(UserDTO):
    played_games: list[int]
    created_competitions: list[int]
    created_tasks: list[int]


class UserStatistics(BaseModel):
    # статистика как игрока
    wins_count: int
    losses_count: int
    tie_count: int

    # статистика как составителя задач
    tasks_created: int
    mean_task_difficulty: float

    # статистика как организатора соревнований
    competitions_created: int
    games_played: int


class Player:
    def __init__(self, user: UserDTO, websocket: WebSocket):
        self.user: UserDTO = user
        self.websocket: WebSocket = websocket
