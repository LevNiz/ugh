from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    phone: str

class UserCreate(UserBase):
    name: str
    role: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    sex: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[str] = None
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    viber: Optional[str] = None
    zoom: Optional[str] = None
    prop_city: Optional[str] = None
    prop_offer: Optional[str] = None
    prop_type: Optional[str] = None
    prop_state: Optional[str] = None
    about: Optional[str] = None
    avatar: Optional[str] = None
    licenses: Optional[str] = None
    notifications_all_messages: Optional[bool] = None
    notifications_new_matches: Optional[bool] = None
    notifications_responses: Optional[bool] = None
    notifications_contacts: Optional[bool] = None
    notifications_news: Optional[bool] = None

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
    notifications_all_messages: Optional[bool]
    notifications_new_matches: Optional[bool]
    notifications_responses: Optional[bool]
    notifications_contacts: Optional[bool]
    notifications_news: Optional[bool]

    class Config:
        orm_mode = True

class UserActivate(BaseModel):
    phone: str
    activation_code: str

class TokenRequest(BaseModel):
    phone: str
    activation_code: str


class PropertyBase(BaseModel):
    deal_format: str
    type: str
    subtype: str
    condition: str
    entry_year: int
    entry_quarter: int
    purpose: str
    location: str
    price: float
    currency: str
    title: str
    description: str
    images: Optional[List[str]] = []
    floor: Optional[int]
    total_area: Optional[float]
    living_area: Optional[float]
    ceiling_height: Optional[float]
    rooms: Optional[int]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    features: Optional[List[str]]
    equipment: Optional[List[str]]
    layout: Optional[str]
    building_floors: Optional[int]
    building_living_area: Optional[float]
    apartments: Optional[int]
    lifts_per_entrance: Optional[int]
    building_features: Optional[List[str]]
    building_name: Optional[str]
    developer: Optional[str]
    materials: Optional[str]
    building_layout: Optional[str]
    territory_area: Optional[float]
    territory_features: Optional[List[str]]
    territory_layout: Optional[str]
    nearby_places: Optional[List[str]]
    views: Optional[List[str]]
    video_title: Optional[str]
    video_url: Optional[str]
    services: Optional[List[str]]
    commission_amount: Optional[float]
    commission_type: Optional[str]
    documents: Optional[List[str]]
    document_file1: Optional[str]
    document_file2: Optional[str]
    document_file3: Optional[str]
    status: Optional[str]

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    realtor_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RequestCreate(BaseModel):
    city: str
    district: Optional[str]
    deal_format: str
    type: str
    subtype: Optional[str]
    condition: Optional[str]
    construction_year: Optional[int]
    construction_quarter: Optional[int]
    total_rooms: Optional[str]
    total_area_min: Optional[float]
    total_area_max: Optional[float]
    budget_min: Optional[float]
    budget_max: Optional[float]
    currency: Optional[str]
    purchase_purpose: Optional[str]
    urgency: Optional[str]
    purchase_method: Optional[str]
    mortgage_approved: Optional[bool]
    wishes: Optional[str]        



class ChatCreate(BaseModel):
    buyer_id: int
    seller_id: int
    property_id: int

class Chat(BaseModel):
    id: int
    buyer_id: int
    seller_id: int
    property_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    content: str

class Message(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True    