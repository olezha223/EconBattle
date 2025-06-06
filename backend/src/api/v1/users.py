from fastapi import APIRouter, Depends, Query, HTTPException, Request
from starlette import status

from src.models.users import UserInfo
from src.service import UserService, get_user_service

router_user = APIRouter(
    prefix="/users",
    tags=["users"]
)

async def get_current_user(request: Request):
    """Проверяем наивно, что пользователь авторизован"""
    user = request.session.get('user')
    # если пользователь нам делает нужный запрос не авторизовавшись, мы не можем это позволить
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user

async def get_current_active_user(
        user_id: str = Query(..., title="User ID"),
        service: UserService = Depends(get_user_service),
):
    """Проверяем, что айди пользователя валиден"""
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user_id

@router_user.get(
    path="/info",
    description="Get user information",
    name="Get user information",
)
async def get_user_info(
        user_id: str = Depends(get_current_active_user),
        service: UserService = Depends(get_user_service),
) -> UserInfo:
    return await service.get_user_info(user_id)

@router_user.put(
    path='/update_username',
    description="Update username",
    name="Update username",
)
async def update_username(
        user_id: str = Depends(get_current_active_user),
        username: str = Query(..., title="New username"),
        service: UserService = Depends(get_user_service),
        current_user: dict = Depends(get_current_user),
) -> None:
    if user_id != current_user['sub']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't rename other user",
        )
    return await service.update_username(user_id, username)


@router_user.get(
    path="/picture",
    description="Get profile picture",
    name="Get profile picture"
)
async def get_user_picture(
        user_id: str = Depends(get_current_active_user),
        service: UserService = Depends(get_user_service),
) -> str:
    user = await service.get_user(user_id)
    return user.picture
