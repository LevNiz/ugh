from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://avvhh_user:avvhh_password@localhost/avvhh"
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SMS_API_URL: str = "https://sms.ru/api/send"
    SMS_API_TOKEN: str = "8AF6EC7A-53C3-80C0-E90B-CA7787E31DC8"

settings = Settings()
