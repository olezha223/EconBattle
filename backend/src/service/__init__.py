from src.repository.competitions import CompetitionsRepo
from src.repository.games import GamesRepo
from src.repository.tasks import TaskRepo
from src.repository.users import UserRepo
from src.service.users import UserService

def get_user_service():
    return UserService(
        user_repo=UserRepo(),
        games_repo=GamesRepo(),
        task_repo=TaskRepo(),
        competitions_repo=CompetitionsRepo()
    )

