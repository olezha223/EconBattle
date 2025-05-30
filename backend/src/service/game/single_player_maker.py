from starlette.websockets import WebSocket
from src.service import get_user_service
from src.service.game.connection_manager import ConnectionManager
import asyncio

from src.service.game.single_player_game import SinglePlayerGame


class SingleMatchMaker:
    def __init__(self):
        self.manager = ConnectionManager()
        self.user_service = get_user_service()
        self.games: dict[str, SinglePlayerGame] = dict()

    async def add_player(self, websocket: WebSocket, player_id: str, competition_id: int):
        self.manager.add_connection(player_id, websocket)
        # начать игру
        user = await self.user_service.get_user(player_id)
        game = SinglePlayerGame(
            user=user,
            websocket=websocket,
            competition_id=competition_id
        )
        self.games[player_id] = game
        await asyncio.sleep(1)
        await game.start()

        # удалить из активных соединений игроков
        self.manager.remove_connection(player_id)
