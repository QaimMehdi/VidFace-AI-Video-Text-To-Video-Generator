from pydantic_settings import BaseSettings
from typing import Optional, List
import os
import secrets

class Settings(BaseSettings):
    # database configuration - use mysql
    DATABASE_URL: str = "mysql+pymysql://root:q1A2I3M4!!@localhost/vidface_db"
    
    # jwt - generate secure secret if not provided
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # redis configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # aws s3 (for file storage)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "vidface-videos"
    
    # file storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100mb
    
    # ai models - must be set via environment variables
    OPENAI_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # video processing
    MAX_VIDEO_DURATION: int = 300  # 5 minutes
    SUPPORTED_VIDEO_FORMATS: List[str] = ["mp4", "avi", "mov", "mkv"]
    SUPPORTED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "m4a"]
    
    # rate limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100
    RATE_LIMIT_PER_DAY: int = 1000
    
    # security settings
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    DEBUG: bool = True  # enabled for development
    
    # cors settings - restrict to specific origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5500",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8080"
    ]
    
    # file upload security
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "mp4", "avi", "mov", "mkv"]
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50mb
    
    # additional security settings
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True
    
    # session security
    SESSION_TIMEOUT_MINUTES: int = 30
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_MINUTES: int = 15
    
    # api security
    API_KEY_HEADER: str = "X-API-Key"
    API_KEY_REQUIRED: bool = False  # set to true in production
    
    # content security policy
    CSP_DEFAULT_SRC: str = "'self'"
    CSP_SCRIPT_SRC: str = "'self' 'unsafe-inline'"
    CSP_STYLE_SRC: str = "'self' 'unsafe-inline'"
    CSP_IMG_SRC: str = "'self' data: https:"
    CSP_FONT_SRC: str = "'self' https:"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 