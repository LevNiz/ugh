from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
import random
import string
import time
import os
import shutil

from app import schemas, crud, deps
from app.config import settings
from app.database import database
from app.middleware import auth_middleware
from app.sms_module import send_sms

app = FastAPI()
app.middleware("http")(auth_middleware)

UPLOAD_DIR = "uploads/"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

def generate_random_password(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(deps.get_db)):
    user = await crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect phone number or password",
        )
    access_token = deps.create_access_token(data={"sub": user['phone']})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register/")
async def create_user(user: schemas.UserCreate, db = Depends(deps.get_db)):
    db_user = await crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    password = generate_random_password()
    hashed_password = deps.get_password_hash(password)
    activation_code = str(random.randint(1000, 9999))
    new_user = await crud.create_user(db, user, hashed_password, activation_code)
    await send_sms(new_user['phone'], f"Your activation code is: {activation_code}")
    return {"message": "User created successfully"}

@app.post("/activate/")
async def activate_user(data: schemas.UserActivate, db = Depends(deps.get_db)):
    db_user = await crud.get_user_by_phone(db, phone=data.phone)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    if db_user['activation_code'] != data.activation_code:
        raise HTTPException(status_code=400, detail="Invalid activation code")
    await db.execute("UPDATE users SET activation_code = 'active' WHERE phone = $1", data.phone)
    return {"message": "User activated successfully"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(deps.get_current_user)):
    return current_user

@app.put("/update/")
async def update_user(
    phone: str,
    user_update: schemas.UserUpdate,
    db = Depends(deps.get_db),
    avatar: UploadFile = File(None),
    license: UploadFile = File(None)
):
    db_user = await crud.get_user_by_phone(db, phone=phone)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if avatar:
        avatar_location = os.path.join(UPLOAD_DIR, avatar.filename)
        with open(avatar_location, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        user_update.avatar = avatar_location
    
    if license:
        license_location = os.path.join(UPLOAD_DIR, license.filename)
        with open(license_location, "wb") as buffer:
            shutil.copyfileobj(license.file, buffer)
        user_update.licenses = license_location  

    updated_user = await crud.update_user(db, db_user['id'], user_update)
    return {"message": "User updated successfully", "user": dict(updated_user)}

@app.post("/reset/")
async def reset_password(phone: str, db = Depends(deps.get_db)):
    db_user = await crud.get_user_by_phone(db, phone=phone)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    new_pass = str(random.randint(1000, 9999))
    hashed_password = deps.get_password_hash(new_pass)
    await db.execute("UPDATE users SET temp_pass_hash = $1 WHERE phone = $2", hashed_password, phone)
    await send_sms(db_user['phone'], f"Your temporary password is: {new_pass}")
    return {"message": "Temporary password set"}

@app.delete("/delete/")
async def delete_user(phone: str, db = Depends(deps.get_db)):
    db_user = await crud.get_user_by_phone(db, phone=phone)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    await db.execute("DELETE FROM users WHERE phone = $1", phone)
    return {"message": "User deleted successfully"}

@app.get("/users/")
async def get_users(skip: int = 0, limit: int = 10, db = Depends(deps.get_db)):
    users = await db.fetch("SELECT * FROM users OFFSET $1 LIMIT $2", skip, limit)
    return users
