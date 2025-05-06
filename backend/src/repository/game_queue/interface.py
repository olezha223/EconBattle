from abc import ABC, abstractmethod

class QueueInterface(ABC):
    @abstractmethod
    def insert_player(self, competition_id: int, player_id: str) -> None:
        """Добавить игрока в очередь для указанного соревнования"""
        ...

    @abstractmethod
    def remove_player(self, competition_id: int, player_id: str) -> None:
        """Удалить игрока из очереди для указанного соревнования"""
        ...

    @abstractmethod
    def check_exists(self, competition_id: int, player_id: str) -> bool:
        """Проверить наличие игрока в очереди для указанного соревнования"""
        ...

    @abstractmethod
    def get_len(self, competition_id: int) -> int:
        """Получить длину очереди для указанного соревнования"""
        ...

    @abstractmethod
    def first(self, competition_id: int) -> str:
        """Получить первого игрока из очереди для указанного соревнования"""
        ...

    @abstractmethod
    def get_first_2(self, competition_id: int) -> list[str]:
        """Получить первых двух игроков из очереди для указанного соревнования"""
        ...

    @abstractmethod
    def pop(self, competition_id: int) -> str:
        """Извлечь первого игрока из очереди для указанного соревнования"""
        ...

    @abstractmethod
    def get_all(self, competition_id: int) -> list[str]:
        """Получить всех игроков из очереди для указанного соревнования"""
        ...