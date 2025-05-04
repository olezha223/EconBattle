from fastapi import APIRouter, Depends, Query
from starlette import status

from src.models.problems import TaskDTO
from src.service import get_problem_service
from src.service.problems import TaskService

router_problems = APIRouter(
    prefix="/problems",
    tags=["problems"],
)


@router_problems.get(
    path="/",
    description="Get Problem by task id",
    tags=["problems"],
    status_code=status.HTTP_200_OK,
    name="Get Problem",
)
async def get_problem(
        task_id: int = Query(..., description="ID of the task to retrieve"),
        service: TaskService = Depends(get_problem_service)
) -> TaskDTO:
    return await service.get(task_id=task_id)


