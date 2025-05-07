from src.database.schemas import Round
from src.models.round import RoundDTO
from src.repository import RepoInterface


class RoundsRepo(RepoInterface):
    async def get_by_id(self, round_id: int) -> RoundDTO:
        round_data = await self.get(object_id=round_id, orm_class=Round, model_class=RoundDTO)
        if not round_data:
            raise ValueError(f"Round {round_id} not found")
        return round_data