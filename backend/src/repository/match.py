import json

from sqlalchemy import insert

from src.database.schemas import Round, Match
from src.models.users import UserDTO
from src.repository import RepoInterface


class MatchRepo(RepoInterface):
    async def update_stats(self, players: dict[int, UserDTO], winner_id, current_round, rounds):
        async with self.session_getter() as session:
            match = Match(
                player1_id=players[list(players)[0]].id,
                player2_id=players[list(players)[1]].id,
                winner_id=winner_id
            )
            session.add(match)

            # Сохранение раундов
            for round_num in range(current_round):
                await session.execute(
                    insert(Round).values(
                        match_id=match.id,
                        round_number=round_num,
                        problems=json.dumps(
                            [p["id"] for p in rounds[round_num]["problems"]]
                        ),
                        player1_score=rounds[round_num]["scores"][list(players)[0]],
                        player2_score=rounds[round_num]["scores"][list(players)[1]]
                    )
                )
            await session.commit()