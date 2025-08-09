from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from sqlalchemy import func

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.core.security import SecurityUtils, RateLimiter
from app.models.user import User
from app.models.video import Video
from app.models.avatar import Avatar
from app.schemas.video import VideoCreate, VideoUpdate, VideoResponse, VideoStatus
from app.services.video_generator import video_generator
from app.services.voice_service import VoiceService

router = APIRouter()

@router.post("/create", response_model=VideoResponse)
async def create_video(
    video_data: VideoCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """create a new video generation request"""
    # additional rate limiting for video creation
    if not RateLimiter.check_rate_limit(request, limit=5):  # 5 videos per minute
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="too many video creation requests. please wait."
        )
    
    # verify avatar exists and is active (if avatar_id is provided)
    avatar_id = None
    if video_data.avatar_id:
        avatar = db.query(Avatar).filter(Avatar.id == video_data.avatar_id, Avatar.is_active == True).first()
        if avatar:
            avatar_id = video_data.avatar_id
        else:
            # avatar not found, but we can still create video without avatar
            print(f"avatar {video_data.avatar_id} not found, creating video without avatar")
    
    # create video record
    db_video = Video(
        user_id=current_user.id,
        title=video_data.title,
        description=video_data.description,
        script=video_data.script,
        avatar_id=avatar_id,  # use None if avatar not found
        voice_id=video_data.voice_id,
        language=video_data.language,
        status="pending"  # use string value
    )
    
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    
    # start video generation in background
    background_tasks.add_task(
        generate_video_background,
        video_id=db_video.id,
        user_id=current_user.id
    )
    
    return db_video

@router.get("/list", response_model=List[VideoResponse])
async def list_videos(
    skip: int = 0,
    limit: int = 10,
    status_filter: Optional[VideoStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """get user's videos with optional filtering"""
    # validate pagination parameters
    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid pagination parameters"
        )
    
    query = db.query(Video).filter(Video.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Video.status == status_filter)
    
    videos = query.offset(skip).limit(limit).all()
    return videos

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """get a specific video by id"""
    # validate video_id
    if video_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid video id"
        )
    
    video = db.query(Video).filter(
        Video.id == video_id,
        Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="video not found"
        )
    
    print(f"Video {video_id} status: {video.status}, output_path: {video.output_video_path}")
    return video

@router.put("/{video_id}", response_model=VideoResponse)
async def update_video(
    video_id: int,
    video_update: VideoUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """update a video (only if not processing)"""
    # validate video_id
    if video_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid video id"
        )
    
    video = db.query(Video).filter(
        Video.id == video_id,
        Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="video not found"
        )
    
    if video.status == "processing":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cannot update video while processing"
        )
    
    # update fields
    update_data = video_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(video, field, value)
    
    db.commit()
    db.refresh(video)
    
    return video

@router.delete("/{video_id}")
async def delete_video(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """delete a video"""
    # validate video_id
    if video_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid video id"
        )
    
    video = db.query(Video).filter(
        Video.id == video_id,
        Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="video not found"
        )
    
    # delete associated files securely
    if video.output_video_path and os.path.exists(video.output_video_path):
        try:
            os.remove(video.output_video_path)
        except OSError:
            pass  # file might already be deleted
    
    if video.thumbnail_path and os.path.exists(video.thumbnail_path):
        try:
            os.remove(video.thumbnail_path)
        except OSError:
            pass  # file might already be deleted
    
    db.delete(video)
    db.commit()
    
    return {"message": "video deleted successfully"}

@router.get("/{video_id}/download")
async def download_video(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """download a completed video"""
    # validate video_id
    if video_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid video id"
        )
    
    video = db.query(Video).filter(
        Video.id == video_id,
        Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="video not found"
        )
    
    if video.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="video not ready for download"
        )
    
    if not video.output_video_path or not os.path.exists(video.output_video_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="video file not found"
        )
    
    # validate file path to prevent path traversal
    video_path = os.path.abspath(video.output_video_path)
    static_dir = os.path.abspath("static/videos")
    
    if not video_path.startswith(static_dir):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid file path"
        )
    
    return {"download_url": f"/generated/{video.id}.mp4"}

async def generate_video_background(video_id: int, user_id: int):
    """background task for video generation using free services"""
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        # get video record
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            return
        
        # update status to processing
        video.status = "processing"  # use string value
        video.progress = 0.1
        db.commit()
        
        # generate video using free service
        try:
            # use simple video generation (text overlay + audio)
            video_path = video_generator.create_simple_video(
                script=video.script,
                language=video.language or "en"
            )
            
            # check if video was actually created
            if not os.path.exists(video_path):
                video.status = "failed"
                video.error_message = "video file was not created"
                db.commit()
                return
            
            # move/copy to generated directory outside backend
            # use the same directory that's mounted as /generated
            base_dir = "C:/temp/vidface_videos"
            os.makedirs(base_dir, exist_ok=True)
            target_path = os.path.join(base_dir, f"{video.id}.mp4")
            print(f"Copying video from {video_path} to {target_path}")
            try:
                import shutil
                shutil.copyfile(video_path, target_path)
                final_path = target_path
                print(f"Successfully copied video to {final_path}")
                print(f"Video should be accessible at: http://127.0.0.1:8000/generated/{video.id}.mp4")
            except Exception as e:
                print(f"error copying video to generated dir: {str(e)}")
                final_path = video_path
            
            # update video record
            video.output_video_path = final_path
            video.status = "completed"  # use string value instead of enum
            video.progress = 1.0
            video.completed_at = func.now()
            
            # get video duration and file size
            try:
                from moviepy.editor import VideoFileClip
                clip = VideoFileClip(final_path)
                video.duration = clip.duration
                video.file_size = os.path.getsize(final_path)
                clip.close()
            except Exception as e:
                print(f"error getting video metadata: {str(e)}")
                video.duration = 10.0
                video.file_size = os.path.getsize(final_path) if os.path.exists(final_path) else 0
            
            db.commit()
            print(f"video {video_id} generated successfully: {final_path}")
            
        except Exception as e:
            print(f"video generation failed for video {video_id}: {str(e)}")
            video.status = "failed"
            video.error_message = str(e)
            db.commit()
            
    except Exception as e:
        print(f"background task error for video {video_id}: {str(e)}")
        # update status to failed
        video = db.query(Video).filter(Video.id == video_id).first()
        if video:
            video.status = "failed"
            video.error_message = str(e)
            db.commit()
    finally:
        db.close() 