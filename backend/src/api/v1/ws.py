from fastapi import WebSocket, APIRouter, Depends
from starlette.websockets import WebSocketDisconnect

from src.game.matchmaker import Matchmaker
from src.models.users import User

ws_router = APIRouter()
matchmaker = Matchmaker()


def get_user_service():
    pass


def get_current_user_ws(username, service = Depends(get_user_service)) -> User:
    return User()


def get_ws_manager() -> Matchmaker:
    return Matchmaker()


@ws_router.websocket("/ws")
async def websocket_endpoint(
        websocket: WebSocket,
        manager: Matchmaker = Depends(get_ws_manager)
):
    username = websocket.query_params.get("username")
    user = get_current_user_ws(username)
    try:
        await manager.connect(websocket, user)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
