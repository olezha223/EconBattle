from abc import ABC, abstractmethod


class QueueInterface(ABC):
    @abstractmethod
    def insert_player(self, player_id: str, state: str) -> None:
        """Вставить игрока"""
        ...

    @abstractmethod
    def remove_player(self, player_id: str) -> None:
        """Убрать игрока"""
        ...

    @abstractmethod
    def check_exists(self, player_id: str) -> bool:
        """Проверить наличие"""
        ...

    @abstractmethod
    def get_len(self) -> int:
        """Длина очереди"""
        ...

    @abstractmethod
    def first(self) -> str:
        """Получить первый элемент"""
        ...

    @abstractmethod
    def get_first_2(self) -> list[str]:
        """Получить первые два элемента"""
        ...

    @abstractmethod
    def pop(self) -> str:
        """Достать и удалить первый элемент"""
        ...

    @abstractmethod
    def get_all(self) -> list[str]:
        """Получить всю очередь"""
        ...
