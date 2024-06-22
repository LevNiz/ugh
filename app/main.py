from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import random
import string
import os
import shutil

from app import schemas, crud, deps
from app.database import database
from app.sms_module import send_sms

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup():
    await database.connect()
    await database.init_db()  # Инициализация базы данных

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

def generate_activation_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

@app.post("/register/")
async def create_user(user: schemas.UserCreate, db = Depends(deps.get_db)):
    db_user = await crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    activation_code = generate_activation_code()
    new_user = await crud.create_user(db, user, activation_code)
    await send_sms(new_user['phone'], f"Your activation code is: {activation_code}")
    return {"message": "User created successfully", 'code': activation_code}

@app.post("/activate/")
async def activate_user(data: schemas.UserActivate, db = Depends(deps.get_db)):
    db_user = await crud.get_user_by_phone(db, phone=data.phone)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    if db_user['activation_code'] != data.activation_code:
        raise HTTPException(status_code=400, detail="Invalid activation code")
    await db.execute("UPDATE users SET activation_code = $1 WHERE phone = $2", data.activation_code, data.phone)
    return {"message": "User activated successfully"}

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(data: schemas.TokenRequest, db = Depends(deps.get_db)):
    print("data", data)
    user = await crud.get_user_by_phone(db, phone=data.phone)
    print(user)

    if not user or user['activation_code'] != data.activation_code:
        raise HTTPException(
            status_code=400,
            detail="Incorrect phone number or activation code",
        )
    access_token = deps.create_access_token(data={"sub": user['phone']})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
async def read_users_me(current_user: schemas.User = Depends(deps.get_current_user)):
    return current_user

@app.put("/update/")
async def update_user(
    phone: str = Form(...),
    first_name: str = Form(None),
    last_name: str = Form(None),
    middle_name: str = Form(None),
    sex: str = Form(None),
    city: str = Form(None),
    email: str = Form(None),
    user_type: str = Form(None),
    whatsapp: str = Form(None),
    telegram: str = Form(None),
    viber: str = Form(None),
    zoom: str = Form(None),
    prop_city: str = Form(None),
    prop_offer: str = Form(None),
    prop_type: str = Form(None),
    prop_state: str = Form(None),
    about: str = Form(None),
    avatar: UploadFile = File(None),
    licenses: UploadFile = File(None),
    db = Depends(deps.get_db)
):
    db_user = await crud.get_user_by_phone(db, phone=phone)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    user_update_data = {
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "sex": sex,
        "city": city,
        "email": email,
        "user_type": user_type,
        "whatsapp": whatsapp,
        "telegram": telegram,
        "viber": viber,
        "zoom": zoom,
        "prop_city": prop_city,
        "prop_offer": prop_offer,
        "prop_type": prop_type,
        "prop_state": prop_state,
        "about": about,
    }

    # Remove keys with None values
    user_update_data = {k: v for k, v in user_update_data.items() if v is not None}

    user_update = schemas.UserUpdate(**user_update_data)
    print("user udpate", user_update)
    if avatar:
        avatar_location = os.path.join(UPLOAD_DIR, avatar.filename)
        with open(avatar_location, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        user_update.avatar = avatar_location
    
    if licenses:
        license_location = os.path.join(UPLOAD_DIR, licenses.filename)
        with open(license_location, "wb") as buffer:
            shutil.copyfileobj(licenses.file, buffer)
        user_update.licenses = license_location  

    print(user_update, type(user_update))
    updated_user = await crud.update_user(db, db_user['id'], user_update)
    return {"message": "User updated successfully", "user": dict(updated_user)}


@app.post("/reset/")
async def reset_activation_code(data: schemas.UserBase, db = Depends(deps.get_db)):
    db_user = await crud.get_user_by_phone(db, phone=data.phone)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    new_activation_code = generate_activation_code()
    await db.execute("UPDATE users SET activation_code = $1 WHERE phone = $2", new_activation_code, data.phone)
    await send_sms(db_user['phone'], f"Your new activation code is: {new_activation_code}")
    return {"message": "New activation code set"}

@app.delete("/delete/")
async def delete_user(data: schemas.UserBase, db = Depends(deps.get_db)):
    db_user = await crud.get_user_by_phone(db, phone=data.phone)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    await db.execute("DELETE FROM users WHERE phone = $1", data.phone)
    return {"message": "User deleted successfully"}

@app.get("/users/")
async def get_users(skip: int = 0, limit: int = 10, db = Depends(deps.get_db)):
    users = await db.fetch("SELECT * FROM users OFFSET $1 LIMIT $2", skip, limit)
    return users
