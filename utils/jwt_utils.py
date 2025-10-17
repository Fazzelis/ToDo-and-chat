import os
from configuration import settings
from fastapi import HTTPException
import jwt
from jwt.exceptions import DecodeError
from datetime import datetime, timezone, timedelta
from uuid import UUID


def encode_jwt(
        payload: dict,
        private_key: str = os.getenv("PRIVATE_KEY"),
        algorithm: str = os.getenv("ALGORITHM")
):
    now = datetime.now(timezone.utc)
    expiration_time = now + timedelta(minutes=settings.expiration_time_of_refresh_token_in_min)
    payload.update(
        exp=int(expiration_time.timestamp()),
        iat=int(now.timestamp())
    )
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
        token,
        public_key: str = os.getenv("PUBLIC_KEY"),
        algorithm: str = os.getenv("ALGORITHM")
):
    try:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
            leeway=10
        )
        return UUID(decoded["sub"])
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
