from src.database.schemas import Game
from src.models.game import GameDTO
from src.models.round import StatusEnum
from tests.conftest import create_rounds, games_repo

game_1 = GameDTO(
    competition_id=1,
    player_1='1',
    player_2='2',
    rounds=[1, ],
    status_player_1=StatusEnum.WINNER.value,
    status_player_2=StatusEnum.LOSER.value,
    rating_difference_player_1=14,
    rating_difference_player_2=-20
)

game_2 = GameDTO(
    competition_id=1,
    player_1='1',
    player_2='2',
    rounds=[2, 3],
    status_player_1=StatusEnum.WINNER.value,
    status_player_2=StatusEnum.LOSER.value,
    rating_difference_player_1=14,
    rating_difference_player_2=-20
)


async def test_create(create_rounds, games_repo):
    dto_id = await games_repo.create(model=game_1, orm=Game)
    assert dto_id == 1


async def test_create_multiple(create_rounds, games_repo):
    rule_id = await games_repo.create(model=game_1, orm=Game)
    assert rule_id == 1

    rule_id = await games_repo.create(model=game_2, orm=Game)
    assert rule_id == 2


async def test_get(create_rounds, games_repo):
    dto_id_1 = await games_repo.create(model=game_1, orm=Game)
    assert dto_id_1 == 1

    dto_id_2 = await games_repo.create(model=game_2, orm=Game)
    assert dto_id_2 == 2

    dto_1 = await games_repo.get(object_id=dto_id_1, orm_class=Game, model_class=GameDTO)
    assert dto_1 == game_1

    dto_2 = await games_repo.get(object_id=dto_id_2, orm_class=Game, model_class=GameDTO)
    assert dto_2 == game_2