from src.database.schemas import Task
from src.models.problems import TaskDTO, TaskTypeEnum, AnswerTypeEnum
from src.repository.tasks import TaskRepo
from tests.test_repository import create_user
from tests.utils.adapter import get_session_test

task_repo = TaskRepo(session_getter=get_session_test)

async def test_create(create_user):
    task = TaskDTO(
        creator_id=1,
        name="test",
        text="test",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE.value,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )
    task_id = await task_repo.create(model=task, orm=Task)

    assert task_id == 1


async def test_create_multiple(create_user):
    task = TaskDTO(
        creator_id=1,
        name="test",
        text="test",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE.value,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )
    task_id = await task_repo.create(model=task, orm=Task)

    assert task_id == 1

    task_2 = TaskDTO(
        creator_id=2,
        name="test-2",
        text="test-2",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )
    task_id = await task_repo.create(model=task_2, orm=Task)

    assert task_id == 2

async def test_get(create_user):
    test_task_1 = TaskDTO(
        creator_id=1,
        name="test",
        text="test",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE.value,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )
    task_id_1 = await task_repo.create(model=test_task_1, orm=Task)

    assert task_id_1 == 1

    test_task_2 = TaskDTO(
        creator_id=2,
        name="test-2",
        text="test-2",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )
    task_id_2 = await task_repo.create(model=test_task_2, orm=Task)

    assert task_id_2 == 2

    task_1 = await task_repo.get(object_id=task_id_1, orm_class=Task, model_class=TaskDTO)
    assert task_1 == test_task_1

    task_2 = await task_repo.get(object_id=task_id_2, orm_class=Task, model_class=TaskDTO)
    assert task_2 == test_task_2