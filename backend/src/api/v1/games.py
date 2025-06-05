from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException
from starlette import status

from src.api.v1.users import get_current_active_user
from src.models.game import GameDTOExtended
from src.service import GameService, get_game_service, UserService, get_user_service

router_games = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router_games.get(
    "/all",
    description="Get all played games for user",
    tags=["games"],
    status_code=status.HTTP_200_OK,
    name="Get All Games",
)
async def get_all_games(
        user_id: str = Depends(get_current_active_user),
        service: GameService = Depends(get_game_service),
) -> List[GameDTOExtended]:
    return await service.get_all(user_id)