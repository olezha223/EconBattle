from src.database.schemas import Game
from src.models.game import GameDTO
from src.models.round import StatusEnum
from src.repository.games import GamesRepo
from tests.utils.adapter import get_session_test
from tests.test_repository import create_user

repo = GamesRepo(session_getter=get_session_test)

async def test_create(create_user):
    dto = GameDTO(
        player_1=1,
        player_2=2,
        rounds=[1,2,3],
        status_player_1=StatusEnum.WINNER.value,
        status_player_2=StatusEnum.LOSER.value,
        rating_difference_player_1=14,
        rating_difference_player_2=-20
    )

    dto_id = await repo.create(model=dto, orm=Game)

    assert dto_id == 1


async def test_create_multiple(create_user):
    rule = GameDTO(
        player_1=1,
        player_2=2,
        rounds=[1, 2, 3],
        status_player_1=StatusEnum.WINNER.value,
        status_player_2=StatusEnum.LOSER.value,
        rating_difference_player_1=14,
        rating_difference_player_2=-20
    )

    rule_id = await repo.create(model=rule, orm=Game)

    assert rule_id == 1

    rule = GameDTO(
        player_1=1,
        player_2=2,
        rounds=[1, 2, 3],
        status_player_1=StatusEnum.WINNER.value,
        status_player_2=StatusEnum.LOSER.value,
        rating_difference_player_1=14,
        rating_difference_player_2=-20
    )

    rule_id = await repo.create(model=rule, orm=Game)

    assert rule_id == 2


async def test_get(create_user):
    test_dto_1 = GameDTO(
        player_1=1,
        player_2=2,
        rounds=[1, 2, 3],
        status_player_1=StatusEnum.WINNER.value,
        status_player_2=StatusEnum.LOSER.value,
        rating_difference_player_1=14,
        rating_difference_player_2=-20
    )

    dto_id_1 = await repo.create(model=test_dto_1, orm=Game)

    assert dto_id_1 == 1

    test_dto_2 = GameDTO(
        player_1=1,
        player_2=2,
        rounds=[1, 2, 3],
        status_player_1=StatusEnum.WINNER.value,
        status_player_2=StatusEnum.LOSER.value,
        rating_difference_player_1=14,
        rating_difference_player_2=-20
    )

    dto_id_2 = await repo.create(model=test_dto_2, orm=Game)

    assert dto_id_2 == 2

    dto_1 = await repo.get(object_id=dto_id_1, orm_class=Game, model_class=GameDTO)
    assert dto_1 == test_dto_1

    dto_2 = await repo.get(object_id=dto_id_2, orm_class=Game, model_class=GameDTO)
    assert dto_2 == test_dto_2