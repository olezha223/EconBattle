from src.database.schemas import Competition
from src.models.competition import CompetitionDTO
from tests.conftest import create_tasks, competition_repo, competition_1_dto, competition_2_dto


async def test_create(create_tasks, competition_repo, competition_1_dto):
    dto_id = await competition_repo.create(model=competition_1_dto, orm=Competition)
    assert dto_id == 1


async def test_create_multiple(create_tasks, competition_repo, competition_1_dto, competition_2_dto):
    dto_id_1 = await competition_repo.create(model=competition_1_dto, orm=Competition)
    dto_id_2 = await competition_repo.create(model=competition_2_dto, orm=Competition)
    assert dto_id_1 == 1
    assert dto_id_2 == 2


async def test_get(create_tasks, competition_repo, competition_1_dto, competition_2_dto):
    # создание 1 соревнования с 1 раундом с 1 задачей
    dto_id_1 = await competition_repo.create(model=competition_1_dto, orm=Competition)
    # создание 2 соревнования с 2 раундами с 1 и 2 задачами соотв.
    dto_id_2 = await competition_repo.create(model=competition_2_dto, orm=Competition)
    assert dto_id_1 == 1
    assert dto_id_2 == 2

    # проверка фактических айди в базе
    dto_1 = await competition_repo.get(object_id=dto_id_1, orm_class=Competition, model_class=CompetitionDTO)
    dto_2 = await competition_repo.get(object_id=dto_id_2, orm_class=Competition, model_class=CompetitionDTO)
    assert dto_1 == competition_1_dto
    assert dto_2 == competition_2_dto


async def test_get_created_competitions(create_tasks, competition_repo, competition_1_dto, competition_2_dto):
    dto_id_1 = await competition_repo.create(model=competition_1_dto, orm=Competition)
    dto_id_2 = await competition_repo.create(model=competition_2_dto, orm=Competition)
    assert dto_id_1 == 1
    assert dto_id_2 == 2

    assert await competition_repo.get_created_competitions('1') == [1]
    assert await competition_repo.get_created_competitions('2') == [2]
    assert await competition_repo.get_created_competitions('3') == []