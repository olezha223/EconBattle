import asyncio
from typing import Generator, Any

import pytest
import redis
from sqlalchemy import text

from src.config import configuration
from src.models.game import NewGame
from src.repository.game_queue.redis_queue import RedisQueue
from src.service import UserService, TaskService
from tests.utils.adapter import get_session_test
from tests.utils.sql_queries import INIT_COMMANDS, CLEANUP_SCRIPTS
from src.database.schemas import Round, Task, Competition, Game
from src.models.competition import CompetitionDTO
from src.repository.users import UserRepo
from src.repository.tasks import TaskRepo
from src.repository.rounds import RoundsRepo
from src.repository.games import GamesRepo
from src.repository.competitions import CompetitionsRepo
from src.models.problems import TaskDTO, TaskTypeEnum, AnswerTypeEnum, TaskFromAuthor
from src.models.round import StatusEnum, RoundDTO
from src.models.users import UserDTO, UserExtended, UserStatistics


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# создание базы данных
@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with get_session_test() as session:
        for command in INIT_COMMANDS:
            await session.execute(text(command))
    try:
        yield
    finally:
        async with get_session_test() as session:
            for command in CLEANUP_SCRIPTS:
                await session.execute(text(command))

@pytest.fixture(scope="function", autouse=True)
async def clear_redis():
    try:
        yield
    finally:
        redis_client = redis.Redis(
            host=configuration.redis.redis_host,
            port=configuration.redis.redis_port,
            db=configuration.redis.redis_db,
            decode_responses=True
        )
        keys = redis_client.keys("game_queue:*")
        if keys:
            redis_client.delete(*keys)


# репозитории
@pytest.fixture
async def redis_queue():
    return RedisQueue()

@pytest.fixture
async def user_repo():
    return UserRepo(session_getter=get_session_test)

@pytest.fixture
async def task_repo():
    return TaskRepo(session_getter=get_session_test)

@pytest.fixture
async def competition_repo():
    return CompetitionsRepo(session_getter=get_session_test)

@pytest.fixture
async def round_repo():
    return RoundsRepo(session_getter=get_session_test)

@pytest.fixture
async def games_repo():
    return GamesRepo(session_getter=get_session_test)

# сервисы
@pytest.fixture
async def user_service(user_repo, task_repo, competition_repo, games_repo):
    return UserService(
        user_repo=user_repo,
        task_repo=task_repo,
        games_repo=games_repo,
        competitions_repo=competition_repo
    )

@pytest.fixture
async def task_service(task_repo):
    return TaskService(task_repo=task_repo)

# блок с данными
@pytest.fixture
async def user_1_dto():
    return UserDTO(id='1', username="user_1",student_rating=1000,teacher_rating=1000)

@pytest.fixture
async def user_2_dto():
    return UserDTO(id='2', username="user_2",student_rating=1000,teacher_rating=1000)

@pytest.fixture
async def user_3_dto():
    return UserDTO(id='3', username="user_3", student_rating=1000, teacher_rating=1000)

@pytest.fixture
async def new_task_1_dto():
    return TaskFromAuthor(
        creator_id='1',
        name="test",
        text="test",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE.value,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )

@pytest.fixture
async def task_1_dto(new_task_1_dto):
    return TaskDTO(
        id=1,
        **new_task_1_dto.model_dump()
    )

@pytest.fixture
async def new_task_2_dto():
    return TaskFromAuthor(
        creator_id='2',
        name="test-2",
        text="test-2",
        price=1000,
        task_type=TaskTypeEnum.SINGLE_CHOICE,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )

@pytest.fixture
async def task_2_dto(new_task_2_dto):
    return TaskDTO(
        id=2,
        **new_task_2_dto.model_dump()
    )

@pytest.fixture
async def new_task_3_dto():
    return TaskFromAuthor(
        creator_id='2',
        name="test-3",
        text="test-3",
        price=1200,
        task_type=TaskTypeEnum.SINGLE_CHOICE.value,
        value={"answers": ["answer1", "answer2"]},
        answer_type=AnswerTypeEnum.STRING,
        correct_value={"correct": ["answer1"]}
    )

@pytest.fixture
async def task_3_dto(new_task_3_dto):
    return TaskDTO(
        id=3,
        **new_task_3_dto.model_dump()
    )

@pytest.fixture
async def competition_1_dto():
    return CompetitionDTO(
        name='тестовое соревнование с одним раундом с 1 задачей',
        creator_id='1',
        # settings
        max_players=2,
        max_rounds=1,
        round_time_in_seconds=1,
        tasks_markup={1: [1, ]}
    )

@pytest.fixture
async def competition_2_dto():
    return CompetitionDTO(
        name='тестовое соревнование с двумя раундами с 1 и 2 задачами соответственно',
        creator_id='2',
        # settings
        max_players=2,
        max_rounds=2,
        round_time_in_seconds=1,
        tasks_markup={1: [1, ], 2: [2, 3]}
    )

@pytest.fixture
async def round_1_dto():
    return RoundDTO(
        points_player_1=143,
        points_player_2=1342,
        status_player_1=StatusEnum.WINNER,
        status_player_2=StatusEnum.LOSER
    )

@pytest.fixture
async def round_2_dto():
    return RoundDTO(
        points_player_1=1453,
        points_player_2=1554,
        status_player_1=StatusEnum.WINNER,
        status_player_2=StatusEnum.LOSER
    )

@pytest.fixture
async def round_3_dto():
    return RoundDTO(
        points_player_1=1000,
        points_player_2=2000,
        status_player_1=StatusEnum.WINNER,
        status_player_2=StatusEnum.LOSER
    )

@pytest.fixture
async def game_1_dto():
    return NewGame(
        competition_id=1,
        player_1='1',
        player_2='2',
        rounds=[1, ],
        status_player_1=StatusEnum.WINNER.value,
        status_player_2=StatusEnum.LOSER.value,
        rating_difference_player_1=14,
        rating_difference_player_2=-20
    )

@pytest.fixture
async def game_2_dto():
    return NewGame(
        competition_id=1,
        player_1='1',
        player_2='2',
        rounds=[2, 3],
        status_player_1=StatusEnum.WINNER.value,
        status_player_2=StatusEnum.LOSER.value,
        rating_difference_player_1=14,
        rating_difference_player_2=-20
    )

@pytest.fixture
async def user_info_1_dto(user_1_dto):
    return UserExtended(
        **user_1_dto.model_dump(),
        played_games=[],
        created_competitions=[1, ],
        created_tasks=[1, ]
    )

# фикстуры для вставки данных
@pytest.fixture
async def create_users(user_repo, user_1_dto, user_2_dto, user_3_dto):
    user_id_1 = await user_repo.create_with_username(username="user_1", user_id='1')
    user_id_2 = await user_repo.create_with_username(username="user_2", user_id='2')
    user_id_3 = await user_repo.create_with_username(username="user_3", user_id='3')
    assert user_id_1 == '1'
    assert user_id_2 == '2'
    assert user_id_3 == '3'

    user_1 = await user_repo.get_by_username(username="user_1")
    user_2 = await user_repo.get_by_username(username="user_2")
    user_3 = await user_repo.get_by_username(username="user_3")
    assert user_1 == user_1_dto
    assert user_2 == user_2_dto
    assert user_3 == user_3_dto


@pytest.fixture
async def create_tasks(
        create_users, task_repo,
        task_1_dto, task_2_dto, task_3_dto,
        new_task_1_dto, new_task_2_dto, new_task_3_dto
):
    task_id_1 = await task_repo.create_task(new_task_1_dto)
    task_id_2 = await task_repo.create_task(new_task_2_dto)
    task_id_3 = await task_repo.create_task(new_task_3_dto)
    assert task_id_1 == 1
    assert task_id_2 == 2
    assert task_id_3 == 3

    task_1 = await task_repo.get_task_by_id(task_id_1)
    task_2 = await task_repo.get_task_by_id(task_id_2)
    task_3 = await task_repo.get_task_by_id(task_id_3)
    assert task_1 == task_1_dto
    assert task_2 == task_2_dto
    assert task_3 == task_3_dto


@pytest.fixture
async def create_competitions(create_tasks, competition_repo, competition_1_dto, competition_2_dto):
    # создание 1 соревнования с 1 раундом с 1 задачей
    dto_id_1 = await competition_repo.create(model=competition_1_dto, orm=Competition)
    dto_id_2 = await competition_repo.create(model=competition_2_dto, orm=Competition)
    assert dto_id_1 == 1
    assert dto_id_2 == 2

    # проверка фактических айди в базе
    dto_1 = await competition_repo.get(object_id=dto_id_1, orm_class=Competition, model_class=CompetitionDTO)
    dto_2 = await competition_repo.get(object_id=dto_id_2, orm_class=Competition, model_class=CompetitionDTO)
    assert dto_1 == competition_1_dto
    assert dto_2 == competition_2_dto


@pytest.fixture
async def create_rounds(create_competitions, round_repo, round_1_dto, round_2_dto, round_3_dto):
    # первый раунд игры в competition 1
    round_id_1 = await round_repo.create(model=round_1_dto, orm=Round)
    round_id_2 = await round_repo.create(model=round_2_dto, orm=Round)
    round_id_3 = await round_repo.create(model=round_3_dto, orm=Round)
    assert round_id_1 == 1
    assert round_id_2 == 2
    assert round_id_3 == 3
    # проверка айди
    round_1 = await round_repo.get(object_id=round_id_1, orm_class=Round, model_class=RoundDTO)
    round_2 = await round_repo.get(object_id=round_id_2, orm_class=Round, model_class=RoundDTO)
    round_3 = await round_repo.get(object_id=round_id_3, orm_class=Round, model_class=RoundDTO)
    assert round_1 == round_1_dto
    assert round_2 == round_2_dto
    assert round_3 == round_3_dto


@pytest.fixture
async def create_games(create_rounds, games_repo, game_1_dto, game_2_dto):
    dto_id_1 = await games_repo.create(model=game_1_dto, orm=Game)
    dto_id_2 = await games_repo.create(model=game_2_dto, orm=Game)
    assert dto_id_1 == 1
    assert dto_id_2 == 2

    dto_1 = await games_repo.get(object_id=dto_id_1, orm_class=Game, model_class=NewGame)
    dto_2 = await games_repo.get(object_id=dto_id_2, orm_class=Game, model_class=NewGame)
    assert dto_1 == game_1_dto
    assert dto_2 == game_2_dto

@pytest.fixture
async def user_stats_1_dto(create_competitions):
    return UserStatistics(
        wins_count=0,
        losses_count=0,
        tie_count=0,
        tasks_created=1,
        mean_task_difficulty=1000,
        competitions_created=1,
        games_played=0
    )