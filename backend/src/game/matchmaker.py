import uuid

from fastapi import WebSocket
import asyncio

from src.game.engine.game import Game
from src.models.users import User, Player


class Matchmaker:
    def __init__(self):
        self.waiting_players: list[Player] = []
        self.active_connections: dict[str, list[Player, Player]] = {}

    # async def add_player(self, websocket: WebSocket, user: User):
    #     self.waiting_players.append((websocket, user))
    #     if len(self.waiting_players) >= 2:
    #         player1_ws, player1 = await self.queue.get()
    #         player2_ws, player2 = await self.queue.get()
    #         game = Game(player1, player2, player1_ws, player2_ws)
    #         self.active_games[player1.id] = game
    #         self.active_games[player2.id] = game
    #         asyncio.create_task(game.start())

    async def pair_players(self):
        while len(self.waiting_players) >= 2:
            player_1 = self.waiting_players.pop(0)
            player_2 = self.waiting_players.pop(0)
            game_id = str(uuid.uuid4())

            self.active_connections[game_id] = [player_1, player_2]

            await player_1.websocket.send_json({"type": "matched", "game_id": game_id})
            await player_2.websocket.send_json({"type": "matched", "game_id": game_id})

            # создаем игру
            game = Game(player1=player_1, player2=player_2)
            await game.start()

    async def connect(self, websocket: WebSocket, user: User):
        await websocket.accept()
        self.waiting_players.append(Player(user=user, websocket=websocket))
        await websocket.send_json({"type": "searching"})
        await self.pair_players()

    async def disconnect(self, websocket: WebSocket):
        for game_id, players in self.active_connections.items():
            for p in players:  # не больше двух итераций
                if p.websocket == websocket:
                    players.remove(p)
                    if len(players) > 1:
                        await players[0].send_json({"type": "opponent_disconnected"})
                    del self.active_connections[game_id]
                    break

    # async def broadcast(self, game_id: str, message: dict, sender: WebSocket):
    #     players = self.active_connections.get(game_id, [])
    #     for player in players:
    #         if player.websocket != sender:
    #             await player.websocket.send_json(message)
