from fastapi import APIRouter, Response, Depends, Cookie
from schemas.user import AuthorizationDto
from database.get_db import get_db
from sqlalchemy.orm import Session
from services.user_service import UserService
from schemas.response.user import AuthorizationResponse


router = APIRouter(
    prefix="",
    tags=["Authorization"]
)


@router.post("/registration", response_model=AuthorizationResponse)
def registration(
        registration_dto: AuthorizationDto,
        response: Response,
        db: Session = Depends(get_db)
):
    return UserService(db).registration(registration_dto=registration_dto, response=response)


@router.post("/authorization", response_model=AuthorizationResponse)
def authorization(
        auth_dto: AuthorizationDto,
        response: Response,
        db: Session = Depends(get_db)
):
    return UserService(db).authorization(auth_dto=auth_dto, response=response)


@router.post("/refresh")
def refresh_tokens(
        response: Response,
        db: Session = Depends(get_db),
        refresh_token: str | None = Cookie(default=None)
):
    return UserService(db).refresh_tokens(response=response, refresh_token=refresh_token)
