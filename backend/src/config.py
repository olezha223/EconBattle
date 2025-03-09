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
class AuthJWTConfig:
    bot_token: str = os.environ.get("BOT_TOKEN", '123')
    secret_key: str = hmac.new(bot_token.encode('utf-8'), "WebAppData".encode('utf-8'), hashlib.sha256).hexdigest()
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 30


@dataclass
class DatabaseConfig:
    """Database connection variables."""

    name: Optional[str] = 'econ-battle'  # os.getenv('DBNAME')
    # test_name: Optional[str] = os.getenv("TEST_DB_NAME")
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
            database=self.name,
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
    auth_jwt: AuthJWTConfig = field(default_factory=AuthJWTConfig)
    redis: RedisConf = field(default_factory=RedisConf)


configuration = Configuration()
