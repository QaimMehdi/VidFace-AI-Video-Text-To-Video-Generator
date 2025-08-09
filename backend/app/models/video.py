from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Video content
    script = Column(Text, nullable=False)
    avatar_id = Column(Integer, ForeignKey("avatars.id"), nullable=True)  # allow null for simple videos
    voice_id = Column(String(100))
    language = Column(String(10), default="en")
    
    # File paths
    input_audio_path = Column(String(500))
    output_video_path = Column(String(500))
    thumbnail_path = Column(String(500))
    
    # Video metadata
    duration = Column(Float)  # in seconds
    resolution = Column(String(20))  # e.g., "1920x1080"
    file_size = Column(Integer)  # in bytes
    format = Column(String(10), default="mp4")
    
    # Processing status
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User")
    avatar = relationship("Avatar")
    
    def __repr__(self):
        return f"<Video(id={self.id}, title='{self.title}', status='{self.status}')>" 