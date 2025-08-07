import json


def get_config() -> dict:
    """ Opens config file and converts to dictionary. """

    with open('../config.json') as file:
        config = dict(json.load(file))
        return config


config_file = get_config()


class Config:
    host: str = config_file["startup_settings"]["host"]
    port: int = config_file["startup_settings"]["port"]


class Database:
    __database: str = config_file["database"]["dbname"]
    __username: str = config_file["database"]["user"]
    __password: str = config_file["database"]["password"]
    __host: str = config_file["database"]["host"]
    __port: int = config_file["database"]["port"]
    schema: str = config_file["database"]["schema"]

    def get_connection_string(self):
        return f"postgresql+asyncpg://{self.__username}:{self.__password}@{self.__host}:{self.__port}/{self.__database}"


class Auth:
    secret_key: str = config_file["auth"]["secret_key"]
    algorithm: str = config_file["auth"]["algorithm"]
    access_token_expire_minutes: int = config_file["auth"]["access_token_expire_minutes"]


config: Config = Config()
database: Database = Database()
auth: Auth = Auth()
