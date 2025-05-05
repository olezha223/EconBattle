from pydantic import BaseModel
from fastapi import WebSocket


class UserDTO(BaseModel):
    id: int
    username: str
    student_rating: int
    teacher_rating: int
    # played_games: list[int]
    # created_competitions: list[int]


class Player:
    def __init__(self, user: UserDTO, websocket: WebSocket):
        self.user: UserDTO = user
        self.websocket: WebSocket = websocket
