from fastapi import WebSocket

from src.repository.game_queue.interface import QueueInterface
from src.repository.game_queue.python_list import PythonQueue
from src.repository.game_queue.redis_queue import RedisQueue


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = dict()

    def add_connection(self, player_id: int, websocket: WebSocket):
        self.active_connections[player_id] = websocket

    def remove_connection(self, player_id: int):
        if player_id in self.active_connections.keys():
            del self.active_connections[player_id]

    def get_connection(self, player_id: int) -> WebSocket:
        return self.active_connections.get(player_id)