from fastapi import APIRouter, Depends, Form
from schemas.task import CreateDto
from services.task_service import TaskService
from sqlalchemy.orm import Session
from database.get_db import get_db
from schemas.response.task import TaskPostResponse, AllTasksResponse
from uuid import UUID

router = APIRouter(
    prefix="/task",
    tags=["Task"]
)


@router.post("/create", response_model=TaskPostResponse)
def post_task(
        name: str = Form(..., min_length=1),
        db: Session = Depends(get_db)
):
    payload = CreateDto(
        name=name
    )
    return TaskService(db=db).create_task(payload=payload)


@router.get('/get-all', response_model=AllTasksResponse)
def get_all_tasks(
        db: Session = Depends(get_db)
):
    return TaskService(db).get_all_tasks()


@router.get('/get-by-id', response_model=TaskPostResponse)
def get_task_by_id(
        task_id: UUID,
        db: Session = Depends(get_db)
):
    return TaskService(db).get_task_by_id(task_id=task_id)


@router.put('/put')
def put_task(
        task_id: UUID,
        db: Session = Depends(get_db)
):
    return TaskService(db).put_task(task_id=task_id)


@router.delete('/delete')
def delete_task(
        task_id: UUID,
        db: Session = Depends(get_db)
):
    return TaskService(db).delete_task(task_id=task_id)


@router.delete("/delete-all")
def delete_all_tasks(db: Session = Depends(get_db)):
    return TaskService(db).delete_all_tasks()
