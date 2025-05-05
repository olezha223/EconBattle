from src.database.schemas import Task
from src.models.problems import TaskDTO, TaskTypeEnum, AnswerTypeEnum
from tests.conftest import create_users, task_repo, task_1_dto, task_2_dto


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

    task_1 = await task_repo.get(object_id=task_id_1, orm_class=Task, model_class=TaskDTO)
    task_2 = await task_repo.get(object_id=task_id_2, orm_class=Task, model_class=TaskDTO)
    assert task_1 == task_1_dto
    assert task_2 == task_2_dto