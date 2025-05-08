from src.repository.competitions import CompetitionsRepo
from src.repository.games import GamesRepo
from src.repository.rounds import RoundsRepo
from src.repository.tasks import TaskRepo
from src.repository.users import UserRepo
from src.service.competitions import CompetitionService
from src.service.games import GameService
from src.service.rounds import RoundService
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
        user_repo=UserRepo(),
        competition_repo=CompetitionsRepo(),
    )

def get_competition_service():
    return CompetitionService(
        competition_repo=CompetitionsRepo(),
        games_repo=GamesRepo(),
        user_repo=UserRepo(),
    )

def get_game_service():
    return GameService(
        game_repo=GamesRepo(),
        competition_repo=CompetitionsRepo(),
        user_repo=UserRepo(),
        round_repo=RoundsRepo(),
    )

def get_round_service():
    return RoundService(
        round_repo=RoundsRepo(),
    )