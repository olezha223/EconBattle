from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = dict()

    def add_connection(self, player_id: int, websocket: WebSocket):
        """Добавить соединение в активные"""
        self.active_connections[player_id] = websocket

    def remove_connection(self, player_id: int):
        """Если еще не удалено, то удалить из активных соединений"""
        if player_id in self.active_connections.keys():
            del self.active_connections[player_id]

    def get_connection(self, player_id: int) -> WebSocket:
        """Получить вебсокет игрока"""
        return self.active_connections.get(player_id)