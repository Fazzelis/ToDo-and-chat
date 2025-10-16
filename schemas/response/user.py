from pydantic import BaseModel
from uuid import UUID


class AuthorizationResponse(BaseModel):
    user_id: UUID
    access_token: str
    token_type: str
