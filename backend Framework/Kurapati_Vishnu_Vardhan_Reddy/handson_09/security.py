from passlib.context import CryptContext
from jose import jwt,JWTError
from models import User
from sqlalchemy import select
from fastapi import Depends, status,HTTPException
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
# bcrypt is preferred over MD5 or SHA-256 for password storage because
# it is intentionally slow and automatically uses a unique salt for every
# password. This makes brute-force and rainbow table attacks much harder.
# MD5 and SHA-256 are designed to be fast hashing algorithms and are not
# suitable for securely storing passwords.
# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )
pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")
SECRET_KEY="vishnu1234"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password_hash(plain_pswrd,hashed_pswrd):
    return pwd_context.verify(plain_pswrd,hashed_pswrd)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:str=Depends(oauth2_scheme),db:AsyncSession=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials")
        statement=select(User).where(User.email==email,User.is_active==True)
        result= await db.execute(statement)
        db_user=result.scalar_one_or_none()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials")
        return db_user
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials jwterror")
        
    

