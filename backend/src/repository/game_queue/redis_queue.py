from src.config import configuration
from src.repository.game_queue.interface import QueueInterface
import redis


class RedisQueue(QueueInterface):
    def __init__(self):
        self.name = configuration.redis.name
        self.redis_client = redis.Redis(
            host=configuration.redis.redis_host,
            port=configuration.redis.redis_port,
            db=configuration.redis.redis_db
        )

    def get_len(self) -> int:
        return self.redis_client.hlen(self.name)

    def check_exists(self, player_id: str) -> bool:
        return self.redis_client.hexists(self.name, player_id)

    def remove_player(self, player_id: str) -> None:
        self.redis_client.hdel(self.name, player_id)

    def insert_player(self, player_id: str, state: str) -> None:
        self.redis_client.hset(self.name, player_id, state)

    def first(self) -> str:
        keys = self.redis_client.hkeys(self.name)
        return keys[0].decode('utf-8') if keys else ''

    def get_first_2(self) -> list[str, str]:
        keys = self.redis_client.hkeys(self.name)
        return [keys[0].decode('utf-8') if keys else '', keys[1].decode('utf-8') if keys else '']

    def pop(self) -> str:
        first = self.first()
        self.remove_player(first)
        return first