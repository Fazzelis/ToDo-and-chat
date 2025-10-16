from pydantic import BaseModel


class AuthorizationDto(BaseModel):
    name: str
    password: str
