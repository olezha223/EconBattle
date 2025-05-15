from datetime import datetime, timedelta
from typing import Optional

from src.models.round import StatusEnum
from src.models.users import UserInfo, UserData
from src.repository.competitions import CompetitionsRepo
from src.repository.games import GamesRepo
from src.repository.tasks import TaskRepo
from src.repository.users import UserRepo


def get_dates(end_date: datetime) -> list[datetime]:
    start_date = datetime(2025, 2, 1)
    if end_date < start_date:
        return []
    delta = end_date - start_date
    days = delta.days + 1
    return [start_date + timedelta(days=i) for i in range(days)]


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

    async def create_user(
            self,
            user_id: str,
            username: str,
            picture: str,
    ) -> str:
        return await self.user_repo.create_with_username(user_id=user_id, username=username, picture=picture)

    async def get_user(self, user_id: str) -> Optional[UserData]:
        return await self.user_repo.get_by_id(user_id)

    async def _get_user_activity(self, user_id: str) -> dict[datetime, int]:  # Исправлен тип возвращаемого значения
        today = datetime.today()
        games = await self.games_repo.get_played_games_by_user(user_id)
        games_created_at_by_user = [game.created_at for game in games]
        tasks = await self.task_repo.get_created_tasks(user_id)
        tasks_created_at_by_user = [task.created_at for task in tasks]
        competitions = await self.competitions_repo.get_all_competitions_created_by_user(user_id)
        competitions_created_at_by_user = [competition.created_at for competition in competitions]

        # Нормализуем даты игр до начала дня (00:00:00)
        normalized_dates = [
            datetime(dt.year, dt.month, dt.day)  # Убираем время, оставляем только дату
            for dt in games_created_at_by_user + tasks_created_at_by_user + competitions_created_at_by_user
        ]

        # Создаем словарь для подсчета
        count_dict = {}
        for dt in normalized_dates:
            count_dict[dt] = count_dict.get(dt, 0) + 1

        # Заполняем результат
        result = {}
        for date in get_dates(today):  # date уже имеет время 00:00:00
            result[date] = count_dict.get(date, 0)  # Используем get для отсутствующих дат

        return result

    async def get_user_info(self, user_id: int) -> UserInfo:
        user_base_info = await self.get_user(user_id)
        loses_count = await self.games_repo.get_status_count(user_id, StatusEnum.LOSER.value)
        wins_count = await self.games_repo.get_status_count(user_id, StatusEnum.WINNER.value)
        tie_count = await self.games_repo.get_status_count(user_id, StatusEnum.TIE.value)
        mean_task_difficulty = await self.task_repo.get_mean_task_difficulty(user_id)
        user_activity = await self._get_user_activity(user_id)
        return UserInfo(
            **user_base_info.model_dump(),
            user_activity=user_activity,
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