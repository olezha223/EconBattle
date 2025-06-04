from typing import List

from src.models.game import NewGame, GameDTOExtended
from src.repository.competitions import CompetitionsRepo
from src.repository.games import GamesRepo
from src.repository.rounds import RoundsRepo
from src.repository.users import UserRepo


class GameService:
    def __init__(
            self,
            game_repo: GamesRepo,
            round_repo: RoundsRepo,
            user_repo: UserRepo,
            competition_repo: CompetitionsRepo
    ):
        self.game_repo = game_repo
        self.round_repo = round_repo
        self.competition_repo = competition_repo
        self.user_repo = user_repo

    async def create_game(self, model: NewGame) -> int:
        return await self.game_repo.create_game(model)

    async def get_all(self, user_id: str) -> List[GameDTOExtended]:
        """Получить статистику игр"""
        games = await self.game_repo.get_played_games_by_user(user_id=user_id)
        result = []
        for game in games:
            round_data = []
            for round_id in game.rounds:
                round_data.append(await self.round_repo.get_by_id(round_id))
            competition = await self.competition_repo.get_by_id(game.competition_id)
            creator = await self.user_repo.get_by_id(competition.creator_id)
            creator_name = creator.username
            game_dto = GameDTOExtended(
                **game.model_dump(),
                round_data=round_data,
                competition_name=competition.name,
                creator_name=creator_name
            )
            result.append(game_dto)

        return result
