from fastapi import APIRouter, Depends, Query

from src.models.users import UserInfo
from src.service import UserService, get_user_service

router_user = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router_user.get(
    path="/info",
    description="Get user information",
    name="Get user information",
)
async def get_user_info(
        user_id: str = Query(..., title="User ID"),
        service: UserService = Depends(get_user_service),
) -> UserInfo:
    return await service.get_user_info(user_id)

@router_user.put(
    path='/update_username',
    description="Update username",
    name="Update username",
)
async def update_username(
        user_id: str = Query(..., title="User ID"),
        username: str = Query(..., title="New username"),
        service: UserService = Depends(get_user_service),
) -> None:
    return await service.update_username(user_id, username)