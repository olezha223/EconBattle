import pytest

from src.repository.users import UserRepo
from tests.utils.adapter import get_session_test

user_repo = UserRepo(session_getter=get_session_test)


async def test_create_one():
    admin_id = await user_repo.create("admin")
    assert admin_id == 1

async def test_create_similar_2():
    admin_id = await user_repo.create("admin")
    assert admin_id == 1

    admin_id = await user_repo.create("admin")
    assert admin_id == 2

async def test_create_two():
    admin_id = await user_repo.create("admin")
    assert admin_id == 1

    other_id = await user_repo.create("other")
    assert other_id == 2

