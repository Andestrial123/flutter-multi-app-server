import json
import logging.config
import os
from enum import Enum
from typing import NamedTuple

import yaml

logger = logging.getLogger(__name__)


class Environ(Enum):
    local = 0
    dev = 1
    staging = 2
    production = 3


class PostgresConfig(NamedTuple):
    username: str
    password: str
    host: str
    database: str
    port: int = 5432
    drivername: str = 'postgresql+asyncpg'
    echo: bool = False
    engine_props: dict = {"future": True, "pool_pre_ping": True, }

    @property
    def url(self) -> str:
        return f"{self.drivername}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class ConfigProvider:

    def __init__(self):
        self.__env = Environ[os.environ.get('ENV', 'local')]
        self.base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.config_path = os.path.join(self.base_path, 'config')

        firebase_creds_str = os.environ.get('FIREBASE_CREDS')
        self.__firebase_creds = json.loads(firebase_creds_str)

        filename = os.path.join(self.config_path, f'config-{self.env.name}.yaml')
        with open(filename, 'r') as f:
            self.__cfg = yaml.load(f, Loader=yaml.SafeLoader)

    @property
    def env(self) -> Environ:
        return self.__env

    @property
    def debug(self) -> bool:
        return self.__cfg['app']['debug']

    @property
    def service_name(self) -> str:
        return 'multi-app-webservice'

    @property
    def version(self) -> str:
        return '0.0.1'

    @property
    def logger_level(self) -> str:
        return self.__cfg['logger']['level']

    @property
    def logger_base_name(self) -> str:
        return self.__cfg['logger']['base_name']

    @property
    def db_host(self) -> str:
        default = self.__cfg['db']['host']

        return os.getenv("POSTGRES_HOST", default)

    @property
    def db_port(self) -> int:
        default = self.__cfg['db']['port']

        return os.getenv("POSTGRES_PORT", default)

    @property
    def db_name(self) -> str:
        default = self.__cfg['db']['name']

        return os.getenv("POSTGRES_DB", default)

    @property
    def firebase_creds(self) -> dict:
        return self.__firebase_creds


config = ConfigProvider()

logger.info(f"Environment: {config.env}")


class LoggerConfig:
    LEVEL = config.logger_level
    BASE_NAME = config.logger_base_name


db_secrets = {
    "username": os.getenv('POSTGRES_USER', "local_db"),
    "password": os.getenv('POSTGRES_PASSWORD', "local_db"),
    "host": os.getenv('POSTGRES_HOST', config.db_host),
    "database": os.getenv('POSTGRES_DB', config.db_name),
    "port": os.getenv('POSTGRES_PORT', config.db_port),
    "echo": bool(os.getenv('POSTGRES_ECHO', False)),
}

postgres_config = PostgresConfig(**db_secrets)
logger.info(f'<Config> {postgres_config}')
