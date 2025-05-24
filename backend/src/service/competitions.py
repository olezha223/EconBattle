from typing import Optional

from src.models.competition import CompetitionDTO, CompetitionPreview, NewCompetition, CompetitionDetailedDTO
from src.repository.competitions import CompetitionsRepo
from src.repository.games import GamesRepo
from src.repository.users import UserRepo


class CompetitionService:
    def __init__(
            self,
            competition_repo: CompetitionsRepo,
            games_repo: GamesRepo,
            user_repo: UserRepo,
    ):
        self.competition_repo = competition_repo
        self.games_repo = games_repo
        self.user_repo = user_repo

    async def get_competition(self, competition_id: int) -> Optional[CompetitionDetailedDTO]:
        competition = await self.competition_repo.get_by_id(competition_id)
        if competition:
            user = await self.user_repo.get_by_id(competition.creator_id)
            return CompetitionDetailedDTO(
                **competition.model_dump(),
                creator_name=user.username,
                picture=user.picture,
                max_time=get_max_time(competition.tasks_markup)
            )

    async def create_competition(self, competition: NewCompetition) -> int:
        return await self.competition_repo.create_competition(competition)

    async def get_all_competitions_created_by_user(self, user_id: str) -> list[CompetitionDTO]:
        return await self.competition_repo.get_all_competitions_created_by_user(user_id)

    async def get_all_competitions(self) -> list[CompetitionDTO]:
        return await self.competition_repo.get_all_competitions()

    async def get_all_competitions_previews_for_user(self, user_id: str) -> list[CompetitionPreview]:
        competitions = await self.get_all_competitions_created_by_user(user_id)
        return await self._get_previews(competitions)

    async def get_all_competitions_previews(self) -> list[CompetitionPreview]:
        competitions = await self.get_all_competitions()
        return await self._get_previews(competitions)

    async def _get_previews(self, competitions: list[CompetitionDTO]) -> list[CompetitionPreview]:
        result = []
        for competition in competitions:
            games_played = await self.games_repo.get_played_games_in_competition(competition_id=competition.id)
            unique_players = await self.games_repo.get_unique_players(games_played)
            creator = await self.user_repo.get_by_id(competition.creator_id)
            preview = CompetitionPreview(
                id=competition.id,
                name=competition.name,
                created_at=competition.created_at,
                games_played=len(games_played),
                unique_players=len(unique_players),
                creator_name=creator.username,
                creator_id=competition.creator_id,
                picture=creator.picture
            )
            result.append(preview)
        return result


def get_max_time(tasks_markup: dict) -> int:
    result = 0
    for task in tasks_markup.values():
        result += task.get("time_limit", 0)
    return result
