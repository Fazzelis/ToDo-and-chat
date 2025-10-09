from sqlalchemy.orm import Session
from schemas.task import CreateDto
from models import Task
from schemas.response.task import AllTasksResponse, TaskPostResponse
from schemas.task import PostDtoResponse
from uuid import UUID
from fastapi import HTTPException


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, payload: CreateDto) -> TaskPostResponse:
        if payload.name == "":
            raise HTTPException(status_code=400, detail="empty field")
        db_task = Task(
            name=payload.name,
            state=False
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return TaskPostResponse(
            status="success",
            info=PostDtoResponse(
                id=db_task.id,
                name=db_task.name,
                state=db_task.state
            )
        )

    def get_all_tasks(self):
        tasks = self.db.query(Task).all()
        response_tasks = []
        for task in tasks:
            response_tasks.append(PostDtoResponse(
                id=task.id,
                name=task.name,
                state=task.state
            ))
        return AllTasksResponse(
            status="success",
            tasks=response_tasks
        )

    def get_task_by_id(self, task_id: UUID):
        task = self.db.query(Task).filter(Task.id == task_id).one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return TaskPostResponse(
            status="success",
            info=PostDtoResponse(
                id=task.id,
                name=task.name,
                state=task.state
            )
        )

    def put_task(self, task_id: UUID):
        task = self.db.query(Task).filter(Task.id == task_id).one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Задача под изменение не найдена")
        if task.state:
            task.state = False
        else:
            task.state = True
        self.db.add(task)
        self.db.commit()
        return TaskPostResponse(
            status="success",
            info=PostDtoResponse(
                id=task.id,
                name=task.name,
                state=task.state
            )
        )

    def delete_task(self, task_id: UUID):
        task = self.db.query(Task).filter(Task.id == task_id).one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Задача для удаления не найдена")
        self.db.delete(task)
        self.db.commit()
        return {
            "status": "success",
            "message": "Задача была успешно удалена"
        }

    def delete_all_tasks(self):
        deleted_tasks = self.db.query(Task).delete()
        self.db.commit()
        return {
            "status": "success",
            "count": deleted_tasks
        }
