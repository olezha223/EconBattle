from src.database.schemas import Round
from src.models.round import RoundDTO, StatusEnum
from src.repository.rounds import RoundsRepo
from tests.utils.adapter import get_session_test

round_repo = RoundsRepo(session_getter=get_session_test)

async def test_create():
    round_dto = RoundDTO(
        points_player_1=1,
        points_player_2=1,
        status_player_1=StatusEnum.WINNER,
        status_player_2=StatusEnum.LOSER
    )

    round_id = await round_repo.create(model=round_dto, orm=Round)

    assert round_id == 1


async def test_create_multiple():
    round_dto = RoundDTO(
        points_player_1=1,
        points_player_2=1,
        status_player_1=StatusEnum.WINNER,
        status_player_2=StatusEnum.LOSER
    )

    round_id = await round_repo.create(model=round_dto, orm=Round)

    assert round_id == 1

    round_dto = RoundDTO(
        points_player_1=1,
        points_player_2=1,
        status_player_1=StatusEnum.WINNER,
        status_player_2=StatusEnum.LOSER
    )

    round_id = await round_repo.create(model=round_dto, orm=Round)

    assert round_id == 2


async def test_get():
    test_round_1 = RoundDTO(
        points_player_1=1,
        points_player_2=1,
        status_player_1=StatusEnum.WINNER,
        status_player_2=StatusEnum.LOSER
    )

    round_id_1 = await round_repo.create(model=test_round_1, orm=Round)

    assert round_id_1 == 1

    test_round_2 = RoundDTO(
        points_player_1=1,
        points_player_2=1,
        status_player_1=StatusEnum.WINNER,
        status_player_2=StatusEnum.LOSER
    )

    round_id_2 = await round_repo.create(model=test_round_2, orm=Round)

    assert round_id_2 == 2

    round_1 = await round_repo.get(object_id=round_id_1, orm_class=Round, model_class=RoundDTO)
    assert round_1 == test_round_1

    round_2 = await round_repo.get(object_id=round_id_2, orm_class=Round, model_class=RoundDTO)
    assert round_2 == test_round_2