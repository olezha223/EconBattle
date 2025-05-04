import pytest

from src.models.users import UserDTO
from src.repository.users import UserRepo
from tests.utils.adapter import get_session_test

user_repo = UserRepo(session_getter=get_session_test)

@pytest.fixture
async def create_user() -> UserDTO:
    user_id = await user_repo.create("user")
    assert user_id == 1

    user = await user_repo.get("user")
    assert user == UserDTO(
        id=user_id,
        username="user",
        student_rating=1000,
        teacher_rating=1000,
        # played_games=0,
        # created_competitions=0
    )
    return user
