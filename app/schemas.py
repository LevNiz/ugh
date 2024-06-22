from pydantic import BaseModel
from typing import Optional

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
    middle_name: str = None
    last_name: str = None
    sex: str = None
    city: str = None
    phone: str = None
    email: str = None
    user_type: str = None
    whatsapp: str = None
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

# class User(UserBase):
#     id: int
#     first_name: str
#     last_name: str
#     role: str

class User(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    sex: Optional[str]
    city: Optional[str]
    phone: str
    email: Optional[str]
    pass_hash: Optional[str]
    temp_pass_hash: Optional[str]
    user_type: Optional[str]
    whatsapp: Optional[str]
    telegram: Optional[str]
    viber: Optional[str]
    zoom: Optional[str]
    prop_city: Optional[str]
    prop_offer: Optional[str]
    prop_type: Optional[str]
    prop_state: Optional[str]
    avatar: Optional[str]
    licenses: Optional[str]
    video: Optional[str]
    about: Optional[str]
    activation_code: Optional[str]
    role: Optional[str]
    updated: int

class UserActivate(BaseModel):
    phone: str
    activation_code: str

class TokenRequest(BaseModel):
    phone: str
    activation_code: str