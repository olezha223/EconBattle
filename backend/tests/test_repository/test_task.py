from src.models.problems import TaskDTO, TaskTypeEnum, AnswerTypeEnum
from src.repository.tasks import TaskRepo
from tests.test_repository import create_user
from tests.utils.adapter import get_session_test

task_repo = TaskRepo(session_getter=get_session_test)

async def test_create(create_user):
    user = create_user

    task = TaskDTO(
        creator_id=user.id,
        name="test",
        text="test",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE.value,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )
    task_id = await task_repo.create(task)

    assert task_id == 1


async def test_create_multiple(create_user):
    user = create_user

    task = TaskDTO(
        creator_id=user.id,
        name="test",
        text="test",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE.value,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )
    task_id = await task_repo.create(task)

    assert task_id == 1

    task_2 = TaskDTO(
        creator_id=user.id,
        name="test-2",
        text="test-2",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )
    task_id = await task_repo.create(task_2)

    assert task_id == 2
