from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Text,
    Integer,
    ForeignKey,
    String
)


class DBUser(BaseModel):
    __tablename__ = "users"

    username = Column(Text, nullable=False, unique=True)
    role = Column(String, nullable=True)

    employer_id = Column(Integer, ForeignKey("company.id"), nullable=True)

