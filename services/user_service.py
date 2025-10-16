from sqlalchemy.orm import Session
from schemas.user import AuthorizationDto
from fastapi import Response, HTTPException
from models.User import User
from utils.password_hasher import password_hasher
from utils.jwt_utils import encode_jwt, decode_jwt
from configuration import settings
from schemas.response.user import AuthorizationResponse
from jwt import ExpiredSignatureError


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def registration(self, registration_dto: AuthorizationDto, response: Response):
        if len(registration_dto.name) <= 3:
            raise HTTPException(status_code=422, detail="The name length must be more than 3 characters")
        if len(registration_dto.password) <= 7:
            raise HTTPException(status_code=422, detail="The password length must be more than 8")
        optional_user = self.db.query(User).filter(User.name == registration_dto.name).one_or_none()
        if optional_user:
            raise HTTPException(status_code=409, detail="User with this name already exist")

        user = User(
            name=registration_dto.name,
            password=password_hasher.hash(registration_dto.password)
        )

        self.db.add(user)
        self.db.commit()

        jwt_payload = {
            "sub": str(user.id)
        }

        access_token = encode_jwt(payload=jwt_payload, token_type="access")
        refresh_token = encode_jwt(payload=jwt_payload, token_type="refresh")

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=settings.expiration_time_of_refresh_token_in_min
        )

        return AuthorizationResponse(
            user_id=user.id,
            access_token=access_token,
            token_type="Bearer"
        )

    def authorization(self, auth_dto: AuthorizationDto, response: Response):
        user = self.db.query(User).filter(User.name == auth_dto.name).one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not password_hasher.verify(auth_dto.password, user.password):
            raise HTTPException(status_code=409, detail="Password is not correct")

        jwt_payload = {
            "sub": str(user.id)
        }

        access_token = encode_jwt(payload=jwt_payload, token_type="access")
        refresh_token = encode_jwt(payload=jwt_payload, token_type="refresh")

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=settings.expiration_time_of_refresh_token_in_min
        )

        return AuthorizationResponse(
            user_id=user.id,
            access_token=access_token,
            token_type="Bearer"
        )

    def refresh_tokens(self, response: Response, refresh_token: str | None):
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token not found")
        try:
            user_id = decode_jwt(token=refresh_token)
            user = self.db.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            jwt_payload = {
                "sub": str(user_id)
            }

            access_token = encode_jwt(payload=jwt_payload, token_type="access")
            refresh_token = encode_jwt(payload=jwt_payload, token_type="refresh")

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="none",
                max_age=settings.expiration_time_of_refresh_token_in_min
            )

            return AuthorizationResponse(
                user_id=user_id,
                access_token=access_token,
                token_type="Bearer"
            )

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
