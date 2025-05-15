from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import WebSocket


class UserDTO(BaseModel):
    id: str
    username: str
    picture: str
    student_rating: int = Field(default=1000)
    teacher_rating: int = Field(default=1000)

class UserData(UserDTO):
    created_at: datetime

class UserInfo(UserData):
    user_activity: dict[datetime, int]
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
