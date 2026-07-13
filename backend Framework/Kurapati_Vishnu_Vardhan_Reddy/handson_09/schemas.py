from pydantic import BaseModel, ConfigDict,EmailStr
from typing import Optional,List
from datetime import date
class CreateCourse(BaseModel):
    name:str
    code: str
    credits:int
    dept_id:int
class CourseUpdate(BaseModel):
    name:Optional[str]=None
    code :Optional[str]=None
    credits: Optional[int]=None
    department_id:Optional[int]=None    

class CourseResponse(BaseModel):
    id:int
    name:str
    code:str
    credits:int
    dept_id:int    

class DepartmentResponse(BaseModel):
    id:int
    name:str
    hod:str
    budget:float
    courses:List[CourseResponse]=[]   

class CreateStudent(BaseModel):
    first_name:str
    last_name:str
    year:int
    email:str
    dept_id:int

class StudentUpdate(BaseModel):
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    email: Optional[str]=None
    year:Optional[int]=None
    dept_id: Optional[int] = None       

class StudentResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str
    year:int
    dept_id:int    


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    grade: str | None = None


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: date
    grade: str | None = None

    class Config:
        from_attributes = True


class EnrollmentUpdate(BaseModel):
    student_id: int | None = None
    course_id: int | None = None
    enrollment_date: date | None = None
    grade: str | None = None  

class UserRegistration(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr  
    is_active:bool       

class UserLogin(BaseModel):
    email:EmailStr
    password: str
    