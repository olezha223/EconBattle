from typing import Optional

from src.database.schemas import User
from src.models.round import StatusEnum
from src.models.users import UserDTO, UserExtended, UserStatistics
from src.repository.competitions import CompetitionsRepo
from src.repository.games import GamesRepo
from src.repository.tasks import TaskRepo
from src.repository.users import UserRepo


class UserService:
    def __init__(
            self,
            user_repo: UserRepo,
            games_repo: GamesRepo,
            task_repo: TaskRepo,
            competitions_repo: CompetitionsRepo
    ):
        self.user_repo = user_repo
        self.games_repo = games_repo
        self.task_repo = task_repo
        self.competitions_repo = competitions_repo

    async def update_student_rating(self, rating_difference: int, user_id: int) -> None:
        await self.user_repo.update_student_rating(rating_difference, user_id)

    async def update_teacher_rating(self, rating_difference: int, user_id: int) -> None:
        await self.user_repo.update_teacher_rating(rating_difference, user_id)

    async def create_user(self, user_id: str, username: str) -> str:
        return await self.user_repo.create_with_username(user_id=user_id, username=username)

    async def get_user(self, user_id: str) -> Optional[UserDTO]:
        return await self.user_repo.get_by_id(user_id)

    async def get_user_information(self, user_id: str) -> UserExtended:
        user_base_info = await self.user_repo.get(object_id=user_id, orm_class=User, model_class=UserDTO)
        played_games = await self.games_repo.get_played_games(user_id)
        created_competitions = await self.competitions_repo.get_created_competitions(user_id)
        created_tasks = await self.task_repo.get_created_tasks(user_id)
        return UserExtended(
            **user_base_info.model_dump(),
            played_games=played_games,
            created_competitions=created_competitions,
            created_tasks=created_tasks
        )

    async def get_user_statistics(self, user_id: int) -> UserStatistics:
        user_info = await self.get_user_information(user_id)
        loses_count = await self.games_repo.get_status_count(user_id, StatusEnum.LOSER.value)
        wins_count = await self.games_repo.get_status_count(user_id, StatusEnum.WINNER.value)
        tie_count = await self.games_repo.get_status_count(user_id, StatusEnum.TIE.value)
        mean_task_difficulty = await self.task_repo.get_mean_task_difficulty(user_id)
        return UserStatistics(
            # статистика как игрока
            wins_count=wins_count,
            losses_count=loses_count,
            tie_count=tie_count,
            # статистика как составителя задач
            tasks_created=len(user_info.created_tasks),
            mean_task_difficulty=mean_task_difficulty,
            # статистика как организатора соревнований
            competitions_created=len(user_info.created_competitions),
            games_played=len(user_info.played_games),
        )