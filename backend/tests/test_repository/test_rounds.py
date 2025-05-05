from src.database.schemas import Round
from src.models.round import RoundDTO, StatusEnum
from tests.conftest import round_repo, round_1_dto, round_2_dto


async def test_create(round_repo, round_1_dto):
    round_id = await round_repo.create(model=round_1_dto, orm=Round)
    assert round_id == 1


async def test_create_multiple(round_repo, round_1_dto, round_2_dto):
    round_id_1 = await round_repo.create(model=round_1_dto, orm=Round)
    round_id_2 = await round_repo.create(model=round_2_dto, orm=Round)
    assert round_id_1 == 1
    assert round_id_2 == 2


async def test_get(round_repo, round_1_dto, round_2_dto):
    round_id_1 = await round_repo.create(model=round_1_dto, orm=Round)
    round_id_2 = await round_repo.create(model=round_2_dto, orm=Round)
    assert round_id_1 == 1
    assert round_id_2 == 2

    round_1 = await round_repo.get(object_id=round_id_1, orm_class=Round, model_class=RoundDTO)
    round_2 = await round_repo.get(object_id=round_id_2, orm_class=Round, model_class=RoundDTO)
    assert round_1 == round_1_dto
    assert round_2 == round_2_dto