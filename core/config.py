from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
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

    CLICK_HOUSE_HOST: str = os.getenv("CLICK_HOUSE_HOST", "localhost")
    CLICK_HOUSE_PORT: int = int(os.getenv("CLICK_HOUSE_PORT", 9000))
    CLICK_HOUSE_DB: str = os.getenv("CLICK_HOUSE_DB", "statistic")
    CLICK_HOUSE_USER: str = os.getenv("CLICK_HOUSE_USER", "default_user")
    CLICK_HOUSE_PASSWORD: str = os.getenv("CLICK_HOUSE_PASSWORD", "")


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
