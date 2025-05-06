from src.repository.competitions import CompetitionsRepo
from src.repository.games import GamesRepo
from src.repository.tasks import TaskRepo
from src.repository.users import UserRepo
from src.service.competitions import CompetitionService
from src.service.tasks import TaskService
from src.service.users import UserService

def get_user_service():
    return UserService(
        user_repo=UserRepo(),
        games_repo=GamesRepo(),
        task_repo=TaskRepo(),
        competitions_repo=CompetitionsRepo()
    )

def get_task_service():
    return TaskService(
        task_repo=TaskRepo(),
    )

def get_competition_service():
    return CompetitionService(
        competition_repo=CompetitionsRepo(),
    )