import os
from pydantic_settings import BaseSettings

#set env variables
class Settings(BaseSettings):
    # all str bcs it's an url
    database_hostname: str
    database_port: str
    database_pass: str
    database_name: str
    database_username: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()