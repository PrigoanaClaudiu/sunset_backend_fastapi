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

# class Settings_email(BaseSettings):
#     EMAIL_HOST: str
#     EMAIL_PORT: int
#     EMAIL_HOST_USER: str
#     EMAIL_HOST_PASSWORD: str
#     EMAIL_FROM: str
#     EMAIL_TO: str

#     class Config:
#         env_file = ".env"

# settings_email = Settings_email()
settings = Settings()