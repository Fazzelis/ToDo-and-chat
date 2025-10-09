from pydantic import BaseModel
from schemas.task import PostDtoResponse


class TaskPostResponse(BaseModel):
    status: str
    info: PostDtoResponse


class AllTasksResponse(BaseModel):
    status: str
    tasks: list[PostDtoResponse]
