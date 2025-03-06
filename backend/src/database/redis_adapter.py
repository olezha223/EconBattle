import redis
from typing import Optional, Dict


class RedisDictManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True  # Автоматическое декодирование из bytes в str
        )

    def add_dict(self, key: str, data: Dict) -> None:
        """
        Добавляет новый словарь в Redis Hash
        """
        self.client.hset(key, mapping=data)

    def count(self) -> int:
        """
        Возвращает общее количество ключей в базе данных
        """
        return self.client.dbsize()

    def pop(self) -> Optional[Dict]:
        """
        Извлекает и удаляет случайный словарь из базы
        """
        while True:
            key = self.client.randomkey()
            if not key:
                return None

            # Проверяем, что это хэш и удаляем атомарно
            data = self.client.hgetall(key)
            if self.client.delete(key):
                return data
            # Если не удалось удалить (параллельное удаление), пробуем снова


if __name__ == "__main__":
    # Инициализация
    manager = RedisDictManager()

    # Добавление данных
    manager.add_dict("user:1", {"name": "Alice", "age": "30"})
    manager.add_dict("user:2", {"name": "Bob", "age": "25"})

    # Получение количества записей
    print(manager.count())  # 2

    # Извлечение данных
    print(manager.pop())  # {'name': 'Alice', 'age': '30'}
    print(manager.count())  # 1