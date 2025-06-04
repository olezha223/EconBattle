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

    async def get_correct_percent(self, task_id: int) -> int:
        async with self.session_getter() as session:
            # берем список всех попыток решить задачу и всех корректных попыток ее решить
            stmt_all = select(TasksStats.id).where(TasksStats.task_id == task_id)
            stmt_correct = stmt_all.where(TasksStats.result == 'correct')
            res = await session.execute(stmt_all)
            res_correct = await session.execute(stmt_correct)
            count_all = len(res.scalars().all())
            if count_all == 0:
                return 0
            return (len(res_correct.scalars().all()) / count_all) * 100