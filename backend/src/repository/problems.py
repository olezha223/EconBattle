from sqlalchemy import select, func

from src.database.schemas import Problem
from src.models.problems import ProblemDTO
from src.repository import RepoInterface


class ProblemsRepo(RepoInterface):
    async def get_random_problems(self, count: int) -> list[ProblemDTO]:
        async with self.session_getter() as session:
            result = await session.execute(
                select(Problem)
                .order_by(func.random())
                .limit(count)
            )
            problems = result.scalars().all()
            return [
                ProblemDTO.model_validate(p, from_attributes=True) for p in problems
            ]