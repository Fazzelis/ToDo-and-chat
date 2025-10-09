from sqlalchemy import Column, func, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base


class Task(Base):
    __tablename__ = "record"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String)
    state = Column(Boolean)
