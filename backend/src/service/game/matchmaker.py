from starlette.websockets import WebSocket

from src.models.users import Player
from src.repository.game_queue.interface import QueueInterface
from src.repository.game_queue.redis_queue import RedisQueue
from src.service import get_user_service
from src.service.game.connection_manager import ConnectionManager
import time
import asyncio

from src.service.game.game import Game


class MatchMaker:
    def __init__(self):
        self.manager = ConnectionManager()
        self.user_service = get_user_service()
        self.game_queue: QueueInterface = RedisQueue()
        self.games: dict[tuple[str, str], Game] = dict()

    def _search_in_games(self, player_id: str) -> bool:
        for key in self.games.keys():
            if player_id in key:
                return True
        return False

    def is_player_connected(self, player_id: str) -> bool:
        return player_id in self.manager.active_connections

    async def add_player(self, websocket: WebSocket, player_id: str, competition_id: int):
        # добавить игрока в активные соединения
        self.manager.add_connection(player_id, websocket)
        # добавить игроку в очередь для данного соревнования
        self.game_queue.insert_player(competition_id, player_id)

        start_waiting_time = time.time()
        while (
            self.game_queue.get_len(competition_id) <= 1 and
            time.time() - start_waiting_time < 3000 and
            self.manager.active_connections.get(player_id, False)
        ):
            await asyncio.sleep(2)
            if not self._search_in_games(player_id):
                try:
                    await websocket.send_json({"type": "waiting", "msg": f"For {time.time() - start_waiting_time} sec."})
                except RuntimeError:
                    continue
            else:
                continue
        if self.game_queue.get_len(competition_id) >= 2:
            await self.create_game(competition_id)
        else:
            try:
                await self.manager.active_connections[player_id].close()
            except (RuntimeError, KeyError):
                pass
            self.manager.remove_connection(player_id)
            self.game_queue.remove_player(competition_id, player_id)


    async def create_game(self, competition_id: int):
        player_id_1 = self.game_queue.pop(competition_id)
        player_id_2 = self.game_queue.pop(competition_id)

        player_1 = self.manager.get_connection(player_id_1)
        await player_1.send_json({"type": "matched", "msg": f"Ваш соперник: {player_id_2}"})

        player_2 = self.manager.get_connection(player_id_2)
        await player_2.send_json({"type": "matched", "msg": f"Ваш соперник: {player_id_1}"})

        user_1 = await self.user_service.get_user(player_id_1)
        user_2 = await self.user_service.get_user(player_id_2)
        game = Game(
            player1=Player(user=user_1, websocket=player_1),
            player2=Player(user=user_2, websocket=player_2),
            competition_id=competition_id
        )
        self.games[(player_id_1, player_id_2)] = game
        await asyncio.sleep(1)
        await game.start()
        del self.games[(player_id_1, player_id_2)]
        self.manager.remove_connection(player_id_1)
        self.manager.remove_connection(player_id_2)

    def handle_disconnect(self, competition_id: int, player_id: str):
        self.manager.remove_connection(player_id)
        self.game_queue.remove_player(competition_id, player_id)
