from src.repository.users import UserRepo
from src.service.users import UserService


def get_user_service() -> UserService:
    return UserService(user_repo=UserRepo())


__all__ = [
    'get_user_service', 'UserService',
]
