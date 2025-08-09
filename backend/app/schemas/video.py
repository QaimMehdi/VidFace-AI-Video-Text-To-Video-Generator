from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from enum import Enum

from app.core.security import SecurityUtils

class VideoStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    script: str
    avatar_id: int
    voice_id: Optional[str] = None
    language: str = "en"
    
    @validator('script')
    def validate_script(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('script must be at least 10 characters long')
        if len(v) > 5000:
            raise ValueError('script must be less than 5000 characters')
        
        # security validation
        if not SecurityUtils.validate_script_content(v):
            raise ValueError('script contains potentially malicious content')
        
        return v
    
    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('title must be at least 3 characters long')
        if len(v) > 200:
            raise ValueError('title must be less than 200 characters')
        
        # security validation
        if not SecurityUtils.validate_script_content(v):
            raise ValueError('title contains potentially malicious content')
        
        return v
    
    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('description must be less than 1000 characters')
        
        # security validation
        if v and not SecurityUtils.validate_script_content(v):
            raise ValueError('description contains potentially malicious content')
        
        return v
    
    @validator('language')
    def validate_language(cls, v):
        # only allow common language codes
        allowed_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
        if v not in allowed_languages:
            raise ValueError('language not supported')
        return v

class VideoCreate(VideoBase):
    pass

class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    script: Optional[str] = None
    avatar_id: Optional[int] = None
    voice_id: Optional[str] = None
    language: Optional[str] = None
    
    @validator('script')
    def validate_script(cls, v):
        if v is not None:
            if len(v.strip()) < 10:
                raise ValueError('script must be at least 10 characters long')
            if len(v) > 5000:
                raise ValueError('script must be less than 5000 characters')
            
            # security validation
            if not SecurityUtils.validate_script_content(v):
                raise ValueError('script contains potentially malicious content')
        
        return v
    
    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            if len(v.strip()) < 3:
                raise ValueError('title must be at least 3 characters long')
            if len(v) > 200:
                raise ValueError('title must be less than 200 characters')
            
            # security validation
            if not SecurityUtils.validate_script_content(v):
                raise ValueError('title contains potentially malicious content')
        
        return v

class VideoResponse(VideoBase):
    id: int
    user_id: int
    status: VideoStatus
    progress: float
    duration: Optional[float] = None
    resolution: Optional[str] = None
    file_size: Optional[int] = None
    format: str = "mp4"
    output_video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 