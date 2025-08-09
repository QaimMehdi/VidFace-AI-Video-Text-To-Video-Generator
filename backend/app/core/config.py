from pydantic_settings import BaseSettings
from typing import Optional, List
import os
import secrets

class Settings(BaseSettings):
    # Application info
    APP_NAME: str = "VidFace API"
    APP_VERSION: str = "1.0.0"
    
    # Database configuration - NO HARDCODED CREDENTIALS
    DATABASE_URL: str
    
    # JWT configuration - secure random secret if not provided
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # AWS S3 (for file storage) - optional
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "vidface-videos"
    
    # File storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # AI models - must be set via environment variables
    OPENAI_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Video processing
    MAX_VIDEO_DURATION: int = 300  # 5 minutes
    VIDEO_OUTPUT_DIR: str = "C:/temp/vidface_videos"
    SUPPORTED_VIDEO_FORMATS: List[str] = ["mp4", "avi", "mov", "mkv"]
    SUPPORTED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "m4a"]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100
    RATE_LIMIT_PER_DAY: int = 1000
    
    # Security settings
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    DEBUG: bool = False  # Secure default - disabled
    
    # CORS settings - restrict to specific origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5500",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500"
    ]
    
    # Password validation settings
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = False  # More flexible for development
    REQUIRE_LOWERCASE: bool = False
    REQUIRE_DIGITS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = True
    
    # Session settings
    SESSION_TIMEOUT_MINUTES: int = 60
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    
    # File security
    MAX_FILENAME_LENGTH: int = 255
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "mp4", "mp3", "wav"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings() 