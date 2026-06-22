from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str
    TO_EMAIL: str
    
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

