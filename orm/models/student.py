from orm.models.base import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
)

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    major = Column(String(100), nullable=False)