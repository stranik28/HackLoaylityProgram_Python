from db.models.base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship


class DBWallet(BaseModel):
    __tablename__ = "wallet"

    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(Integer)

    user = relationship("DBUser", lazy="raise", uselist=False)
