from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional
import re

class FeedbackCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Имя")
    contact: str = Field(..., min_length=5, max_length=100, description="Телефон или email")
    message: str = Field(..., min_length=10, max_length=5000, description="Сообщение")
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Имя должно содержать минимум 2 символа')
        return v.strip()
    
    @validator('contact')
    def validate_contact(cls, v):
        v = v.strip()
        if len(v) < 5:
            raise ValueError('Контакт должен содержать минимум 5 символов')
        is_email = '@' in v and '.' in v
        is_phone = any(re.findall(r'\d', v)) and len(re.findall(r'\d', v)) >= 10
        if not is_email and not is_phone:
            raise ValueError('Введите корректный email или номер телефона')
        return v
    
    @validator('message')
    def validate_message(cls, v):
        if len(v.strip()) < 10:
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