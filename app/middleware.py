from fastapi import FastAPI, Request, HTTPException
from jose import JWTError, jwt
from app.config import settings
from app.database import database

async def auth_middleware(request: Request, call_next):
    if request.method == 'OPTIONS':
        return await call_next(request)
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email = payload.get("sub")
        async with database.pool.acquire() as connection:
            user = await connection.fetchrow("SELECT * FROM users WHERE email = $1", user_email)
            if user and user['updated'] == payload.get("updated"):
                request.state.user = user
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
    except (JWTError, IndexError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    response = await call_next(request)
    return response
