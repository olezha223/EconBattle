from sqlalchemy import select, func, insert

from src.database.schemas import Task
from src.models.problems import TaskDTO
from src.repository import RepoInterface


class TaskRepo(RepoInterface):
    async def create(self, task: TaskDTO) -> int:
        async with self.session_getter() as session:
            result = await session.execute(
                insert(Task).values(**task.model_dump())
                .returning(Task.id)
            )
            task_id = result.scalar()
            return task_id

    async def get(self, task_id: int) -> TaskDTO:
        async with self.session_getter() as session:
            result = await session.execute(
                select(Task)
                .where(Task.id == task_id)
            )
            task = result.scalar()
            return TaskDTO.model_validate(task, from_attributes=True)