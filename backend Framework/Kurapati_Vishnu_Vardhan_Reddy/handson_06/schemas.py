from pydantic import BaseModel, ConfigDict
from typing import Optional,List
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