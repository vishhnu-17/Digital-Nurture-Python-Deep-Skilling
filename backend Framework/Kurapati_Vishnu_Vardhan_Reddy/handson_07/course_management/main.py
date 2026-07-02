from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, engine
from models import Base, Course, Student, Enrollment
from schemas import CourseCreate, CourseUpdate, CourseResponse, StudentCreate, StudentUpdate, StudentResponse, EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Course Management API",
    description="A RESTful API for managing courses, students, and enrollments using FastAPI.",
    version="1.0",
    contact={
        "name": "Vishal",
        "email": "vishal@example.com"
    },
    lifespan=lifespan
)

def send_confirmation_email(student_email : str):
    print (f"Sending Confirmation Email to {student_email}")

@app.get("/")
async def home():
    return {
        "message": "API running"
    }


@app.post("/api/courses/", tags=['Courses'],
response_model = CourseResponse,
status_code=status.HTTP_201_CREATED,
summary = "Create a new course",
response_description = "The newly created course")

async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):
    new_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )

    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    return {
        "id": new_course.id,
        "name": new_course.name,
        "code": new_course.code,
        "credits": new_course.credits,
        "department_id": new_course.department_id
    }


@app.get("/api/courses/",tags=['Courses'])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Course)

    if department_id is not None:
        query = query.where(Course.department_id == department_id)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    courses = result.scalars().all()

    return [
        {
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "credits": course.credits,
            "department_id": course.department_id
        }
        for course in courses
    ]


@app.get("/api/courses/{course_id}",tags=['Courses'],
response_model = CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code = 404,
            detail = "Course Not Found"
        )

    return {
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits,
        "department_id": course.department_id
    }

@app.put("/api/courses/{course_id}",tags=['Courses'])
async def update_course(
    course_id: int,
    updated_course: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code = 404,
            detail = "Course Not Found"
        )

    if updated_course.name is not None:
        course.name = updated_course.name

    if updated_course.code is not None:
        course.code = updated_course.code

    if updated_course.credits is not None:
        course.credits = updated_course.credits

    if updated_course.department_id is not None:
        course.department_id = updated_course.department_id

    await db.commit()
    await db.refresh(course)

    return {
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits,
        "department_id": course.department_id
    }

@app.delete("/api/courses/{course_id}",tags=['Courses'],
status_code=status.HTTP_204_NO_CONTENT)

async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code = 404,
            detail = "Course Not Found"
        )

    await db.delete(course)
    await db.commit()

    
@app.post(
    "/api/students/",tags=['Students'],
    response_model = StudentResponse,
    status_code = status.HTTP_201_CREATED
)
async def create_student(
    student : StudentCreate,
    db : AsyncSession = Depends(get_db)
):
   new_student = Student(
    first_name = student.first_name,
    last_name = student.last_name,
    email = student.email
   )

   db.add(new_student)
   await db.commit()
   await db.refresh(new_student)
   return new_student


@app.get(
    "/api/students/",tags=['Students'],
    response_model = list[StudentResponse]
)
async def get_students(
    db : AsyncSession = Depends(get_db)
):
   result = await db.execute(select(Student))
   students = result.scalars().all()
   return students

@app.get("/api/students/{student_id}",tags=['Students'],
response_model = StudentResponse)
async def get_student(
    student_id : int,
    db : AsyncSession = Depends(get_db)
):
  result = await db.execute(
    select(Student).where(Student.id == student_id)
  )

  student = result.scalar_one_or_none()

  if student is None:
    raise HTTPException(
        status_code = 404,
        detail = "Student Not Found"
    )

  return student

@app.put("/api/students/{student_id}",tags=['Students'],
response_model = StudentResponse)
async def update_student(
    student_id : int,
    updated_student : StudentUpdate,
    db : AsyncSession = Depends(get_db)
):
  result = await db.execute(
    select(Student).where(Student.id == student_id)
  )

  student = result.scalar_one_or_none()

  if student is None:
    raise HTTPException(
        status_code = 404,
        detail = "Student Not Found"
    )

  if updated_student.first_name is not None:
    student.first_name = updated_student.first_name

  if updated_student.last_name is not None:
    student.last_name = updated_student.last_name

  if updated_student.email is not None:
    student.email = updated_student.email

  await db.commit()
  await db.refresh(student)

  return student

@app.delete("/api/students/{student_id}",tags=['Students'],
status_code = status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id : int,
    db: AsyncSession = Depends(get_db)
):
   
   result = await db.execute(
    select(Student).where(Student.id == student_id)
   )
   student = result.scalar_one_or_none()
   if student is None:
     raise HTTPException(
        status_code = 404,
        detail = "Student not found"
     )

   await db.delete(student)
   await db.commit()

@app.post("/api/enrollments",tags=['Enrollments'],
response_model = EnrollmentResponse,
status_code = status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment : EnrollmentCreate,
    background_tasks : BackgroundTasks,
    db : AsyncSession = Depends(get_db)

):

  new_enrollment = Enrollment(
    student_id = enrollment.student_id,
    course_id = enrollment.course_id
  )

  db.add(new_enrollment)

  await db.commit()
  await db.refresh(new_enrollment)

  background_tasks.add_task(
    send_confirmation_email,
    "student@example.com"
  )

  return new_enrollment

@app.get(
    "/api/enrollments/",
    tags=["Enrollments"],
    response_model=list[EnrollmentResponse]
)
async def get_enrollments(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Enrollment)
    )

    enrollments = result.scalars().all()

    return enrollments

@app.get(
    "/api/enrollments/{enrollment_id}",
    tags=["Enrollments"],
    response_model=EnrollmentResponse
)
async def get_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return enrollment


@app.put(
    "/api/enrollments/{enrollment_id}",
    tags=["Enrollments"],
    response_model=EnrollmentResponse
)
async def update_enrollment(
    enrollment_id: int,
    updated_enrollment: EnrollmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    if updated_enrollment.student_id is not None:
        enrollment.student_id = updated_enrollment.student_id

    if updated_enrollment.course_id is not None:
        enrollment.course_id = updated_enrollment.course_id

    await db.commit()
    await db.refresh(enrollment)

    return enrollment

@app.delete(
    "/api/enrollments/{enrollment_id}",
    tags=["Enrollments"],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    await db.delete(enrollment)
    await db.commit()

@app.get(
    "/api/courses/{course_id}/students/",
    tags=["Courses"],
    response_model=list[StudentResponse]
)
async def get_course_students(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Student)
        .join(Enrollment)
        .where(Enrollment.course_id == course_id)
    )

    students = result.scalars().all()

    return students