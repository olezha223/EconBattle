from tests.conftest import user_service, create_competitions, user_info_1_dto, user_stats_1_dto

async def test_get_user_info(user_service, create_competitions, user_info_1_dto):
    user_info = await user_service.get_user_information('1')
    assert user_info == user_info_1_dto

async def test_get_user_statistics(user_service, create_competitions, user_stats_1_dto):
    user_stats = await user_service.get_user_statistics('1')
    assert user_stats == user_stats_1_dto