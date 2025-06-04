from typing import Optional

from sqlalchemy import select, insert, update, and_

from src.database.schemas import User
from src.models.users import UserDTO, UserData
from src.repository import RepoInterface


class UserRepo(RepoInterface):
    async def get_by_id(self, user_id: str) -> Optional[UserData]:
        return await self.get(object_id=user_id, orm_class=User, model_class=UserData)

    async def update_student_rating(self, rating_difference: int, user_id: str) -> None:
        actual_user = await self.get_by_id(user_id)
        if actual_user.student_rating + rating_difference < 0: # чтобы все сходилось в 0
            rating_difference = - actual_user.student_rating

        stmt = update(User).where(User.id == user_id).values(student_rating=User.student_rating + rating_difference)
        async with self.session_getter() as session:
            await session.execute(stmt)

    async def update_teacher_rating(self, rating_difference: int, user_id: str) -> None:
        actual_user = await self.get_by_id(user_id)
        if actual_user.teacher_rating + rating_difference < 0: # чтобы все сходилось в 0
            rating_difference = - actual_user.teacher_rating

        stmt = update(User).where(User.id == user_id).values(teacher_rating=User.teacher_rating + rating_difference)
        async with self.session_getter() as session:
            await session.execute(stmt)

    async def update_username(self, username: str, user_id: str) -> None:
        stmt = update(User).where(User.id == user_id).values(username=username)
        async with self.session_getter() as session:
            await session.execute(stmt)

    async def get_by_username(self, username: str) -> Optional[UserDTO]:
        async with self.session_getter() as session:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            scalar = result.scalar_one_or_none()
            if scalar:
                return UserDTO.model_validate(scalar, from_attributes=True)
            return None

    async def create_with_username(
            self,
            username: str,
            user_id: str,
            picture: str,
    ) -> str:
        get_result = await self.get_by_id(user_id)
        if get_result:
            return get_result.id
        return await self.create(model=UserDTO(username=username, id=user_id, picture=picture), orm=User)
