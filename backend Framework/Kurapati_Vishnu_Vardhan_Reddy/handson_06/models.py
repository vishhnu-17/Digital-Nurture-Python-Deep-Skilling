from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

class Course(Base):
    __tablename__="courses"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    code=Column(String)
    credits=Column(Integer)
    dept_id=Column(Integer)