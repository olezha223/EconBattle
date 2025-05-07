from src.service import TaskService
from tests.conftest import create_tasks, task_service, new_task_1_dto, new_task_2_dto, create_users


async def test_create(task_service: TaskService, new_task_1_dto, new_task_2_dto, create_users):
    assert await task_service.create(new_task_1_dto) == 1
    assert await task_service.create(new_task_2_dto) == 2


async def test_double_create(task_service, new_task_1_dto, create_users):
    assert await task_service.create(new_task_1_dto) == 1
    assert await task_service.create(new_task_1_dto) == 2
