from src.models.problems import TaskDTO
from src.repository.tasks import TaskRepo


class TaskService:
    def __init__(self, problem_repo: TaskRepo):
        self.problem_repo = problem_repo

    async def get(self, task_id: int) -> TaskDTO:
        return await self.problem_repo.get(task_id)

    async def create(self, task: TaskDTO) -> int:
        return await self.problem_repo.create(task)