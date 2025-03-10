from src.models.users import Player, UserDTO
from src.service.game.connection_manager import ConnectionManager
import time
import asyncio

from src.service.game.game import Game


class MatchMaker:
    def __init__(self):
        self.manager = ConnectionManager()
        self.games: dict[tuple[str, str], Game] = dict()

    async def add_player(self, websocket, player_id):
        self.manager.add_connection(player_id, websocket)
        start_waiting_time = time.time()
        while (
            self.manager.game_queue.get_len() <= 1 and
            time.time() - start_waiting_time < 10 and
            self.manager.active_connections.get(player_id, False)
        ):
            await asyncio.sleep(2)
            try:
                await websocket.send_json({"type": "waiting", "msg": f"For {time.time() - start_waiting_time} sec."})
            except RuntimeError:
                pass
        if self.manager.game_queue.get_len() >= 2:
            player_id_1 = self.manager.game_queue.pop()
            player_id_2 = self.manager.game_queue.pop()

            player_1 = self.manager.get_connection(player_id_1)
            await player_1.send_json({"type": "matched", "msg": f"Ваш соперник: {player_id_2}"})

            player_2 = self.manager.get_connection(player_id_2)
            await player_2.send_json({"type": "matched", "msg": f"Ваш соперник: {player_id_1}"})
            # отрубить обоих игроков
            # await player_1.close()
            # await player_2.close()

            # удалить из данных
            self.manager.remove_connection(player_id_1)
            self.manager.remove_connection(player_id_2)

            # начать игру
            game = Game(
                player1=Player(
                    user=UserDTO(id=int(player_id_1), username="Oleg", rating=1000),
                    websocket=player_1
                ),
                player2=Player(
                    user=UserDTO(id=int(player_id_2), username="Misha", rating=1100),
                    websocket=player_2
                )
            )
            self.games[(player_id_1, player_id_2)] = game
            await game.start()
        else:
            # выйти из очереди и отключиться от сервера если никого не нашли
            try:
                await self.manager.active_connections[player_id].close()
            except (RuntimeError, KeyError): # отработает в случае с успешным завершением поиска партнера
                pass
            self.manager.remove_connection(player_id)
