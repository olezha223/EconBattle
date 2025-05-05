import asyncio
from typing import Generator, Any

import pytest
from sqlalchemy import text

from tests.utils.adapter import get_session_test
from tests.utils.sql_queries import INIT_COMMANDS, CLEANUP_SCRIPTS


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with get_session_test() as session:
        for command in INIT_COMMANDS:
            await session.execute(text(command))
    try:
        yield
    finally:
        async with get_session_test() as session:
            for command in CLEANUP_SCRIPTS:
                await session.execute(text(command))
