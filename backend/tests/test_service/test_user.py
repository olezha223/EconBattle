from tests.conftest import (
    user_service, create_competitions, create_users,
    user_info_1_dto, user_stats_1_dto, user_1_dto
)

async def test_get_user_info(user_service, create_competitions, user_info_1_dto):
    user_info = await user_service.get_user_information('1')
    assert user_info == user_info_1_dto

async def test_get_user_statistics(user_service, create_competitions, user_stats_1_dto):
    user_stats = await user_service.get_user_statistics('1')
    assert user_stats == user_stats_1_dto

async def test_create_user(user_service, user_1_dto):
    user_1_id = await user_service.create_user(user_id=user_1_dto.id, username=user_1_dto.username)
    assert user_1_id == user_1_dto.id


async def test_double_create(user_service, user_1_dto):
    user_1_id = await user_service.create_user(user_id=user_1_dto.id, username=user_1_dto.username)
    assert user_1_id == user_1_dto.id
    user_1_id = await user_service.create_user(user_id=user_1_dto.id, username=user_1_dto.username)
    assert user_1_id == user_1_dto.id


async def test_get_user(user_service, create_users, user_1_dto):
    user_1 = await user_service.get_user("1")
    assert user_1 == user_1_dto

    user_none = await user_service.get_user("none")
    assert user_none is None