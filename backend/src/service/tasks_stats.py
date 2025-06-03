from typing import Optional

from src.models.problems import TaskDTO
from src.repository.tasks_stats import TasksStatsRepo


class TaskStatsService:
    def __init__(
            self,
            tasks_stats_repo: TasksStatsRepo
    ):
        self.tasks_stats_repo = tasks_stats_repo

    async def create(self, pid: str, problem: TaskDTO, answer_list: Optional[list] = None) -> None:
        """Создает запись об ответе пользователя на задачу"""
        if answer_list:
            if answer_list == problem.correct_value.get("answers", []):
                result = "correct"
            else:
                result = "incorrect"
        else:
            result = "not done"
        await self.tasks_stats_repo.create_user_answer(
            user_id=pid,
            task_id=problem.id,
            result=result,
        )
