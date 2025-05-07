from src.repository.users import UserRepo
from tests.utils.adapter import get_session_test
from tests.conftest import user_1_dto, user_2_dto

user_repo = UserRepo(session_getter=get_session_test)


async def test_create_one():
    admin_id = await user_repo.create_with_username("admin", user_id='1')
    assert admin_id == '1'

async def test_create_similar_2():
    admin_id_1 = await user_repo.create_with_username("admin", user_id='1')
    admin_id_2 = await user_repo.create_with_username("admin", user_id='1')
    assert admin_id_1 == '1'
    assert admin_id_2 == '1'

async def test_create_two():
    admin_id = await user_repo.create_with_username("admin", user_id='1')
    other_id = await user_repo.create_with_username("other", user_id='2')
    assert admin_id == '1'
    assert other_id == '2'

async def test_get(user_1_dto):
    admin_id = await user_repo.create_with_username("user_1", user_id='1')
    admin = await user_repo.get_by_username("user_1")
    assert admin_id == '1'
    assert admin == user_1_dto

async def test_get_two(user_1_dto, user_2_dto):
    admin_id = await user_repo.create_with_username("user_1", user_id='1')
    other_id = await user_repo.create_with_username("user_2", user_id='2')
    assert admin_id == '1'
    assert other_id == '2'

    admin = await user_repo.get_by_username("user_1")
    other = await user_repo.get_by_username("user_2")
    assert admin == user_1_dto
    assert other == user_2_dto


async def test_get_not_existing():
    user = await user_repo.get_by_username("foo")
    assert user is None