from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException
from starlette import status

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
        user_id: str = Query(..., description="User ID"),
        service: GameService = Depends(get_game_service),
        user_service: UserService = Depends(get_user_service)
) -> List[GameDTOExtended]:
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await service.get_all(user_id)