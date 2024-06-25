from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.database import database
from app import models, crud
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_db():  
    conn = await database.pool.acquire()
    try:
        yield conn
    finally:
        await database.pool.release(conn)

# async def get_user_by_phone(db, phone: str):
#     query = "SELECT * FROM users WHERE phone = $1"
#     user = await db.fetchrow(query, phone)
#     return user        

async def get_user_by_phone(db, phone: str):
    query = "SELECT * FROM users WHERE phone = $1"
    user = await db.fetchrow(query, phone)
    if user:
        return dict(user)
    return None

def create_access_token(data: dict):
    print("data in create token:", data)
    try:
        to_encode = data.copy()
        print(to_encode, type(to_encode))
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt        
    except Exception as e:
        print(e)

# async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         phone: str = payload.get("sub")
#         if phone is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = await get_user_by_phone(db, phone=phone)
#     if user is None:
#         raise credentials_exception
#     return user

async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWTError: {e}")
        raise credentials_exception
    user = await crud.get_user_by_phone(db, phone=phone)
    if user is None:
        raise credentials_exception
    
    
    return dict(user)
