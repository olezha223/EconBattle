from sqlalchemy import insert

from src.database.schemas import TasksStats
from src.repository import RepoInterface


class TasksStatsRepo(RepoInterface):
    async def create_user_answer(self, task_id: int, user_id: int, result: str) -> None:
        async with self.session_getter() as session:
            stmt = insert(TasksStats).values(task_id=task_id, user_id=user_id, result=result)
            await session.execute(stmt)