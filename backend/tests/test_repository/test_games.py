from src.database.schemas import Game
from src.models.game import GameDTO
from src.models.round import StatusEnum
from tests.conftest import create_rounds, games_repo, game_1_dto, game_2_dto, create_games

async def test_create(create_rounds, games_repo, game_1_dto):
    dto_id = await games_repo.create(model=game_1_dto, orm=Game)
    assert dto_id == 1


async def test_create_multiple(create_rounds, games_repo, game_1_dto, game_2_dto):
    rule_id = await games_repo.create(model=game_1_dto, orm=Game)
    assert rule_id == 1

    rule_id = await games_repo.create(model=game_2_dto, orm=Game)
    assert rule_id == 2


async def test_get(create_rounds, games_repo, game_1_dto, game_2_dto):
    dto_id_1 = await games_repo.create(model=game_1_dto, orm=Game)
    assert dto_id_1 == 1

    dto_id_2 = await games_repo.create(model=game_2_dto, orm=Game)
    assert dto_id_2 == 2

    dto_1 = await games_repo.get(object_id=dto_id_1, orm_class=Game, model_class=GameDTO)
    assert dto_1 == game_1_dto

    dto_2 = await games_repo.get(object_id=dto_id_2, orm_class=Game, model_class=GameDTO)
    assert dto_2 == game_2_dto


async def test_get_played_games(create_games, games_repo):
    assert await games_repo.get_played_games('1') == [1, 2]
    assert await games_repo.get_played_games('2') == [1, 2]