from src.database.schemas import Round
from src.models.round import RoundDTO
from src.repository.rounds import RoundsRepo


class RoundService:
    def __init__(self, round_repo: RoundsRepo):
        self.round_repo = round_repo

    async def create(self, model: RoundDTO) -> int:
        return await self.round_repo.create(model=model, orm=Round)
