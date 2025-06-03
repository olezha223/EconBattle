from typing import Optional

from src.models.competition import CompetitionDTO, CompetitionPreview, NewCompetition, CompetitionDetailedDTO
from src.repository.competitions import CompetitionsRepo
from src.repository.games import GamesRepo
from src.repository.tasks import TaskRepo
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
        self.task_repo = TaskRepo()

    async def get_competition(self, competition_id: int) -> Optional[CompetitionDetailedDTO]:
        competition = await self.competition_repo.get_by_id(competition_id)
        if competition:
            user = await self.user_repo.get_by_id(competition.creator_id)
            mean_task_difficulty = await self.task_repo.get_mean_task_difficulty_for_competition(competition.tasks_markup)
            percent_of_correct = await self.task_repo.get_correct_percentage(competition.tasks_markup)
            return CompetitionDetailedDTO(
                **competition.model_dump(),
                creator_name=user.username,
                picture=user.picture,
                max_time=get_max_time(competition.tasks_markup),
                mean_task_difficulty=mean_task_difficulty,
                percent_of_correct=percent_of_correct
            )
        return None

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
            mean_task_difficulty = await self.task_repo.get_mean_task_difficulty_for_competition(competition.tasks_markup)
            preview = CompetitionPreview(
                id=competition.id,
                name=competition.name,
                created_at=competition.created_at,
                games_played=len(games_played),
                unique_players=len(unique_players),
                creator_name=creator.username,
                creator_id=competition.creator_id,
                picture=creator.picture,
                mean_task_difficulty=mean_task_difficulty
            )
            result.append(preview)
        return result


def get_max_time(tasks_markup: dict) -> int:
    result = 0
    for task in tasks_markup.values():
        result += task.time_limit
    return result
