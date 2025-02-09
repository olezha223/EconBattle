from fastapi import WebSocket, APIRouter, Depends
from src.game.matchmaker import Matchmaker
from src.models.users import User

ws_router = APIRouter()
matchmaker = Matchmaker()


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: User = Depends(get_current_user_ws)):  # TODO: добавить эту функцию в auth/helpers.py
    await websocket.accept()
    await matchmaker.add_player(websocket, user)
