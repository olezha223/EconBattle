from typing import Optional, Any
from src.database.schemas import Task
from src.models.problems import TaskDTO, TaskWithoutAnswers
from src.repository.tasks import TaskRepo


class TaskService:
    def __init__(self, task_repo: TaskRepo):
        self.task_repo = task_repo

    @staticmethod
    def get_task_without_answers(task: TaskDTO) -> TaskWithoutAnswers:
        task_json = task.model_dump()
        del task_json['correct_value']
        return TaskWithoutAnswers(**task_json)

    async def get(self, task_id: int) -> TaskDTO:
        task = await self.task_repo.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with id {task_id} not found")
        return task

    async def get_task_answer(self, task_id: int) -> dict[str, Any]:
        task = await self.get(task_id)
        return task.correct_value


    async def create(self, task: TaskDTO) -> int:
        return await self.task_repo.create(model=task, orm=Task)