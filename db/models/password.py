from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey
)

from sqlalchemy.orm import relationship

from db.models.users import DBUser


class DBPassword(BaseModel):
    __tablename__ = "password"

    user_id = Column(Integer, ForeignKey('users.id', ondelete="RESTRICT"), nullable=False)

    password = Column(Text)

    user = relationship("DBUser", lazy="raise", uselist=False)
