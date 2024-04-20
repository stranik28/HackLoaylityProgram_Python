from db.models.base import BaseModel
from sqlalchemy import Column, String


class DBCompany(BaseModel):
    __tablename__ = 'company'
    name = Column(String, unique=True, nullable=False)
    logo = Column(String, nullable=False)
    category = Column(String, nullable=False)
