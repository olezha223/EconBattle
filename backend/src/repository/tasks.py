from typing import List, Optional

from sqlalchemy import select, func, insert

from src.database.schemas import Task, TasksStats
from src.models.competition import Round
from src.models.problems import TaskDTO, TaskFromAuthor
from src.repository import RepoInterface


class TaskRepo(RepoInterface):
    async def get_task_by_id(self, task_id: int) -> Optional[TaskDTO]:
        stmt = select(Task).where(Task.id == task_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()
            if task:
                return TaskDTO.model_validate(task, from_attributes=True)
            return None

    async def get_created_tasks(self, user_id: int) -> List[TaskDTO]:
        stmt = select(Task).where(Task.creator_id == user_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    async def get_mean_task_difficulty(self, user_id: int) -> float:
        stmt = select(Task.price).where(Task.creator_id == user_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            price_list = result.scalars().fetchall()
            return 0 if len(price_list) == 0 else sum(price_list) / len(price_list)

    async def get_mean_task_difficulty_for_competition(self, tasks_markup: dict[str, Round]) -> float:
        task_ids = []
        for round_num in tasks_markup:
            if type(tasks_markup[round_num]) == dict:
                task_ids.extend(tasks_markup[round_num]['tasks'])
            else:
                task_ids.extend(tasks_markup[round_num].tasks)
        prices = []
        for task_id in task_ids:
            prices.append((await self.get_task_by_id(task_id)).price)

        if len(prices) == 0:
            return 0
        return round(sum(prices) / len(prices), 1)

    async def get_correct_percentage(self, tasks_markup: dict[str, Round]) -> float:
        task_ids = []
        for round_num in tasks_markup:
            task_ids.extend(tasks_markup[round_num].tasks)

        all_cases = 0
        all_correct = 0
        for task_id in task_ids:
            async with self.session_getter() as session:
                stmt_all = select(TasksStats.id).where(TasksStats.task_id == task_id)
                stmt_correct = stmt_all.where(TasksStats.result == 'correct')
                res = await session.execute(stmt_all)
                res_correct = await session.execute(stmt_correct)
                all_cases += len(res.scalars().all())
                all_correct += len(res_correct.scalars().all())
        if all_cases == 0 or all_correct == 0:
            return 0
        return round((all_correct / all_cases) * 100, 1)

    async def create_task(self, task: TaskFromAuthor) -> int:
        async with self.session_getter() as session:
            stmt = insert(Task).values(**task.model_dump()).returning(Task.id)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def get_all_problems_for_user(self, user_id: str) -> List[TaskDTO]:
        async with self.session_getter() as session:
            stmt = select(Task).where(Task.creator_id == user_id).order_by(Task.id)
            result = await session.execute(stmt)
            return [
                TaskDTO.model_validate(
                    task, from_attributes=True
                ) for task in result.scalars().fetchall()
            ]

    async def get_all_problems_without_user(self, user_id: str) -> List[TaskDTO]:
        async with self.session_getter() as session:
            stmt = select(Task).where(Task.creator_id != user_id).order_by(Task.id)
            result = await session.execute(stmt)
            return [
                TaskDTO.model_validate(
                    task, from_attributes=True
                ) for task in result.scalars().fetchall()
            ]

    async def get_all_problems(self) -> List[TaskDTO]:
        async with self.session_getter() as session:
            stmt = select(Task).order_by(Task.id)
            result = await session.execute(stmt)
            return [
                TaskDTO.model_validate(
                    task, from_attributes=True
                ) for task in result.scalars().fetchall()
            ]

