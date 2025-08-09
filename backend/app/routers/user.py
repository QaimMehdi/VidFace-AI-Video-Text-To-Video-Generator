from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user's profile"""
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    # Update fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    from app.models.video import Video, VideoStatus
    
    # Video statistics
    total_videos = db.query(Video).filter(Video.user_id == current_user.id).count()
    completed_videos = db.query(Video).filter(
        Video.user_id == current_user.id,
        Video.status == VideoStatus.COMPLETED
    ).count()
    processing_videos = db.query(Video).filter(
        Video.user_id == current_user.id,
        Video.status == VideoStatus.PROCESSING
    ).count()
    
    # Subscription info
    subscription_info = {
        "tier": current_user.subscription_tier,
        "expires": current_user.subscription_expires,
        "is_active": current_user.subscription_expires is None or current_user.subscription_expires > datetime.utcnow()
    }
    
    return {
        "total_videos": total_videos,
        "completed_videos": completed_videos,
        "processing_videos": processing_videos,
        "subscription": subscription_info
    } 