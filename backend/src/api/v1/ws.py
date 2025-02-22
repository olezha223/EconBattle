from fastapi import WebSocket, APIRouter, Depends
from src.game.matchmaker import Matchmaker
from src.models.users import User

ws_router = APIRouter()
matchmaker = Matchmaker()


def get_current_user_ws() -> User:
    from random import randint
    res = randint(0, 3)
    if res > 1:
        return User(id=2, username='Oleg', rating=1000)
    return User(id=1, username='Misha', rating=1100)


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: User = Depends(get_current_user_ws)):
    await websocket.accept()
    print(user)
    print(websocket)
    await matchmaker.add_player(websocket, user)
