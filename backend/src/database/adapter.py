from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine


from src.config import configuration


async_engine: AsyncEngine = _create_async_engine(
    url=configuration.db.build_connection_str(),
    echo=False, #configuration.debug,
    pool_pre_ping=True
)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            # Выполняю транзакцию
            yield session
            await session.commit()

        except Exception:
            # В случае ошибки откатываю все назад
            await session.rollback()
            raise

        finally:
            # В любом случае закрываю соединение
            await session.close()
