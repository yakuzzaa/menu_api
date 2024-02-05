from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    REDIS_PORT: int
    REDIS_HOST: str

    class Config:
        env_file = '.env'


settings = Settings()
