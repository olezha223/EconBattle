from src.database.schemas import Task
from tests.conftest import create_users, task_repo, task_1_dto, task_2_dto, create_tasks


async def test_create(create_users, task_repo, task_1_dto):
    task_id = await task_repo.create(model=task_1_dto, orm=Task)
    assert task_id == 1


async def test_create_multiple(create_users, task_repo, task_1_dto, task_2_dto):
    task_id_1 = await task_repo.create(model=task_1_dto, orm=Task)
    task_id_2 = await task_repo.create(model=task_2_dto, orm=Task)
    assert task_id_1 == 1
    assert task_id_2 == 2


async def test_get(create_users, task_repo, task_1_dto, task_2_dto):
    task_id_1 = await task_repo.create(model=task_1_dto, orm=Task)
    task_id_2 = await task_repo.create(model=task_2_dto, orm=Task)
    assert task_id_1 == 1
    assert task_id_2 == 2

    task_1 = await task_repo.get_task_by_id(task_id_1)
    task_2 = await task_repo.get_task_by_id(task_id_2)
    assert task_1 == task_1_dto
    assert task_2 == task_2_dto


async def test_get_created_tasks(create_tasks, task_repo):
    assert await task_repo.get_created_tasks('1') == [1]
    assert await task_repo.get_created_tasks('2') == [2, 3]
    assert await task_repo.get_created_tasks('3') == []

async def test_get_mean_task_difficulty(create_tasks, task_repo):
    assert await task_repo.get_mean_task_difficulty('1') == 1000
    assert await task_repo.get_mean_task_difficulty('2') == 1100
    assert await task_repo.get_mean_task_difficulty('3') == 0
