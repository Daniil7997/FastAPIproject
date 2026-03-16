from pydantic_settings import BaseSettings, SettingsConfigDict


class MySettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str 
    DB_NAME: str
    PRIVATE_KEY_HEX: str
    PUBLIC_KEY_HEX: str

    model_config = SettingsConfigDict(env_file="envs/main.env")

    @property
    def url_db_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def url_db_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = MySettings()
