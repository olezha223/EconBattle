from src.models.problems import TaskDTO, TaskWithoutAnswers, TaskFromAuthor, TaskPreview, TaskForGame
from src.repository.competitions import CompetitionsRepo
from src.repository.tasks import TaskRepo
from src.repository.users import UserRepo


class TaskService:
    def __init__(self, task_repo: TaskRepo, user_repo: UserRepo, competition_repo: CompetitionsRepo):
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.competition_repo = competition_repo

    @staticmethod
    def get_task_for_round(task: TaskDTO) -> TaskForGame:
        task_json = task.model_dump()
        del task_json['correct_value']
        task_json['created_at'] = task.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return TaskForGame(**task_json)

    async def get(self, task_id: int) -> TaskDTO:
        task = await self.task_repo.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with id {task_id} not found")
        return task

    async def create_task(self, task: TaskFromAuthor) -> int:
        return await self.task_repo.create_task(task)

    async def get_all_problems_previews_for_user(self, user_id: str) -> list[TaskPreview]:
        tasks = await self.task_repo.get_all_problems_for_user(user_id)
        return await self._get_previews(tasks)

    async def get_all_problems_previews_without_users(self, user_id: str) -> list[TaskPreview]:
        tasks = await self.task_repo.get_all_problems_without_user(user_id)
        return await self._get_previews(tasks)

    async def _get_previews(self, tasks: list[TaskDTO]) -> list[TaskPreview]:
        previews = []
        for task in tasks:
            creator = await self.user_repo.get_by_id(task.creator_id)
            used_in_competitions = await self.competition_repo.get_competitions_with_task(task.id)
            preview = TaskPreview(
                created_at=task.created_at,
                id=task.id,
                creator_id=task.creator_id,
                name=task.name,
                used_in_competitions=len(used_in_competitions),
                creator_name=creator.username,
            )
            previews.append(preview)
        return previews
