import os
# import logging

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    TELEGRAM_TOKEN: str
    # DB_NAME: str = 'db.sqlite'
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "user-service"
    POSTGRES_PASSWORD: str = "user-service"
    POSTGRES_DB: str = "user-service"

    # @property
    # def database_url(self) -> str:
    #     return f"sqlite+aiosqlite:///{self.BASE_DIR}/{self.DB_NAME}"

    @property
    def database_url(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    # @property
    # def database_url(self) -> PostgresDsn:
    #     return PostgresDsn.build(
    #         scheme="postgresql+asyncpg",
    #         username=self.POSTGRES_USER,
    #         password=self.POSTGRES_PASSWORD,
    #         host=self.POSTGRES_HOST,
    #         port=self.POSTGRES_PORT,
    #         path=self.POSTGRES_DB,
    #         # query={
    #         #     "sslmode": "require" if self.POSTGRES else "disable"
    #         # },
    #     )
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )


settings = Settings()
