from sqlalchemy.orm import Session
from schemas.user import AuthorizationDto
from fastapi import HTTPException
from models.User import User
from utils.password_hasher import password_hasher
from utils.jwt_utils import encode_jwt
from schemas.response.user import AuthorizationResponse


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def registration(self, registration_dto: AuthorizationDto):
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

        token = encode_jwt(payload=jwt_payload)

        return AuthorizationResponse(
            user_id=user.id,
            token=token,
            token_type="Bearer"
        )

    def authorization(self, auth_dto: AuthorizationDto):
        user = self.db.query(User).filter(User.name == auth_dto.name).one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not password_hasher.verify(auth_dto.password, user.password):
            raise HTTPException(status_code=409, detail="Password is not correct")

        jwt_payload = {
            "sub": str(user.id)
        }

        token = encode_jwt(payload=jwt_payload)

        return AuthorizationResponse(
            user_id=user.id,
            token=token,
            token_type="Bearer"
        )
