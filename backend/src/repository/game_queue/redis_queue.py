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

    def insert_player(self, competition_id: int, player_id: int) -> None:
        key = f"game_queue:{competition_id}"
        self.redis_client.rpush(key, str(player_id))

    def remove_player(self, competition_id: int, player_id: int) -> None:
        key = f"game_queue:{competition_id}"
        self.redis_client.lrem(key, 0, str(player_id))

    def check_exists(self, competition_id: int, player_id: int) -> bool:
        key = f"game_queue:{competition_id}"
        elements = self.redis_client.lrange(key, 0, -1)
        return str(player_id) in elements

    def get_len(self, competition_id: int) -> int:
        key = f"game_queue:{competition_id}"
        return self.redis_client.llen(key)

    def first(self, competition_id: int) -> int:
        key = f"game_queue:{competition_id}"
        element = self.redis_client.lindex(key, 0)
        return int(element) if element else None

    def get_first_2(self, competition_id: int) -> list[int]:
        key = f"game_queue:{competition_id}"
        return [int(e) for e in self.redis_client.lrange(key, 0, 1)]

    def pop(self, competition_id: int) -> int:
        key = f"game_queue:{competition_id}"
        element = self.redis_client.lpop(key)
        return int(element) if element else None

    def get_all(self, competition_id: int) -> list[int]:
        key = f"game_queue:{competition_id}"
        return [int(e) for e in self.redis_client.lrange(key, 0, -1)]

    def clear_all(self) -> None:
        keys = self.redis_client.keys("game_queue:*")
        if keys:
            self.redis_client.delete(*keys)
