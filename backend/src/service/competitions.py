from typing import Optional

from src.database.schemas import Competition
from src.models.competition import CompetitionDTO
from src.repository.competitions import CompetitionsRepo


class CompetitionService:
    def __init__(self, competition_repo: CompetitionsRepo):
        self.competition_repo = competition_repo

    async def get_competition(self, competition_id: int) -> Optional[CompetitionDTO]:
        return await self.competition_repo.get(competition_id, Competition, CompetitionDTO)

    async def create_competition(self, competition: CompetitionDTO) -> int:
        return await self.competition_repo.create(competition, Competition)