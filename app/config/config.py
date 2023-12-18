from os import environ
from dotenv import load_dotenv

load_dotenv()


class RedisSettings:
    REDIS_HOST: str = environ.get("REDIS_HOST")
    REDIS_PORT: int = environ.get("REDIS_PORT")


class DefaultServerSettings:
    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api/v1")
    APP_HOST: str = environ.get("APP_HOST")
    APP_PORT: int = int(environ.get("APP_PORT"))


MONGO_URL: str = environ.get("MONGO_URL")
