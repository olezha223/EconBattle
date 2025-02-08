from fastapi import WebSocket, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.adapter import get_session
from src.game.matchmaker import Matchmaker
from src.models.users import User

router = APIRouter()
matchmaker = Matchmaker()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: User = Depends(get_current_user_ws)):  # TODO: добавить эту функцию в auth/helpers.py
    await websocket.accept()
    await matchmaker.add_player(websocket, user)
