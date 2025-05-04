from src.repository.problems import ProblemRepo
from src.repository.users import UserRepo
from src.service.problems import TaskService
from src.service.users import UserService


def get_user_service() -> UserService:
    return UserService(user_repo=UserRepo())

def get_problem_service() -> TaskService:
    return TaskService(problem_repo=ProblemRepo())

__all__ = [
    'get_user_service', 'UserService',
    'get_problem_service', 'TaskService',
]
