import pytest

from src.models.users import UserDTO
from src.repository.users import UserRepo
from tests.utils.adapter import get_session_test

user_repo = UserRepo(session_getter=get_session_test)

@pytest.fixture
async def create_user():
    user_id_1 = await user_repo.create_with_username(username="user_1")
    user_id_2 = await user_repo.create_with_username(username="user_2")
    user_id_3 = await user_repo.create_with_username(username="user_3")
    assert user_id_1 == 1
    assert user_id_2 == 2
    assert user_id_3 == 3

    user_1 = await user_repo.get_by_username(username="user_1")
    user_2 = await user_repo.get_by_username(username="user_2")
    user_3 = await user_repo.get_by_username(username="user_3")

    assert user_1 == UserDTO(
        id=user_1.id,
        username="user_1",
        student_rating=1000,
        teacher_rating=1000,
        # played_games=0,
        # created_competitions=0
    )

    assert user_2 == UserDTO(
        id=user_2.id,
        username="user_2",
        student_rating=1000,
        teacher_rating=1000,
        # played_games=0,
        # created_competitions=0
    )

    assert user_3 == UserDTO(
        id=user_3.id,
        username="user_3",
        student_rating=1000,
        teacher_rating=1000,
        # played_games=0,
        # created
        # _competitions=0
    )

