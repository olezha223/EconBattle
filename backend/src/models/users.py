from pydantic import BaseModel
from fastapi import WebSocket


class UserDTO(BaseModel):
    id: int
    username: str
    rating: int


class Player:
    def __init__(self, user: UserDTO, websocket: WebSocket):
        self.user: UserDTO = user
        self.websocket: WebSocket = websocket
