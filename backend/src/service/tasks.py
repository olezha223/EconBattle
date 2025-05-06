from typing import Optional
from src.database.schemas import Task
from src.models.problems import TaskDTO
from src.repository.tasks import TaskRepo


class TaskService:
    def __init__(self, task_repo: TaskRepo):
        self.task_repo = task_repo

    async def get(self, task_id: int) -> Optional[TaskDTO]:
        return await self.task_repo.get_task_by_id(task_id)

    async def create(self, task: TaskDTO) -> int:
        return await self.task_repo.create(model=task, orm=Task)