from passlib.context import CryptContext
from typing import List
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


async def create_property(db, property: schemas.PropertyCreate, realtor_id: int):
    query = """
    INSERT INTO properties (realtor_id, deal_format, type, subtype, condition, entry_year, entry_quarter, purpose, location, price, currency, title, description, images, floor, total_area, living_area, ceiling_height, rooms, bedrooms, bathrooms, features, equipment, layout, building_floors, building_living_area, apartments, lifts_per_entrance, building_features, building_name, developer, materials, building_layout, territory_area, territory_features, territory_layout, nearby_places, views, video_title, video_url, services, commission_amount, commission_type, documents, document_file1, document_file2, document_file3, status, created_at)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45, $46, $47, $48, $49)
    RETURNING id
    """
    values = (
        realtor_id, property.deal_format, property.type, property.subtype, property.condition, property.entry_year, property.entry_quarter, property.purpose, property.location, property.price, property.currency, property.title, property.description, property.images, property.floor, property.total_area, property.living_area, property.ceiling_height, property.rooms, property.bedrooms, property.bathrooms, property.features, property.equipment, property.layout, property.building_floors, property.building_living_area, property.apartments, property.lifts_per_entrance, property.building_features, property.building_name, property.developer, property.materials, property.building_layout, property.territory_area, property.territory_features, property.territory_layout, property.nearby_places, property.views, property.video_title, property.video_url, property.services, property.commission_amount, property.commission_type, property.documents, property.document_file1, property.document_file2, property.document_file3, property.status, int(time.time())
    )
    new_property = await db.fetchrow(query, *values)
    return dict(new_property)


async def get_properties_by_user(db, user_id: int) -> List[schemas.Property]:
    query = "SELECT * FROM properties WHERE realtor_id = $1"
    rows = await db.fetch(query, user_id)
    return [dict(row) for row in rows]