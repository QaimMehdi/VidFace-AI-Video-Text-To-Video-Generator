import re
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

from app.core.security import SecurityUtils
from app.core.config import settings

class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if not SecurityUtils.validate_password_strength(v):
            raise ValueError(
                f'password must be at least {settings.PASSWORD_MIN_LENGTH} characters long '
                f'and contain uppercase, lowercase, digits, and special characters'
            )
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('invalid email format')
        return v.lower()
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('username must be less than 50 characters')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('username can only contain letters, numbers, and underscores')
        return v.lower()

class UserLogin(BaseModel):
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        return v.lower()

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    subscription_tier: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 