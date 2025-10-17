from sqlalchemy.orm import Session
from schemas.task import CreateDto
from models.Task import Task
from schemas.response.task import AllTasksResponse, TaskPostResponse
from schemas.task import PostDtoResponse
from uuid import UUID
from fastapi import HTTPException
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError
from models.User import User


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, payload: CreateDto, encoded_jwt: str | None) -> TaskPostResponse:
        if not encoded_jwt:
            raise HTTPException(status_code=401, detail="Token not found")
        try:
            user_id = decode_jwt(encoded_jwt)
            user = self.db.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if payload.name == "":
                raise HTTPException(status_code=400, detail="Empty field")

            db_task = Task(
                name=payload.name,
                state=False,
                user_id=user_id
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
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Access token expired")

    def get_all_tasks(self, encoded_jwt: str | None):
        if not encoded_jwt:
            raise HTTPException(status_code=401, detail="Access token not found")
        try:
            user_id = decode_jwt(encoded_jwt)
            user = self.db.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            tasks = self.db.query(Task).filter(Task.user_id == user_id).all()
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

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Access token expired")

    def get_task_by_id(self, task_id: UUID, encoded_jwt: str | None):
        if not encoded_jwt:
            raise HTTPException(status_code=401, detail="Access token not found")
        try:
            user_id = decode_jwt(encoded_jwt)
            user = self.db.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            task = self.db.query(Task).filter(Task.id == task_id).filter(Task.user_id == user_id).one_or_none()
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
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")

    def put_task(self, task_id: UUID, encoded_jwt: str | None):
        if not encoded_jwt:
            raise HTTPException(status_code=401, detail="Token not found")
        try:
            user_id = decode_jwt(encoded_jwt)
            user = self.db.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            task = self.db.query(Task).filter(Task.id == task_id).filter(Task.user_id == user_id).one_or_none()
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

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")

    def delete_task(self, task_id: UUID, encode_jwt: str | None):
        if not encode_jwt:
            raise HTTPException(status_code=401, detail="Token not found")
        try:
            user_id = decode_jwt(encode_jwt)
            user = self.db.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            task = self.db.query(Task).filter(Task.id == task_id).filter(Task.user_id == user_id).one_or_none()
            if not task:
                raise HTTPException(status_code=404, detail="Задача для удаления не найдена")
            self.db.delete(task)
            self.db.commit()
            return {
                "status": "success",
                "message": "Задача была успешно удалена"
            }

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")

    def delete_all_tasks(self, encoded_jwt: str | None):
        if not encoded_jwt:
            raise HTTPException(status_code=401, detail="Token not found")
        try:
            user_id = decode_jwt(encoded_jwt)
            user = self.db.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            deleted_tasks = self.db.query(Task).filter(Task.user_id == user_id).delete()
            self.db.commit()
            return {
                "status": "success",
                "count": deleted_tasks
            }

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
