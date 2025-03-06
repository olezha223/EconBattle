from fastapi import WebSocket, APIRouter, Depends
from starlette.websockets import WebSocketDisconnect

from src.game.matchmaker import Matchmaker
from src.models.users import UserDTO
from src.service import get_user_service, UserService

ws_router = APIRouter()

service = get_user_service()


async def get_current_user_ws(username: str = "Oleg") -> UserDTO:
    username: str = "Oleg"
    return await service.get(username)


manager = Matchmaker()


@ws_router.websocket("/ws")
async def websocket_endpoint(
        websocket: WebSocket
):
    username = websocket.query_params.get("username")
    user = await get_current_user_ws(username)
    try:
        await manager.connect(websocket, user)
    except WebSocketDisconnect:
        print("error")
        await manager.disconnect(websocket)
