from sqlalchemy import select, insert

from src.database.schemas import User
from src.models.users import UserDTO
from src.repository import RepoInterface


class UserRepo(RepoInterface):
    async def get(self, username: str) -> UserDTO:
        async with self.session_getter() as session:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            scalar = result.scalar_one_or_none()
            return UserDTO.model_validate(scalar, from_attributes=True)

    async def create(self, username) -> int:
        async with self.session_getter() as session:
            stmt = insert(User).values(username=username).returning(User.id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
