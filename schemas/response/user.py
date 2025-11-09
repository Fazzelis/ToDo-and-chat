from pydantic import BaseModel
from uuid import UUID


class AuthorizationResponse(BaseModel):
    user_id: UUID
    token: str
    token_type: str
