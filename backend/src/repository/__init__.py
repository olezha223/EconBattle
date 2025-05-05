from typing import Type

from pydantic import BaseModel
from sqlalchemy import insert, select

from src.database.adapter import get_session
from src.database.schemas import Base


class RepoInterface:
    def __init__(self, session_getter=get_session):
        self.session_getter = session_getter

    async def create(self, model: BaseModel, orm: Type[Base]) -> int:
        async with self.session_getter() as session:
            result = await session.execute(
                insert(orm).values(**model.model_dump())
                .returning(orm.id)
            )
            return result.scalar()

    async def get(self, object_id: int, orm_class: Type[Base], model_class: Type[BaseModel]) -> BaseModel:
        async with self.session_getter() as session:
            result = await session.execute(
                select(orm_class)
                .where(orm_class.id == object_id)
            )
            result_data = result.scalar()
            return model_class.model_validate(result_data, from_attributes=True)