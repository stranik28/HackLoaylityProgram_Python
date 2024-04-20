from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import BaseModel

from db.models.company import DBCompany
from db.models.users import DBUser


class DBOperation(BaseModel):
    __tablename__ = 'operation'
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    company = relationship("DBCompany", lazy="raise", uselist=False)
    user = relationship("DBUser", lazy="raise", uselist=False)
