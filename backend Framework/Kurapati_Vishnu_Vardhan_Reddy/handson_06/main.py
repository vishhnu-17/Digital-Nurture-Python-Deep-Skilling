from fastapi import FastAPI,Depends
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import CreateCourse
from models import *
from sqlalchemy import select
from database import init_db
from schemas import *
app=FastAPI(title="Course Management API", version="1.0")
@app.on_event("startup")
async def startup():
    await init_db()
@app.get("/")
async def home():
    return {
        "message":"API RUNNING"
    }
@app.post("/api/courses")
async def create_course(course:CreateCourse,db:AsyncSession=Depends(get_db),status_code=201):
    new_course=Course(name=course.name,code=course.code,credits=course.credits,dept_id=course.dept_id)
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course
    return{ "message":"course created successfully",
         "course":course   }

@app.get("/api/courses/{id}/")
async def get_course(id:int,db:AsyncSession=Depends(get_db)):
    statement=select(Course).where(Course.id==id)
    result=await db.execute(statement)
    course=result.scalars().first()
    return course
    
@app.put("/api/courses/{id}/")
async def update_course(id:int,new_course:CourseUpdate,db:AsyncSession=Depends(get_db)):
    statement=select(Course).where(Course.id==id)
    res= await db.execute(statement)
    course= res.scalar_one_or_none()
    if(course) is None:
        return{ "message":"course not found"}
    if(new_course.name):
        course.name=new_course.name
    if(new_course.code):
        course.code=new_course.code
    if new_course.credits:
        course.credits= new_course.credits
    if new_course.department_id:
        course.dept_id=new_course.department_id
    await db.commit()
    await db.refresh(course)
    return course                

@app.delete("/api/courses/{id}/")
async def delete(id:int,db:AsyncSession=Depends(get_db)):
    statement=select(Course).where(Course.id==id)
    result=await db.execute(statement)
    course=result.scalar_one_or_none()
    if(course) is None:
        return {"message": "course to delete not found"}
    await db.delete(course)
    await db.commit()
    return {"message": "Course deleted successfully"}
    
             
@app.get("/api/courses/",response_model=list[CourseResponse])
async def get_courses(skip:int=0,limit:int=10,department_id:int|None=None, db:AsyncSession=Depends(get_db)):
    statement=select(Course).offset(skip).limit(limit)
    if(department_id):
        statement=statement.where(Course.dept_id==department_id)
    result=await db.execute(statement)    
    courses=result.scalars().all()
    return courses
    return{"skip":skip,"limit":limit,"department_id":department_id }
    

# db is a variable that receives the AsyncSession object yielded by get_db(). 
# Before the endpoint runs, FastAPI calls get_db(), creates a new session, and injects it into db. 
# The endpoint uses this session for database operations.
# After the endpoint finishes, control returns to get_db(), and the session is automatically closed. 

    