
#This file defines the database table using SQLAlchemy.
from sqlalchemy import Column, Integer, String, Float
from database import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    admission_no = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    phone_no = Column(String(15), nullable=False)
    cgpa = Column(Float, nullable=False)
    passing_year = Column(Integer, nullable=False)
