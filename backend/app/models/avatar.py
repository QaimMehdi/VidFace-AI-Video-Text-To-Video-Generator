from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Avatar(Base):
    __tablename__ = "avatars"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # avatar files
    image_path = Column(String(500), nullable=False)
    video_path = Column(String(500))  # reference video for training
    
    # avatar metadata
    category = Column(String(100))  # celebrity, professional, casual, custom
    gender = Column(String(20))  # male, female, neutral
    age_range = Column(String(50))  # e.g., "25-35", "40-50"
    ethnicity = Column(String(100))
    
    # ai model info
    ai_model_id = Column(String(200))  # ai model identifier (renamed from model_id)
    is_public = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # usage stats
    usage_count = Column(Integer, default=0)
    rating = Column(Integer, default=0)  # 1-5 stars
    
    # timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Avatar(id={self.id}, name='{self.name}', category='{self.category}')>" 