from typing import List, Any

from fastapi import APIRouter, Depends, Query, HTTPException
from starlette import status

from src.models.problems import TaskDTO, TaskFromAuthor, TaskPreview
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
        service: TaskService = Depends(get_task_service)
) -> int:
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
        service: TaskService = Depends(get_task_service)
) -> TaskDTO:
    task = await service.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found",
        )
    return await service.get(task_id=task_id)

@router_problems.get(
    path="/previews",
    description="Get all problems previews for creator",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get all problems previews for creator",
)
async def get_all_problems_previews_for_user(
        user_id: str = Query(..., description="ID of the creator"),
        service: TaskService = Depends(get_task_service),
        user_service: UserService = Depends(get_user_service)
) -> List[TaskPreview]:
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await service.get_all_problems_previews_for_user(user_id)


@router_problems.get(
    path="/all",
    description="Get all problems previews",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get all problems previews",
)
async def get_all_problems_previews(
        service: TaskService = Depends(get_task_service),
) -> List[TaskPreview]:
    return await service.get_all_problems_previews()


@router_problems.get(
    path="/check-answer",
    description="Get correct answer by task id",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get correct"
)
async def get_answer(
        task_id: int = Query(..., description="ID of the task"),
        service: TaskService = Depends(get_task_service)
) -> dict[str, Any]:
    task = await service.get(task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found",
        )
    return task.correct_value
