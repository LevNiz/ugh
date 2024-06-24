from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from app import schemas, crud, deps

import shutil

router = APIRouter()

@router.post("/create")
async def create_property(
    deal_format: str = Form(...),
    type: str = Form(...),
    subtype: str = Form(...),
    condition: str = Form(...),
    entry_year: int = Form(...),
    entry_quarter: int = Form(...),
    purpose: str = Form(...),
    location: str = Form(...),
    price: float = Form(...),
    currency: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    images: List[UploadFile] = File(None),
    floor: Optional[int] = Form(None),
    total_area: Optional[float] = Form(None),
    living_area: Optional[float] = Form(None),
    ceiling_height: Optional[float] = Form(None),
    rooms: Optional[int] = Form(None),
    bedrooms: Optional[int] = Form(None),
    bathrooms: Optional[int] = Form(None),
    features: Optional[str] = Form(None),
    equipment: Optional[str] = Form(None),
    layout: Optional[UploadFile] = File(None),
    building_floors: Optional[int] = Form(None),
    building_living_area: Optional[float] = Form(None),
    apartments: Optional[int] = Form(None),
    lifts_per_entrance: Optional[int] = Form(None),
    building_features: Optional[str] = Form(None),
    building_name: Optional[str] = Form(None),
    developer: Optional[str] = Form(None),
    materials: Optional[str] = Form(None),
    building_layout: Optional[UploadFile] = File(None),
    territory_area: Optional[float] = Form(None),
    territory_features: Optional[str] = Form(None),
    territory_layout: Optional[UploadFile] = File(None),
    nearby_places: Optional[str] = Form(None),
    views: Optional[str] = Form(None),
    video_title: Optional[str] = Form(None),
    video_url: Optional[str] = Form(None),
    services: Optional[str] = Form(None),
    commission_amount: Optional[float] = Form(None),
    commission_type: Optional[str] = Form(None),
    documents: Optional[str] = Form(None),
    document_file1: Optional[UploadFile] = File(None),
    document_file2: Optional[UploadFile] = File(None),
    document_file3: Optional[UploadFile] = File(None),
    current_user: schemas.User = Depends(deps.get_current_user),
    db=Depends(deps.get_db)
):
    print("in prop", current_user)
    if current_user['role'] not in ['realtor', 'agency', 'developer']:
        raise HTTPException(status_code=403, detail="Only realtors can create properties")
    
    images_path = []
    print(images)
    for image in images:
        image_path = f"uploads/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        images_path.append(image_path)

    print("imgs", images_path)

    layout_path = None
    if layout:
        layout_path = f"uploads/{layout.filename}"
        with open(layout_path, "wb") as buffer:
            shutil.copyfileobj(layout.file, buffer)

    building_layout_path = None
    if building_layout:
        building_layout_path = f"uploads/{building_layout.filename}"
        with open(building_layout_path, "wb") as buffer:
            shutil.copyfileobj(building_layout.file, buffer)

    territory_layout_path = None
    if territory_layout:
        territory_layout_path = f"uploads/{territory_layout.filename}"
        with open(territory_layout_path, "wb") as buffer:
            shutil.copyfileobj(territory_layout.file, buffer)

    document_file1_path = None
    if document_file1:
        document_file1_path = f"uploads/{document_file1.filename}"
        with open(document_file1_path, "wb") as buffer:
            shutil.copyfileobj(document_file1.file, buffer)

    document_file2_path = None
    if document_file2:
        document_file2_path = f"uploads/{document_file2.filename}"
        with open(document_file2_path, "wb") as buffer:
            shutil.copyfileobj(document_file2.file, buffer)

    document_file3_path = None
    if document_file3:
        document_file3_path = f"uploads/{document_file3.filename}"
        with open(document_file3_path, "wb") as buffer:
            shutil.copyfileobj(document_file3.file, buffer)

    # Split comma-separated strings into lists
    features_list = features.split(",") if features else []
    equipment_list = equipment.split(",") if equipment else []
    building_features_list = building_features.split(",") if building_features else []
    territory_features_list = territory_features.split(",") if territory_features else []
    nearby_places_list = nearby_places.split(",") if nearby_places else []
    views_list = views.split(",") if views else []
    services_list = services.split(",") if services else []
    documents_list = documents.split(",") if documents else []

    property_data = schemas.PropertyCreate(
        deal_format=deal_format,
        type=type,
        subtype=subtype,
        condition=condition,
        entry_year=entry_year,
        entry_quarter=entry_quarter,
        purpose=purpose,
        location=location,
        price=price,
        currency=currency,
        title=title,
        description=description,
        images=images_path,
        floor=floor,
        total_area=total_area,
        living_area=living_area,
        ceiling_height=ceiling_height,
        rooms=rooms,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        features=features_list,
        equipment=equipment_list,
        layout=layout_path,
        building_floors=building_floors,
        building_living_area=building_living_area,
        apartments=apartments,
        lifts_per_entrance=lifts_per_entrance,
        building_features=building_features_list,
        building_name=building_name,
        developer=developer,
        materials=materials,
        building_layout=building_layout_path,
        territory_area=territory_area,
        territory_features=territory_features_list,
        territory_layout=territory_layout_path,
        nearby_places=nearby_places_list,
        views=views_list,
        video_title=video_title,
        video_url=video_url,
        services=services_list,
        commission_amount=commission_amount,
        commission_type=commission_type,
        documents=documents_list,
        document_file1=document_file1_path,
        document_file2=document_file2_path,
        document_file3=document_file3_path,
        status='moderated'
    )

    new_property = await crud.create_property(db, property_data, current_user['id'])
    return new_property


@router.get("/my_properties/", response_model=List[schemas.Property])
async def get_my_properties(current_user: dict = Depends(deps.get_current_user), db=Depends(deps.get_db)):
    if current_user['role'] not in ['realtor', 'agency', 'developer']:
        raise HTTPException(status_code=403, detail="Only realtors can view their properties")
    
    properties = await crud.get_properties_by_user(db, current_user['id'])
    return properties