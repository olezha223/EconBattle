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
        """Подключен ли игрок к серверу"""
        return player_id in self.manager.active_connections

    def is_not_playing(self, player_id: str) -> bool:
        """Находится ли игрок в очереди ожидания"""
        return player_id not in self.active_players

    async def add_player(self, websocket: WebSocket, player_id: str, competition_id: int):
        """Добавление в очередь игроков с последующим входом в матч"""
        self.handle_connect(websocket, player_id, competition_id)

        # Когда мы вошли в очередь мы становимся в ней либо единственным, либо вторым человеком
        if self.game_queue.get_len(competition_id) >= 2:
            # Если мы второй человек, то длина очереди сразу станет больше 1
            # и надо будет достать игроков из очереди и создавать игру между ними
            await self.create_game(competition_id)
        else:
            # Если же мы первые в очереди мы будем ждать нашего соперника еще 60 секунд перед выходом из очереди
            start_time_waiting = time.time()
            while True:
                if time.time() - start_time_waiting >= 60: break
                if not self.is_not_playing(player_id): break
                if not self.is_player_connected(player_id): break
                # Если игрок играет ил не подключен к серверу или вышло время мы завершаем ожидание
                await asyncio.sleep(0.3)
            if not self.is_not_playing(player_id):
                # когда игрок начал играть мы просто следим, чтобы он был подключен,
                # когда надо - отключится внутри игры
                while True:
                    if not self.is_player_connected(player_id): break
                    await asyncio.sleep(0.3)
            else:
                try:
                    # если же после выхода из очереди мы играем,
                    # значит вышел лимит ожидания и надо отправить об этом сообщение и закрыть соединение
                    await websocket.send_json({"type": "search time limit reached"})
                    await websocket.close()
                except (RuntimeError, KeyError):
                    pass
                self.handle_disconnect(competition_id, player_id)
            # в конце на всякий случай пробуем закрыть соединение
            try:
                await websocket.close()
            except (RuntimeError, KeyError):
                pass
            self.handle_disconnect(competition_id, player_id)


    async def create_game(self, competition_id: int):
        """Создание игры"""
        # достаем игроков из очереди
        player_id_1 = self.game_queue.pop(competition_id)
        player_id_2 = self.game_queue.pop(competition_id)

        # добавляем пользователей в активных игроков
        self.active_players.add(player_id_1)
        self.active_players.add(player_id_2)

        # получаем данные из активных соединений и базы данных
        player_1 = self.manager.get_connection(player_id_1)
        player_2 = self.manager.get_connection(player_id_2)

        user_1 = await self.user_service.get_user(player_id_1)
        user_2 = await self.user_service.get_user(player_id_2)
        # Для первого игрока отправляем данные второго
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

        # даем игроку посмотреть, кто с ним играет
        await asyncio.sleep(5)

        game = Game(
            player1=Player(user=user_1, websocket=player_1),
            player2=Player(user=user_2, websocket=player_2),
            competition_id=competition_id
        )

        # долгожданный старт игры
        await game.start()

        # предварительно освобождаем ресурсы
        self.manager.remove_connection(player_id_1)
        self.manager.remove_connection(player_id_2)

        self.active_players.remove(player_id_1)
        self.active_players.remove(player_id_2)

    def handle_connect(self, websocket: WebSocket, player_id: str, competition_id: int):
        # при подключении необходимо добавить соединение игрока в активные и вставить его в очередь ожидания
        self.manager.add_connection(player_id, websocket)
        self.game_queue.insert_player(competition_id, player_id)

    def handle_disconnect(self, competition_id: int, player_id: str):
        # при отключении надо освободить ресурсы
        self.manager.remove_connection(player_id)
        self.game_queue.remove_player(competition_id, player_id)
