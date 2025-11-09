from fastapi import APIRouter, Depends, Form
from schemas.task import CreateDto
from services.task_service import TaskService
from sqlalchemy.orm import Session
from database.get_db import get_db
from schemas.response.task import TaskPostResponse, AllTasksResponse
from uuid import UUID
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings

router = APIRouter(
    prefix="/task",
    tags=["Task"]
)


@router.post("/create", response_model=TaskPostResponse)
def post_task(
        name: str = Form(..., min_length=1),
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        db: Session = Depends(get_db)
):
    payload = CreateDto(
        name=name
    )
    return TaskService(db=db).create_task(payload=payload, encoded_jwt=credentials.credentials)


@router.get('/get-all', response_model=AllTasksResponse)
def get_all_tasks(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).get_all_tasks(encoded_jwt=credentials.credentials)


@router.get('/get-by-id', response_model=TaskPostResponse)
def get_task_by_id(
        task_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).get_task_by_id(task_id=task_id, encoded_jwt=credentials.credentials)


@router.put('/put')
def put_task(
        task_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).put_task(task_id=task_id, encoded_jwt=credentials.credentials)


@router.delete('/delete')
def delete_task(
        task_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).delete_task(task_id=task_id, encode_jwt=credentials.credentials)


@router.delete("/delete-all")
def delete_all_tasks(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
):
    return TaskService(db).delete_all_tasks(encoded_jwt=credentials.credentials)
