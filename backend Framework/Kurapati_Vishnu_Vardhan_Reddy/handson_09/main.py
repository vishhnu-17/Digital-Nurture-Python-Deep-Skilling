from fastapi import FastAPI, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy import select
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from security import get_current_user
from database import get_db, init_db
from models import *
from schemas import *
from routers.auth import router as auth_router


app=FastAPI(title="Course Management API", version="1.0", description="A REST API for managing departments, courses, students and enrollments.",
            contact={"name":"vishnu","email":"vishnu@gmail.com"}
)

app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:3000"],
                   allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth_router)
@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/",summary="Home endpoint",response_description="API status message")
async def home():
    return {
        "message":"API RUNNING"
    }


# -------------------- COURSE CRUD --------------------

@app.post("/api/courses",response_model=CourseResponse,status_code=status.HTTP_201_CREATED,tags=[
    'Courses'],summary="Create a new course",response_description="The created course")

async def create_course(course:CreateCourse,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    new_course=Course(name=course.name,code=course.code,credits=course.credits,dept_id=course.dept_id)
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

@app.get("/api/courses/{id}/",response_model=CourseResponse,tags=['Courses'],summary="Get a course by ID",response_description="The requested course")
async def get_course(id:int,db:AsyncSession=Depends(get_db)):
    statement=select(Course).where(Course.id==id)
    result=await db.execute(statement)
    course=result.scalars().first()
    return course

@app.put("/api/courses/{id}/",response_model=CourseResponse,tags=['Courses'],summary="Update a course",response_description="The updated course")
async def update_course(id:int,new_course:CourseUpdate,db:AsyncSession=Depends(get_db)):
    statement=select(Course).where(Course.id==id)
    res=await db.execute(statement)
    course=res.scalar_one_or_none()
    if(course) is None:
        raise HTTPException(status_code=404,detail="Course not found")
    if(new_course.name):
        course.name=new_course.name
    if(new_course.code):
        course.code=new_course.code
    if new_course.credits:
        course.credits=new_course.credits
    if new_course.department_id:
        course.dept_id=new_course.department_id
    await db.commit()
    await db.refresh(course)
    return course

@app.delete("/api/courses/{id}/",status_code=status.HTTP_204_NO_CONTENT,tags=['Courses'],summary="Delete a course",response_description="Course deleted successfully")
async def delete(id:int,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    statement=select(Course).where(Course.id==id)
    result=await db.execute(statement)
    course=result.scalar_one_or_none()
    if(course) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(course)
    await db.commit()

@app.get("/api/courses/",response_model=list[CourseResponse],tags=['Courses'],summary="Get all courses",response_description="List of courses")
async def get_courses(skip:int=0,limit:int=10,department_id:int|None=None,db:AsyncSession=Depends(get_db)):
    statement=select(Course).offset(skip).limit(limit)
    if(department_id):
        statement=statement.where(Course.dept_id==department_id)
    result=await db.execute(statement)
    courses=result.scalars().all()
    return courses


# -------------------- STUDENT CRUD --------------------

@app.post("/api/students/",response_model=StudentResponse,status_code=status.HTTP_201_CREATED,tags=['Student'],summary="Create a new student",response_description="The created student")
async def create_students(student:CreateStudent,db:AsyncSession=Depends(get_db)):
    new_stu=Student(first_name=student.first_name,last_name=student.last_name,email=student.email,dept_id=student.dept_id,year=student.year)
    db.add(new_stu)
    await db.commit()
    await db.refresh(new_stu)
    return new_stu

@app.get("/api/students/{id}/",response_model=StudentResponse,tags=['Student'],summary="Get a student by ID",response_description="The requested student")
async def get_student_by_id(id:int,db:AsyncSession=Depends(get_db)):
    statement=select(Student).where(Student.id==id)
    result=await db.execute(statement)
    student=result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404,detail="Student not found")
    return student

@app.put("/api/students/{id}/",response_model=StudentResponse,tags=['Student'],summary="Update a student",response_description="The updated student")
async def update_student(id:int,new_stu:StudentUpdate,db:AsyncSession=Depends(get_db)):
    statement=select(Student).where(Student.id==id)
    res=await db.execute(statement)
    stu=res.scalar_one_or_none()
    if(stu) is None:
        raise HTTPException(status_code=404,detail="Student not found")
    if new_stu.first_name is not None:
        stu.first_name=new_stu.first_name
    if new_stu.last_name is not None:
        stu.last_name=new_stu.last_name
    if new_stu.email is not None:
        stu.email=new_stu.email
    if new_stu.dept_id is not None:
        stu.dept_id=new_stu.dept_id
    if new_stu.year is not None:
        stu.year=new_stu.year
    await db.commit()
    await db.refresh(stu)
    return stu

@app.delete("/api/students/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=['Student'],summary="Delete a student",response_description="Student deleted successfully")
async def delete_student(id:int,db:AsyncSession=Depends(get_db)):
    statement=select(Student).where(Student.id==id)
    result=await db.execute(statement)
    stu=result.scalars().first()
    if stu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="student not found")
    await db.delete(stu)
    await db.commit()

@app.get("/api/students/",response_model=list[StudentResponse],status_code=status.HTTP_200_OK,tags=['Student'],summary="Get all students",response_description="List of students")
async def get_students(skip:int=0,limit:int=10,department_id:int|None=None,db:AsyncSession=Depends(get_db)):
    statement=select(Student).limit(limit).offset(skip)
    if(department_id) is not None:
        statement=statement.where(Student.dept_id==department_id)
    result=await db.execute(statement)
    students=result.scalars().all()
    return students

# -------------------- ENROLLMENT CRUD --------------------

@app.post("/api/enrollments/",response_model=EnrollmentResponse,status_code=status.HTTP_201_CREATED,tags=['Enrollement'],summary="Create a new enrollment",response_description="The created enrollment")
async def create_enrollment(enrollment:EnrollmentCreate,background_tasks:BackgroundTasks,db:AsyncSession=Depends(get_db)):
    new_enrollment=Enrollment(student_id=enrollment.student_id,course_id=enrollment.course_id,enrollment_date=enrollment.enrollment_date,grade=enrollment.grade)
    db.add(new_enrollment)
    await db.commit()
    statement=select(Student).where(Student.id==new_enrollment.student_id)
    result = await db.execute(statement)
    student=result.scalars().first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    background_tasks.add_task(send_confirmation_email,student.email)
    await db.refresh(new_enrollment)
    return new_enrollment

@app.get("/api/enrollments/{id}/",response_model=EnrollmentResponse,tags=['Enrollement'],summary="Get an enrollment by ID",response_description="The requested enrollment")
async def get_enrollment(id:int,db:AsyncSession=Depends(get_db)):
    statement=select(Enrollment).where(Enrollment.id==id)
    result=await db.execute(statement)
    enrollment=result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Enrollment not found")
    return enrollment

@app.put("/api/enrollments/{id}/",response_model=EnrollmentResponse,tags=['Enrollement'],summary="Update an enrollment",response_description="The updated enrollment")
async def update_enrollment(id:int,new_enrollment:EnrollmentUpdate,db:AsyncSession=Depends(get_db)):
    statement=select(Enrollment).where(Enrollment.id==id)
    result=await db.execute(statement)
    enrollment=result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Enrollment not found")
    if new_enrollment.student_id is not None:
        enrollment.student_id=new_enrollment.student_id
    if new_enrollment.course_id is not None:
        enrollment.course_id=new_enrollment.course_id
    if new_enrollment.enrollment_date is not None:
        enrollment.enrollment_date=new_enrollment.enrollment_date
    if new_enrollment.grade is not None:
        enrollment.grade=new_enrollment.grade
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

@app.delete("/api/enrollments/{id}/",status_code=status.HTTP_204_NO_CONTENT,tags=['Enrollement'],summary="Delete an enrollment",response_description="Enrollment deleted successfully")
async def delete_enrollment(id:int,db:AsyncSession=Depends(get_db)):
    statement=select(Enrollment).where(Enrollment.id==id)
    result=await db.execute(statement)
    enrollment=result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Enrollment not found")
    await db.delete(enrollment)
    await db.commit()

@app.get("/api/enrollments/",response_model=list[EnrollmentResponse],status_code=status.HTTP_200_OK,tags=['Enrollement'],summary="Get all enrollments",response_description="List of enrollments")
async def get_enrollments(db:AsyncSession=Depends(get_db)):
    statement=select(Enrollment)
    result=await db.execute(statement)
    enrollments=result.scalars().all()
    return enrollments


# -------------------- RELATIONSHIP ENDPOINT --------------------

@app.get("/api/courses/{id}/students/",response_model=list[StudentResponse],tags=['Student'],summary="Get students enrolled in a course",response_description="List of students enrolled in the course")
async def get_student_from_course(id:int,db:AsyncSession=Depends(get_db)):
    statement=select(Student).join(Enrollment).where(Enrollment.course_id==id)
    result=await db.execute(statement)
    students=result.scalars().all()
    return students

def send_confirmation_email(student_email:str):
    print("sending confirmation mail to ",student_email)