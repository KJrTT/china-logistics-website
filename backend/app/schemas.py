from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
import re

class FeedbackCreate(BaseModel):
    name: str
    contact: str
    message: str
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Имя должно содержать минимум 2 символа')
        return v.strip()
    
    @validator('contact')
    def validate_contact(cls, v):
        v = v.strip()
        
        if not v or len(v) < 5:
            raise ValueError('Контакт должен содержать минимум 5 символов')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'^(\+7|8)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
        phone_pattern_simple = r'^[\+\d\s\-\(\)]{10,20}$'
        
        is_email = re.match(email_pattern, v) is not None
        is_phone = re.match(phone_pattern, v) is not None or re.match(phone_pattern_simple, v) is not None
        
        if not is_email and not is_phone:
            raise ValueError('Введите корректный email или номер телефона')
        
        return v
    
    @validator('message')
    def validate_message(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Сообщение должно содержать минимум 10 символов')
        return v.strip()

class FeedbackResponse(BaseModel):
    id: int
    name: str
    contact: str
    message: str
    status: str
    is_processed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class FeedbackUpdate(BaseModel):
    status: str
    is_processed: Optional[bool] = None