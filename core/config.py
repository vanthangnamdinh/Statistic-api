import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = ""

    CLICK_HOUSE_HOST: str = "localhost"
    CLICK_HOUSE_PORT: int = 9000
    CLICK_HOUSE_DB: str = "statistic"


class TestConfig(Config):
    CLICK_HOUSE_HOST: str = "localhost"
    CLICK_HOUSE_PORT: int = 9000
    CLICK_HOUSE_DB: str = "statistic"


class LocalConfig(Config):
    WRITER_DB_URL: str = "clickhouse+http://localhost:9000/statistic"


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "test": TestConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
