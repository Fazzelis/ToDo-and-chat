from pydantic import BaseModel
from uuid import UUID


class PostDto(BaseModel):
    name: str
    state: bool


class CreateDto(BaseModel):
    name: str


class PostDtoResponse(PostDto):
    id: UUID
