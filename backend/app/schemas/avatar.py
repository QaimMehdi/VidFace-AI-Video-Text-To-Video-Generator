from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AvatarBase(BaseModel):
    name: str
    image_path: str
    category: str
    gender: Optional[str] = None
    is_public: bool = True
    is_active: bool = True
    usage_count: int = 0
    ai_model_id: Optional[str] = None  # renamed from model_id to avoid pydantic warning

class AvatarCreate(AvatarBase):
    pass

class AvatarResponse(AvatarBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 