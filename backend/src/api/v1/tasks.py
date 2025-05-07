from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from src.models.problems import TaskDTO, TaskFromAuthor
from src.service import get_task_service
from src.service.tasks import TaskService

router_problems = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router_problems.get(
    path="/",
    description="Get Problem by task id",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get Problem",
)
async def get_problem(
        task_id: int = Query(..., description="ID of the task to retrieve"),
        service: TaskService = Depends(get_task_service)
) -> TaskDTO:
    return await service.get(task_id=task_id)


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
    return await service.create(task)


@router_problems.get(
    path='/all',
    description="Get all created problems for user",
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    name="Get All Problems",
)
async def get_all_problems(
        user_id: str = Query(..., description="User ID"),
        service: TaskService = Depends(get_task_service)
) -> List[TaskDTO]:
    return await service.get_all(user_id)