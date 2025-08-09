from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    subscription_tier = Column(String(50), default="free")  # free, pro, enterprise
    subscription_expires = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Profile fields
    avatar_url = Column(String(500))
    bio = Column(Text)
    company = Column(String(200))
    website = Column(String(500))
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>" 