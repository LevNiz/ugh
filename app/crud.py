from passlib.context import CryptContext
from app import schemas

import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_phone(db, phone: str):
    query = "SELECT * FROM users WHERE phone = $1"
    user = await db.fetchrow(query, phone)
    return user

async def create_user(db, user: schemas.UserCreate, activation_code: str):
    query = """
        INSERT INTO users (phone, first_name, role, activation_code) 
        VALUES ($1, $2, $3, $4) 
        RETURNING id, phone, first_name, role
    """
    new_user = await db.fetchrow(query, user.phone, user.name, user.role, activation_code)
    return new_user

async def update_user(db, user_id: int, user_update: schemas.UserUpdate):
    user_update_dict = user_update.dict(exclude_unset=True)
    set_clause = ", ".join([f"{key} = ${idx + 1}" for idx, key in enumerate(user_update_dict.keys())])
    set_clause += f", updated = ${len(user_update_dict) + 1}"
    query = f"UPDATE users SET {set_clause} WHERE id = ${len(user_update_dict) + 2} RETURNING *"
    values = list(user_update_dict.values())
    values.append(int(time.time()))  # Add updated timestamp
    values.append(user_id)  # Add user_id
    updated_user = await db.fetchrow(query, *values)
    return updated_user

