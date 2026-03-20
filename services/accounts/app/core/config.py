from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class MySettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str 
    DB_NAME: str
    IS_TEST_DB: bool
    PRIVATE_KEY_HEX: str

    model_config = SettingsConfigDict(env_file="envs/.env.local",
                                      env_file_required=False,
                                      extra='ignore')


    @property
    def url_db_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = MySettings()
