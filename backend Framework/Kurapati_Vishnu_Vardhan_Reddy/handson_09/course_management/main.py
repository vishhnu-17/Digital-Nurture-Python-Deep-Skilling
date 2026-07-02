from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, engine
from models import Base, Course, Student, Enrollment, User
from schemas import CourseCreate, CourseUpdate, CourseResponse, StudentCreate, StudentUpdate, StudentResponse, EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate, UserCreate, UserResponse, Token, UserLogin, TokenData

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from security import get_password_hash, verify_password
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "your_secret_key_here_change_this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 Authorization Code Flow:
# The user is redirected to an authorization server to log in.
# After successful authentication, the authorization server returns an authorization code.
# The client exchanges the authorization code for an access token.
#
# In this project, we use a simpler JWT login flow.
# The user sends email and password directly to the login endpoint.
# After successful authentication, the server immediately returns a JWT access token.

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/"
)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

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
    db: AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user)
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
    db: AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user)
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

@app.post(
    "/api/v1/auth/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@app.post(
    "/api/v1/auth/login/",
    response_model=Token
)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )

    db_user = result.scalar_one_or_none()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }