from abc import ABC, abstractmethod


class QueueInterface(ABC):
    @abstractmethod
    def insert_player(self, player_id: str, state: str) -> None:
        ...

    @abstractmethod
    def remove_player(self, player_id: str) -> None:
        ...

    @abstractmethod
    def check_exists(self, player_id: str) -> bool:
        ...

    @abstractmethod
    def get_len(self) -> int:
        ...

    @abstractmethod
    def first(self) -> str:
        ...

    @abstractmethod
    def get_first_2(self) -> list[str, str]:
        ...

    @abstractmethod
    def pop(self) -> str:
        ...
