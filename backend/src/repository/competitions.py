from typing import List, Optional

from sqlalchemy import select, insert

from src.database.schemas import Competition
from src.models.competition import CompetitionDTO, NewCompetition
from src.repository import RepoInterface


class CompetitionsRepo(RepoInterface):
    async def create_competition(self, competition: NewCompetition) -> int:
        stmt = insert(Competition).values(**competition.model_dump()).returning(Competition.id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalar_one()

    async def get_by_id(self, competition_id: int) -> Optional[CompetitionDTO]:
        competition = await self.get(competition_id, orm_class=Competition, model_class=CompetitionDTO)
        return competition

    async def get_all_competitions_created_by_user(self, user_id: str) -> list[CompetitionDTO]:
        stmt = select(Competition).where(Competition.creator_id == user_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    async def get_created_competitions(self, user_id: str) -> List[int]:
        stmt = select(Competition.id).where(Competition.creator_id == user_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    async def get_all_competitions(self) -> List[CompetitionDTO]:
        stmt = select(Competition).order_by(Competition.created_at)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    async def get_competitions_with_task(self, task_id: int) -> List[CompetitionDTO]:
        all_competitions = await self.get_all_competitions()
        result = []
        for competition in all_competitions:
            for round_obj in competition.tasks_markup.values():
                if task_id in round_obj.get("tasks", []):
                    result.append(competition)
        return result

