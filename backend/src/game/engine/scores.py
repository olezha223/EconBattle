# game/storage.py
import json
import aiofiles
import asyncio
from pathlib import Path


class JSONStorage:
    def __init__(self, file_path: str = "waiting_players.json"):
        self.file_path = Path(file_path)
        self.lock = asyncio.Lock()

    async def save(self, data: list):
        async with self.lock:
            async with aiofiles.open(self.file_path, 'w') as f:
                await f.write(json.dumps(data, default=str))  # default=str для объектов

    async def load(self) -> list:
        try:
            async with self.lock:
                async with aiofiles.open(self.file_path, 'r') as f:
                    content = await f.read()
                    return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return []