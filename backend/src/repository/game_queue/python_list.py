from src.repository.game_queue.interface import QueueInterface
from typing import List


class PythonQueue(QueueInterface):
    def __init__(self):
        self.python_list: List[str] = []

    def get_all(self) -> List[str]:
        return self.python_list

    def pop(self) -> str:
        first = self.first()
        self.remove_player(first)
        return first

    def get_first_2(self) -> List[str]:
        return self.python_list[:2]

    def first(self) -> str:
        return self.python_list[0]

    def get_len(self) -> int:
        return len(self.python_list)

    def check_exists(self, player_id: str) -> bool:
        return player_id in self.python_list

    def remove_player(self, player_id: str) -> None:
        self.python_list.remove(player_id)

    def insert_player(self, player_id: str, state: str) -> None:
        self.python_list.append(player_id)
