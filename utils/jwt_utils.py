import os
from configuration import settings
from fastapi import HTTPException
import jwt



def encode_jwt(
        payload: dict,
        token_type: str,
        private_key: str = os.getenv("PRIVATE_KEY"),
        algorithm: str = os.getenv("ALGORITHM")
):
    if token_type == "access":
        expiration_time = settings.expiration_time_of_access_token_in_min
    elif token_type == "refresh":
        expiration_time = settings.expiration_time_of_refresh_token_in_min
    else:
        raise HTTPException(status_code=400, detail="Unknown token type")
