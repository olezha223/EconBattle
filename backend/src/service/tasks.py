from typing import Optional

from src.models.problems import TaskDTO, TaskFromAuthor, TaskPreview, TaskForGame, TaskDetailedDTO
from src.repository.competitions import CompetitionsRepo
from src.repository.tasks import TaskRepo
from src.repository.tasks_stats import TasksStatsRepo
from src.repository.users import UserRepo


class TaskService:
    def __init__(self, task_repo: TaskRepo, user_repo: UserRepo, competition_repo: CompetitionsRepo):
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.competition_repo = competition_repo
        self.tasks_stats_repo = TasksStatsRepo()

    @staticmethod
    def get_task_for_round(task: TaskDTO) -> TaskForGame:
        task_json = task.model_dump()
        del task_json['correct_value']
        task_json['created_at'] = task.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return TaskForGame(**task_json)

    async def get(self, task_id: int) -> Optional[TaskDetailedDTO]:
        task = await self.task_repo.get_task_by_id(task_id)
        if task:
            user = await self.user_repo.get_by_id(task.creator_id)
            return TaskDetailedDTO(
                **task.model_dump(),
                creator_name=user.username,
                picture=user.picture
            )
        return None

    async def create_task(self, task: TaskFromAuthor) -> int:
        return await self.task_repo.create_task(task)

    async def get_all_problems_previews_for_user(self, user_id: str) -> list[TaskPreview]:
        tasks = await self.task_repo.get_all_problems_for_user(user_id)
        return await self._get_previews(tasks)

    async def get_all_public_problems_previews_for_user(self, user_id: str) -> list[TaskPreview]:
        tasks = await self.task_repo.get_all_problems_for_user(user_id)
        tasks = [task for task in tasks if task.access_type == "public"]
        return await self._get_previews(tasks)

    async def get_all_problems_previews(self) -> list[TaskPreview]:
        tasks = await self.task_repo.get_all_problems()
        tasks = [task for task in tasks if task.access_type == "public"]
        return await self._get_previews(tasks)

    async def _get_previews(self, tasks: list[TaskDTO]) -> list[TaskPreview]:
        previews = []
        for task in tasks:
            creator = await self.user_repo.get_by_id(task.creator_id)
            used_in_competitions = await self.competition_repo.get_competitions_with_task(task.id)
            correct_percent = await self.tasks_stats_repo.get_correct_percent(task.id)
            preview = TaskPreview(
                created_at=task.created_at,
                id=task.id,
                creator_id=task.creator_id,
                name=task.name,
                used_in_competitions=len(used_in_competitions),
                creator_name=creator.username,
                price=task.price,
                access_type=task.access_type,
                picture=creator.picture,
                correct_percent=correct_percent
            )
            previews.append(preview)
        return previews
