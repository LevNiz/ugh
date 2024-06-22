from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    middlet_name = Column(String(100))
    sex = Column(String(1))
    city = Column(String(100))
    phone = Column(String(15))
    email = Column(String(100), unique=True, index=True)
    pass_hash = Column(String(100))
    temp_pass_hash = Column(String(100), nullable=True)
    user_type = Column(String(100))
    watsapp = Column(String(50))
    telegram = Column(String(50))
    viber = Column(String(50))
    zoom = Column(String(50))
    prop_city = Column(String(100))
    prop_offer = Column(String(100))
    prop_type = Column(String(100))
    prop_state = Column(String(100))
    avatar = Column(String(100), default='noUserImage.svg')
    licenses = Column(String(100), default='noLicenseImage.svg')
    video = Column(String(100))
    about = Column(String(500))
    activation_code = Column(String(10), nullable=True)
    role = Column(String(10), default='user')
    updated = Column(BigInteger)
