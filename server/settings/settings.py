from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    APP_TITLE: str = 'online-shop'

    COOKIE_NAME: str = 'USER_SESSION'

    SECRET: str = ''

    PG_HOST: str = 'localhost'
    PG_PORT: int = 5432
    PG_DATABASE: str = 'postgres'
    PG_USER: str = 'postgres'
    PG_PASSWORD: str = 'postgres'


settings = Settings()
