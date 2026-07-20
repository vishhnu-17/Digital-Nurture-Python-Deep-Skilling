from sqlalchemy import (create_engine,
           Column,Integer,String,Numeric,ForeignKey)
from sqlalchemy.orm import declarative_base,relationship
DATABASE_URL="mysql+mysqlconnector://root:1234@localhost:3306/college_db_orm"
from sqlalchemy.orm import sessionmaker
engine= create_engine(DATABASE_URL,echo=True)
SessionLocal=sessionmaker(bind=engine)
session=SessionLocal()
base=declarative_base()

class Department(base):
    __tablename__="departments"
    department_id=Column(Integer,primary_key=True)
    department_name=Column(String(50),nullable=False)
    students=relationship("Student",back_populates="department")
    courses=relationship("Course",back_populates="department")
    professors=relationship("Professor",back_populates="department")    
class Student(base):
    __tablename__="students"
    student_id=Column(Integer,primary_key=True,autoincrement=False)
    first_name=Column(String(50))
    last_name=Column(String(50))
    email=Column(String(100),unique=True)    
    enrollment_year=Column(Integer)
    department_id=Column(Integer,ForeignKey("departments.department_id"))
    department=relationship("Department",back_populates="students")
    enrollments=relationship("Enrollment",back_populates="student")
    
class Enrollment(base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True)
    student_id = Column(
        Integer,
        ForeignKey("students.student_id")
    )
    course_id = Column(
        Integer,
        ForeignKey("courses.course_id")
    )
    grade = Column(String(2))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
class Course(base):
    __tablename__="courses"
    course_id=Column(Integer,primary_key=True)
    course_name=Column(String(50),nullable=False)
    department_id=Column(Integer,ForeignKey("departments.department_id"))
    department=relationship("Department",back_populates="courses")
    enrollments=relationship("Enrollment",back_populates="course")
class Professor(base):
    __tablename__ = "professors"

    professor_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    salary = Column(Numeric(10, 2))
    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship("Department", back_populates="professors")    
base.metadata.create_all(engine)    
# students=session.query(Student).all()
# departments=session.query(Department).all()
# for department in departments:
#     print(f'{department.department_name}')
#     for stu in department.students:
#         print(stu.first_name)
# for stu in students:
#     print(f'{stu.first_name} {stu.department.department_name}')   

