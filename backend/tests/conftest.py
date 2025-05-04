import asyncio
from typing import Generator, Any

import pytest
from sqlalchemy import text

from tests.utils.adapter import get_session_test
from tests.utils.sql_queries import get_cleanup_script, INIT_COMMANDS


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    tables = ['answers', 'tasks', 'users']
    async with get_session_test() as session:
        for command in INIT_COMMANDS:
            await session.execute(text(command))
    try:
        yield
    finally:
        async with get_session_test() as session:
            for table in tables:
                await session.execute(text(get_cleanup_script(table)))
