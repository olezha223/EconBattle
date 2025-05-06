from typing import Optional

from sqlalchemy import select, insert, update

from src.database.schemas import User
from src.models.users import UserDTO
from src.repository import RepoInterface


class UserRepo(RepoInterface):
    async def update_student_rating(self, rating_difference: int, user_id: int) -> None:
        stmt = update(User).where(User.id == user_id).values(student_rating=User.student_rating + rating_difference)
        async with self.session_getter() as session:
            await session.execute(stmt)

    async def update_teacher_rating(self, rating_difference: int, user_id: int) -> None:
        stmt = update(User).where(User.id == user_id).values(teacher_rating=User.teacher_rating + rating_difference)
        async with self.session_getter() as session:
            await session.execute(stmt)

    async def get_by_username(self, username: str) -> Optional[UserDTO]:
        async with self.session_getter() as session:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            scalar = result.scalar_one_or_none()
            if scalar:
                return UserDTO.model_validate(scalar, from_attributes=True)

    async def create_with_username(self, username: str, id: str) -> str:
        async with self.session_getter() as session:
            user = await self.get(object_id=id, orm_class=User, model_class=UserDTO)
            if not user:
                stmt = insert(User).values(username=username, id=id).returning(User.id)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
            return user.id
