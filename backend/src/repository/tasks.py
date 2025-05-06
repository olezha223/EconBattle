from typing import List, Optional

from sqlalchemy import select, func, insert

from src.database.schemas import Task
from src.models.problems import TaskDTO
from src.repository import RepoInterface


class TaskRepo(RepoInterface):
    async def get_task_by_id(self, task_id: int) -> Optional[TaskDTO]:
        stmt = select(Task).where(Task.id == task_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()
            if task:
                return TaskDTO.model_validate(task, from_attributes=True)

    async def get_created_tasks(self, user_id: int) -> List[int]:
        stmt = select(Task.id).where(Task.creator_id == user_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    async def get_mean_task_difficulty(self, user_id: int) -> float:
        stmt = select(Task.price).where(Task.creator_id == user_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            price_list = result.scalars().fetchall()
            return 0 if len(price_list) == 0 else sum(price_list) / len(price_list)