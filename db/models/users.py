from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Text,
)


class DBUser(BaseModel):
    __tablename__ = "user"

    username = Column(Text, nullable=False, unique=True)

