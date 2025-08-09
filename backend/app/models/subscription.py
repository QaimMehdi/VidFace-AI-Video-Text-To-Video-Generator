from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Subscription details
    plan_type = Column(String(50), nullable=False)  # free, pro, enterprise
    status = Column(String(50), default="active")  # active, cancelled, expired
    
    # Billing
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    billing_cycle = Column(String(20))  # monthly, yearly
    
    # Dates
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    cancelled_at = Column(DateTime)
    
    # Payment info
    payment_method = Column(String(100))
    last_payment_date = Column(DateTime)
    next_payment_date = Column(DateTime)
    
    # Features
    video_limit = Column(Integer)  # -1 for unlimited
    storage_limit = Column(Integer)  # in MB, -1 for unlimited
    resolution_limit = Column(String(20))  # e.g., "1080p", "4K"
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan='{self.plan_type}')>" 