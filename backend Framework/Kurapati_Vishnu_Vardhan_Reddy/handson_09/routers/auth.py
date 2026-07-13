from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from database import get_db
from models import User
from schemas import UserRegistration,UserResponse,UserLogin
from security import get_password_hash, verify_password_hash,create_access_token
router=APIRouter(prefix="/api/v1/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register_user(user:UserRegistration,db:AsyncSession=Depends(get_db)):
    statement=select(User).where(user.email==User.email)
    result= await db.execute(statement)
    existing_user=result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered")
    hashed_password=get_password_hash(user.password)
    new_user=User(email=user.email,hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(form_data:OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_db)):
    statement=select(User).where(User.email==form_data.username)
    result=await db.execute(statement)
    db_user=result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not verify_password_hash(form_data.password,db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="invalid username or password")
    access_token=create_access_token({"sub":db_user.email})
    return({"access_token": access_token,"token_type":"bearer"})
    