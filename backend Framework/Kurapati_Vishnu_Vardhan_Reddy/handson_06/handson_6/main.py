from typing import Optional

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, engine
from models import Base, Course
from schemas import CourseCreate, CourseUpdate

app = FastAPI(
    title="Course Management API",
    version="1.0"
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def home():
    return {
        "message": "API running"
    }


@app.post("/api/courses/")
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


@app.get("/api/courses/")
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


@app.get("/api/courses/{course_id}")
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if course is None:
        return {
            "message": "Course not found"
        }

    return {
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits,
        "department_id": course.department_id
    }

@app.put("/api/courses/{course_id}")
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
        return {
            "message": "Course not found"
        }

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

@app.delete("/api/courses/{course_id}")
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if course is None:
        return {
            "message": "Course not found"
        }

    await db.delete(course)
    await db.commit()

    return {
        "message": "Course deleted successfully"
    }