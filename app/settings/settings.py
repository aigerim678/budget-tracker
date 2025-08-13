import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    host: str = os.getenv("HOST")
    port: int = int(os.getenv("PORT"))


class Database:
    __database: str = os.getenv("DB_NAME")
    __username: str = os.getenv("DB_USER")
    __password: str = os.getenv("DB_PASSWORD")
    __host: str = os.getenv("DB_HOST")
    __port: int = int(os.getenv("DB_PORT"))
    schema: str = os.getenv("DB_SCHEMA")

    def get_connection_string(self):
        return f"postgresql+asyncpg://{self.__username}:{self.__password}@{self.__host}:{self.__port}/{self.__database}"


class Auth:
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class Cache:
    host: str = os.getenv("REDIS_HOST")
    port: int = int(os.getenv("REDIS_PORT"))
    db: int = int(os.getenv("REDIS_DB"))
    password: str = os.getenv("REDIS_PASS")


config: Config = Config()
database: Database = Database()
auth: Auth = Auth()
cache: Cache = Cache()
