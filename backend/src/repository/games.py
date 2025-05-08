from typing import List, Optional

from sqlalchemy import select, or_, and_, union_all

from src.database.schemas import Game
from src.models.game import NewGame, GameDTO
from src.models.round import StatusEnum
from src.repository import RepoInterface


class GamesRepo(RepoInterface):
    async def create_game(self, game_dto: NewGame) -> int:
        return await self.create(model=game_dto, orm=Game)

    async def get_by_id(self, game_id: int) -> Optional[GameDTO]:
        return await self.get(object_id=game_id, orm_class=Game, model_class=NewGame)

    async def get_played_games_by_user(self, user_id: int) -> List[GameDTO]:
        stmt = select(Game.id).where(or_(Game.player_1 == user_id, Game.player_2 == user_id))
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    async def get_played_games_in_competition(self, competition_id: int) -> List[int]:
        stmt = select(Game.id).where(Game.competition_id == competition_id)
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    async def get_unique_players(self, game_ids: List[int]) -> List[int]:
        player1_subquery = (
            select(Game.player_1.label('player'))
            .where(Game.id.in_(game_ids))
        )
        player2_subquery = (
            select(Game.player_2.label('player'))
            .where(Game.id.in_(game_ids))
        )
        combined = union_all(player1_subquery, player2_subquery).alias('combined')
        stmt = select(combined.c.player).distinct()
        async with self.session_getter() as session:
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    async def get_status_count(self, user_id: int, status: str) -> int:
        stmt_1 = select(Game.id).where(and_(Game.player_1 == user_id, Game.status_player_1 == status))
        stmt_2 = select(Game.id).where(and_(Game.player_2 == user_id, Game.status_player_2 == status))
        async with self.session_getter() as session:
            result_1 = await session.execute(stmt_1)
            result_2 = await session.execute(stmt_2)
            return len(result_1.scalars().fetchall()) + len(result_2.scalars().fetchall())