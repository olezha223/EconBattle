from abc import ABC, abstractmethod


class QueueInterface(ABC):
    @abstractmethod
    def insert_player(self, player_id: int) -> None:
        """Вставить игрока"""
        ...

    @abstractmethod
    def remove_player(self, player_id: int) -> None:
        """Убрать игрока"""
        ...

    @abstractmethod
    def check_exists(self, player_id: int) -> bool:
        """Проверить наличие"""
        ...

    @abstractmethod
    def get_len(self) -> int:
        """Длина очереди"""
        ...

    @abstractmethod
    def first(self) -> int:
        """Получить первый элемент"""
        ...

    @abstractmethod
    def get_first_2(self) -> list[int]:
        """Получить первые два элемента"""
        ...

    @abstractmethod
    def pop(self) -> int:
        """Достать и удалить первый элемент"""
        ...

    @abstractmethod
    def get_all(self) -> list[int]:
        """Получить всю очередь"""
        ...
