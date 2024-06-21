from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    phone: str

class UserCreate(UserBase):
    name: str
    role: str

class UserUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    middlet_name: str = None
    sex: str = None
    city: str = None
    phone: str = None
    email: str = None
    user_type: str = None
    watsapp: str = None
    telegram: str = None
    viber: str = None
    zoom: str = None
    prop_city: str = None
    prop_offer: str = None
    prop_type: str = None
    prop_state: str = None
    avatar: str = None
    licenses: str = None
    video: str = None
    about: str = None

class UserAuth(UserBase):
    password: str

class User(UserBase):
    id: int
    first_name: str
    last_name: str
    role: str

    class Config:
        orm_mode = True

class UserActivate(BaseModel):
    phone: str
    activation_code: str
