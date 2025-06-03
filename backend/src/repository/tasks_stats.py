from sqlalchemy import insert, select

from src.database.schemas import TasksStats
from src.repository import RepoInterface


class TasksStatsRepo(RepoInterface):
    async def create_user_answer(self, task_id: int, user_id: int, result: str) -> None:
        async with self.session_getter() as session:
            stmt = insert(TasksStats).values(task_id=task_id, user_id=user_id, result=result)
            await session.execute(stmt)

    async def get_all_tasks_count(self, task_ids: list[int]) -> int:
        async with self.session_getter() as session:
            stmt = select(TasksStats).where(TasksStats.task_id.in_(task_ids))
            res = await session.execute(stmt)
            return len(res.scalars().all())