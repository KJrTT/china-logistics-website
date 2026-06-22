from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 465
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: str = "noreply@company.ru"
    TO_EMAIL: str = "manager@company.ru"
    
    # Mailtrap API (опционально)
    MAILTRAP_API_TOKEN: Optional[str] = None
    FROM_NAME: str = "Логистика B2B"
    
    SECRET_KEY: str = "dev_secret_key_1234567890"
    
    DEBUG: bool = True
    ENVIRONMENT: str = "dev"
    FRONTEND_URL: str = "http://localhost:3000"
    
    SEND_CONFIRMATION_TO_USER: bool = True
    SEND_NOTIFICATION_TO_MANAGER: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()