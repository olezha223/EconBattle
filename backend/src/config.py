import hashlib
import hmac
import os
import logging
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv
from dataclasses import dataclass, field
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).parent.parent


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass(frozen=True)
class AuthConfig:
    client_id: str = os.getenv('CLIENT_ID', 'example')
    client_secret: str = os.getenv('CLIENT_SECRET', 'example')


@dataclass
class DatabaseConfig:
    """Database connection variables."""

    name: Optional[str] = 'econ-battle'  # os.getenv('DBNAME')
    test_name: Optional[str] = 'test'  # os.getenv('TEST_DBNAME')
    user: Optional[str] = 'postgres'
    password: Optional[str] = 'postgres'
    port: int = 5432
    host: str = 'localhost'

    driver: str = 'asyncpg'
    database_system: str = 'postgresql'

    def build_testdb_connection_str(self) -> str:
        """Подключение к тестовой базе"""

        return URL.create(
            drivername=f'{self.database_system}+{self.driver}',
            username=self.user,
            database=self.test_name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)

    def build_connection_str(self) -> str:
        """This function build a connection string."""

        return URL.create(
            drivername=f'{self.database_system}+{self.driver}',
            username=self.user,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class AppConfig:
    """Bot configuration."""

    title = "MiniApp python hse"
    description = "Наше приложение"
    version = "1.0"
    root_path = ""

@dataclass
class RedisConf:
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    name: str = "active_players"

@dataclass
class Configuration:
    """All in one configuration's class."""

    debug: bool = bool(os.getenv('DEBUG'))
    logging_level: int = int(os.getenv('LOGGING_LEVEL', logging.INFO))
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    app: AppConfig = field(default_factory=AppConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)
    redis: RedisConf = field(default_factory=RedisConf)


configuration = Configuration()
