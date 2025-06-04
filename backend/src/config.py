import os
import logging

from dotenv import load_dotenv
from dataclasses import dataclass, field
from sqlalchemy.engine import URL


dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass(frozen=True)
class AuthConfig:
    client_id: str = os.getenv('GOOGLE_CLIENT_ID', 'example')
    client_secret: str = os.getenv('GOOGLE_CLIENT_SECRET', 'example')


@dataclass
class DatabaseConfig:
    """Database connection variables."""

    name: str = os.getenv('DBNAME', 'example')
    test_name: str = os.getenv('TEST_DBNAME', 'example')
    user: str = os.getenv("POSTGRES_USER", "example")
    password: str = os.getenv("POSTGRES_PASSWORD", "example")
    port: int = os.getenv("POSTGRES_PORT", 5432)
    host: str = os.getenv("POSTGRES_HOST", "localhost")

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
    """App configuration."""

    title = "Курсовая работа"
    description = "Многопользовательская игра"
    version = "1.0"
    root_path = ""

@dataclass
class RedisConf:
    redis_host: str = os.getenv('REDIS_HOST', 'localhost')
    redis_port: int = os.getenv('REDIS_PORT', 6379)
    redis_db: int = 0

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
