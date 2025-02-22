from pydantic import BaseModel
from fastapi import WebSocket


class User(BaseModel):
    id: int
    username: str
    rating: int


class Player(BaseModel):
    user: User
    websocket: WebSocket
