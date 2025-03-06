import uuid

from fastapi import WebSocket
import asyncio
from src.game.engine.game import Game
from src.models.users import UserDTO, Player


class Matchmaker:
    def __init__(self):
        self.waiting_players: list[Player] = []
        # self.waiting_players = RedisDictManager()
        self.active_connections: dict[str, list[Player, Player]] = {}

    async def pair_players(self):
        print([p.user.model_dump() for p in self.waiting_players])

        while len(self.waiting_players) >= 2:
            player_1 = self.waiting_players[0]
            player_2 = self.waiting_players[1]
            game_id = str(uuid.uuid4())

            self.active_connections[game_id] = [player_1, player_2]

            await player_1.websocket.send_json({"type": "matched", "game_id": game_id})
            await player_2.websocket.send_json({"type": "matched", "game_id": game_id})

            # # создаем игру
            # game = Game(player1=player_1, player2=player_2)
            # await game.start()

    async def connect(self, websocket: WebSocket, user: UserDTO):
        await websocket.accept()
        # self.waiting_players.add_dict(key=str(user.id), data=user.model_dump())
        self.waiting_players.append(Player(user=user, websocket=websocket))
        await websocket.send_json({"type": "searching"})
        print(f'Пользователь {user.username} вошел в поиск')
        await self.pair_players()

    async def disconnect(self, websocket: WebSocket):
        for game_id, players in self.active_connections.items():
            for p in players:  # не больше двух итераций
                if p.websocket == websocket:
                    players.remove(p)
                    if len(players) > 1:
                        await players[0].websocket.send_json({"type": "opponent_disconnected"})
                    del self.active_connections[game_id]
                    break
