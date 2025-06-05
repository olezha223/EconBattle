from typing import List, Any

from fastapi import APIRouter, Depends, Query, HTTPException
from starlette import status

from src.api.v1.users import get_current_user, get_current_active_user
from src.models.problems import TaskDTO, TaskFromAuthor, TaskPreview, TaskDetailedDTO
from src.service import get_task_service, UserService, get_user_service
from src.service.tasks import TaskService

router_problems = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router_problems.post(
    path="/",
    description="Create new Problem",
    tags=["tasks"],
    status_code=status.HTTP_201_CREATED,
    name="Create Problem",
)
async def create_problem(
        task: TaskFromAuthor,
        service: TaskService = Depends(get_task_service),
        current_user: dict = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service),
) -> int:
    creator = task.creator_id
    if creator != current_user['sub']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't create new task not with your author id",
        )
    user = await user_service.get_user(creator)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return await service.create_task(task)


@router_problems.get(
    path="/",
    description="Get Problem by task id",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get Problem",
)
async def get_problem(
        task_id: int = Query(..., description="ID of the task"),
        service: TaskService = Depends(get_task_service),
        current_user: dict = Depends(get_current_user),
) -> TaskDetailedDTO:
    task = await service.get(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.access_type == "private" and task.creator_id != current_user['sub']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this task is forbidden",
        )

    return task

@router_problems.get(
    path="/previews",
    description="Get all problems previews for profile page",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get all problems previews for creator",
)
async def get_all_problems_previews_for_user(
        user_id: str = Depends(get_current_active_user),
        service: TaskService = Depends(get_task_service),
        current_user: dict = Depends(get_current_user),
) -> List[TaskPreview]:
    if user_id != current_user['sub']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't access private page of user",
        )
    return await service.get_all_problems_previews_for_user(user_id)


@router_problems.get(
    path="/previews-public",
    description="Get all problems previews for creator",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get all problems previews for creator",
)
async def get_all_public_problems_previews_for_user(
        user_id: str = Query(..., description="ID of the creator"),
        service: TaskService = Depends(get_task_service),
        user_service: UserService = Depends(get_user_service),
) -> List[TaskPreview]:
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await service.get_all_public_problems_previews_for_user(user_id)


@router_problems.get(
    path="/all",
    description="Get all problems previews for public tasks feed",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get all problems previews",
)
async def get_all_problems_previews(
        service: TaskService = Depends(get_task_service),
) -> List[TaskPreview]:
    return await service.get_all_problems_previews()