from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.avatar import Avatar
from app.schemas.avatar import AvatarResponse

router = APIRouter()

@router.get("/list", response_model=List[AvatarResponse])
async def list_avatars(
    category: Optional[str] = None,
    gender: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get available avatars with optional filtering"""
    query = db.query(Avatar).filter(Avatar.is_active == True, Avatar.is_public == True)
    
    if category:
        query = query.filter(Avatar.category == category)
    
    if gender:
        query = query.filter(Avatar.gender == gender)
    
    avatars = query.limit(limit).all()
    return avatars

@router.get("/categories")
async def get_avatar_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get available avatar categories"""
    categories = db.query(Avatar.category).filter(
        Avatar.is_active == True,
        Avatar.is_public == True,
        Avatar.category.isnot(None)
    ).distinct().all()
    
    return {"categories": [cat[0] for cat in categories]}

@router.get("/{avatar_id}", response_model=AvatarResponse)
async def get_avatar(
    avatar_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific avatar by ID"""
    avatar = db.query(Avatar).filter(
        Avatar.id == avatar_id,
        Avatar.is_active == True,
        Avatar.is_public == True
    ).first()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )
    
    return avatar

@router.get("/popular", response_model=List[AvatarResponse])
async def get_popular_avatars(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get most popular avatars"""
    avatars = db.query(Avatar).filter(
        Avatar.is_active == True,
        Avatar.is_public == True
    ).order_by(Avatar.usage_count.desc()).limit(limit).all()
    
    return avatars

@router.get("/featured", response_model=List[AvatarResponse])
async def get_featured_avatars(
    limit: int = 6,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get featured avatars (high rating)"""
    avatars = db.query(Avatar).filter(
        Avatar.is_active == True,
        Avatar.is_public == True,
        Avatar.rating >= 4
    ).order_by(Avatar.rating.desc()).limit(limit).all()
    
    return avatars 