from passlib.context import CryptContext
from app import schemas

import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_phone(db, phone: str):
    query = "SELECT * FROM users WHERE phone = $1"
    user = await db.fetchrow(query, phone)
    return user

async def create_user(db, user: schemas.UserCreate, hashed_password: str, activation_code: str):
    query = """
        INSERT INTO users (phone, pass_hash, first_name, role, activation_code) 
        VALUES ($1, $2, $3, $4, $5) 
        RETURNING id, phone, first_name, role
    """
    new_user = await db.fetchrow(query, user.phone, hashed_password, user.name, user.role, activation_code)
    return new_user

async def update_user(db, user_id: int, user_update: schemas.UserUpdate):
    set_clause = ", ".join([f"{key} = ${idx}" for idx, key in enumerate(user_update.dict().keys(), start=2)])
    query = f"UPDATE users SET {set_clause}, updated = $1 WHERE id = $2 RETURNING *"
    values = [user_update.dict().get(key) for key in user_update.dict().keys()]
    values.insert(0, int(time.time()))
    updated_user = await db.fetchrow(query, *values, user_id)
    return updated_user


async def authenticate_user(db, phone: str, password: str):
    user = await get_user_by_phone(db, phone)
    if not user:
        return False
    if not pwd_context.verify(password, user['pass_hash']):
        return False
    return user
