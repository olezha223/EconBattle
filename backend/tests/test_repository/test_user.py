import pytest

from src.models.users import UserDTO
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

async def test_get():
    admin_id = await user_repo.create("admin")
    assert admin_id == 1

    admin = await user_repo.get("admin")
    assert admin == UserDTO(
        id=admin_id,
        username="admin",
        student_rating=1000,
        teacher_rating=1000,
        #played_games=0,
        #created_competitions=0
    )

async def test_get_two():
    admin_id = await user_repo.create("admin")
    assert admin_id == 1

    other_id = await user_repo.create("other")
    assert other_id == 2

    admin = await user_repo.get("admin")
    assert admin == UserDTO(
        id=admin_id,
        username="admin",
        student_rating=1000,
        teacher_rating=1000,
        #played_games=0,
        #created_competitions=0
    )

    other = await user_repo.get("other")
    assert other == UserDTO(
        id=other_id,
        username="other",
        student_rating=1000,
        teacher_rating=1000,
        # played_games=0,
        # created_competitions=0
    )
