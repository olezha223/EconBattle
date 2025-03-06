from src.models.users import UserDTO
from src.repository.users import UserRepo


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def get(self, username: str) -> UserDTO:
        return await self.user_repo.get(username)

    async def create(self, username: str) -> int:
        return await self.user_repo.create(username)
