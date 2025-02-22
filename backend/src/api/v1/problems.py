from fastapi import APIRouter
from sqlalchemy import select, func

from src.database.adapter import get_session
from src.database.schemas import Problem
from src.models.problems import ProblemDTO

router_problems = APIRouter()


@router_problems.get("/get_problems")
async def get_problems():
    async with get_session() as session:
        result = await session.execute(
            select(Problem)
            .order_by(func.random())
            # .limit(1)
        )
    problems = result.scalars().all()
    return [
        ProblemDTO.model_validate(p, from_attributes=True) for p in problems
    ]

