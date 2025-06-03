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
        self.active_players: set[str] = set()

    def is_player_connected(self, player_id: str) -> bool:
        return player_id in self.manager.active_connections

    def is_not_playing(self, player_id: str) -> bool:
        return player_id not in self.active_players

    async def add_player(self, websocket: WebSocket, player_id: str, competition_id: int):
        self.handle_connect(websocket, player_id, competition_id)
        if self.game_queue.get_len(competition_id) >= 2:
            await self.create_game(competition_id)
        else:
            start_time_waiting = time.time()
            while True:
                if time.time() - start_time_waiting >= 60: break
                if not self.is_not_playing(player_id): break
                if not self.is_player_connected(player_id): break
                await asyncio.sleep(0.3)
            if not self.is_not_playing(player_id):
                while True:
                    if not self.is_player_connected(player_id): break
                    await asyncio.sleep(0.3)
            else:
                try:
                    await websocket.send_json({"type": "search time limit reached"})
                    await websocket.close()
                except (RuntimeError, KeyError):
                    pass
                self.handle_disconnect(competition_id, player_id)
            try:
                await websocket.close()
            except (RuntimeError, KeyError):
                pass
            self.handle_disconnect(competition_id, player_id)


    async def create_game(self, competition_id: int):
        player_id_1 = self.game_queue.pop(competition_id)
        player_id_2 = self.game_queue.pop(competition_id)

        self.active_players.add(player_id_1)
        self.active_players.add(player_id_2)

        player_1 = self.manager.get_connection(player_id_1)
        player_2 = self.manager.get_connection(player_id_2)

        user_1 = await self.user_service.get_user(player_id_1)
        user_2 = await self.user_service.get_user(player_id_2)
        await player_1.send_json({
            "type": "matched",
            "msg": {
                "id": user_2.id,
                "username": user_2.username,
                "picture": user_2.picture,
                "student_rating": user_2.student_rating,
                "teacher_rating": user_2.teacher_rating,
                "created_at": user_2.created_at.isoformat()
            }
        })

        # Для второго игрока отправляем данные первого
        await player_2.send_json({
            "type": "matched",
            "msg": {
                "id": user_1.id,
                "username": user_1.username,
                "picture": user_1.picture,
                "student_rating": user_1.student_rating,
                "teacher_rating": user_1.teacher_rating,
                "created_at": user_1.created_at.isoformat()
            }
        })
        game = Game(
            player1=Player(user=user_1, websocket=player_1),
            player2=Player(user=user_2, websocket=player_2),
            competition_id=competition_id
        )
        # time.sleep(6)
        await asyncio.sleep(1)
        await game.start()
        self.manager.remove_connection(player_id_1)
        self.manager.remove_connection(player_id_2)

        self.active_players.remove(player_id_1)
        self.active_players.remove(player_id_2)

    def handle_connect(self, websocket: WebSocket, player_id: str, competition_id: int):
        self.manager.add_connection(player_id, websocket)
        self.game_queue.insert_player(competition_id, player_id)

    def handle_disconnect(self, competition_id: int, player_id: str):
        self.manager.remove_connection(player_id)
        self.game_queue.remove_player(competition_id, player_id)
