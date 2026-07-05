from sqlalchemy import Column,Integer,String,ForeignKey,Date
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

class Course(Base):
    __tablename__="courses"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    code=Column(String)
    credits=Column(Integer)
    dept_id=Column(Integer,ForeignKey("departments.id"))
class Student(Base):
    __tablename__="Students"
    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String)
    last_name=Column(String)
    email=Column(String)
    year=Column(Integer)
    dept_id=Column(Integer,ForeignKey("departments.id"))    

class Enrollment(Base):
    __tablename__="enrollments"
    id=Column(Integer,primary_key=True)
    student_id=Column(Integer,ForeignKey("Students.id"))    
    course_id=Column(Integer,ForeignKey("courses.id"))
    enrollment_date=Column(Date)
    grade=Column(String,nullable=True)
    
class Department(Base):
    __tablename__="departments"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    hod=Column(String)
    budget=Column(Integer)
        