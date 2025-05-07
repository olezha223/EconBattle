from typing import List

from sqlalchemy import select

from src.database.schemas import Competition
from src.repository import RepoInterface


class CompetitionsRepo(RepoInterface):
    async def get_created_competitions(self, user_id: str) -> List[int]:
        stmt = select(Competition.id).where(Competition.creator_id == user_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()