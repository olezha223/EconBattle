from typing import List

from sqlalchemy import select, or_, and_

from src.database.schemas import Game
from src.models.round import StatusEnum
from src.repository import RepoInterface


class GamesRepo(RepoInterface):
    async def get_played_games(self, user_id: int) -> List[int]:
        stmt = select(Game.id).where(or_(Game.player_1 == user_id, Game.player_2 == user_id))
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