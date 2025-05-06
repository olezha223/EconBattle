from src.database.schemas import Game
from src.models.game import GameDTO
from src.repository.games import GamesRepo


class GameService:
    def __init__(self, game_repo: GamesRepo):
        self.game_repo = game_repo

    async def create_game(self, model: GameDTO) -> int:
        return await self.game_repo.create(model, orm=Game)
