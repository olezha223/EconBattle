from fastapi import WebSocket
import asyncio

from src.game.engine.game import Game
from src.models.users import User


class Matchmaker:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.active_games = {}

    async def add_player(self, websocket: WebSocket, user: User):
        await self.queue.put((websocket, user))
        if self.queue.qsize() >= 2:
            player1_ws, player1 = await self.queue.get()
            player2_ws, player2 = await self.queue.get()
            game = Game(player1, player2, player1_ws, player2_ws)
            self.active_games[player1.id] = game
            self.active_games[player2.id] = game
            asyncio.create_task(game.start())