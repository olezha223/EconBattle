from src.config import configuration
from src.repository.game_queue.interface import QueueInterface
import redis


class RedisQueue(QueueInterface):
    def __init__(self):
        self.redis_client = redis.Redis(
            host=configuration.redis.redis_host,
            port=configuration.redis.redis_port,
            db=configuration.redis.redis_db,
            decode_responses=True
        )

    def insert_player(self, competition_id: int, player_id: str) -> None:
        key = f"game_queue:{competition_id}"
        self.redis_client.rpush(key, player_id)

    def remove_player(self, competition_id: int, player_id: str) -> None:
        key = f"game_queue:{competition_id}"
        self.redis_client.lrem(key, 0, player_id)

    def check_exists(self, competition_id: int, player_id: str) -> bool:
        key = f"game_queue:{competition_id}"
        elements = self.redis_client.lrange(key, 0, -1)
        return player_id in elements

    def get_len(self, competition_id: int) -> int:
        key = f"game_queue:{competition_id}"
        return self.redis_client.llen(key)

    def first(self, competition_id: int) -> str:
        key = f"game_queue:{competition_id}"
        element = self.redis_client.lindex(key, 0)
        return element if element else None

    def get_first_2(self, competition_id: int) -> list[str]:
        key = f"game_queue:{competition_id}"
        return [e for e in self.redis_client.lrange(key, 0, 1)]

    def pop(self, competition_id: int) -> str:
        key = f"game_queue:{competition_id}"
        element = self.redis_client.lpop(key)
        return element if element else None

    def get_all(self, competition_id: int) -> list[str]:
        key = f"game_queue:{competition_id}"
        return [e for e in self.redis_client.lrange(key, 0, -1)]

    def clear_all(self) -> None:
        keys = self.redis_client.keys("game_queue:*")
        if keys:
            self.redis_client.delete(*keys)
