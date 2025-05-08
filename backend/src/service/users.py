from typing import Optional

from src.database.schemas import User
from src.models.round import StatusEnum
from src.models.users import UserDTO, UserInfo, UserData
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

    async def update_username(self, username: str, user_id: str) -> None:
        return await self.user_repo.update_username(user_id, username)

    async def create_user(self, user_id: str, username: str) -> str:
        return await self.user_repo.create_with_username(user_id=user_id, username=username)

    async def get_user(self, user_id: str) -> Optional[UserData]:
        return await self.user_repo.get_by_id(user_id)

    async def get_user_info(self, user_id: int) -> UserInfo:
        user_base_info = await self.user_repo.get(object_id=user_id, orm_class=User, model_class=UserDTO)
        loses_count = await self.games_repo.get_status_count(user_id, StatusEnum.LOSER.value)
        wins_count = await self.games_repo.get_status_count(user_id, StatusEnum.WINNER.value)
        tie_count = await self.games_repo.get_status_count(user_id, StatusEnum.TIE.value)
        mean_task_difficulty = await self.task_repo.get_mean_task_difficulty(user_id)
        return UserInfo(
            **user_base_info.model_dump(),
            # статистика как игрока
            wins_count=wins_count,
            losses_count=loses_count,
            tie_count=tie_count,
            # статистика как составителя задач
            tasks_created=len(await self.task_repo.get_created_tasks(user_id)),
            mean_task_difficulty=mean_task_difficulty,
            # статистика как организатора соревнований
            competitions_created=len(await self.competitions_repo.get_all_competitions_created_by_user(user_id)),
            games_played=len(await self.games_repo.get_played_games_by_user(user_id)),
        )