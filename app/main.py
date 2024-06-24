from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.database import database
from app.routes import users, properties

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(properties.router, prefix="/properties", tags=["properties"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup():
    await database.connect()
    await database.drop_tables()  # Инициализация базы данных
    await database.init_db()  # Инициализация базы данных

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

