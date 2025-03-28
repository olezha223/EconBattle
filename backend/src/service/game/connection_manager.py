from fastapi import WebSocket

from src.repository.game_queue.interface import QueueInterface
from src.repository.game_queue.python_list import PythonQueue
from src.repository.game_queue.redis_queue import RedisQueue


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = dict()
        self.game_queue: QueueInterface = RedisQueue()

    def add_connection(self, player_id: str, websocket: WebSocket):
        self.active_connections[player_id] = websocket
        self.game_queue.insert_player(player_id)

    def remove_connection(self, player_id: str):
        if player_id in self.active_connections.keys():
            del self.active_connections[player_id]
        self.game_queue.remove_player(player_id)

    def get_connection(self, player_id: str) -> WebSocket:
        return self.active_connections.get(player_id)