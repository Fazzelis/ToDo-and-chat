from pydantic_settings import BaseSettings
from fastapi.security import HTTPBearer
from typing import ClassVar


class Settings(BaseSettings):
    expiration_time_of_access_token_in_min: int = 5
    expiration_time_of_refresh_token_in_min: int = 20160

    expiration_time_of_access_token_in_sec: int = expiration_time_of_access_token_in_min*60
    expiration_time_of_refresh_token_in_sec: int = expiration_time_of_refresh_token_in_min*60

    http_bearer: ClassVar = HTTPBearer()

settings = Settings()
