from fastapi import APIRouter, Depends, Request
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
        db: Session = Depends(get_db)
):
    return UserService(db).registration(registration_dto=registration_dto)


@router.post("/authorization", response_model=AuthorizationResponse)
def authorization(
        auth_dto: AuthorizationDto,
        db: Session = Depends(get_db)
):
    return UserService(db).authorization(auth_dto=auth_dto)
