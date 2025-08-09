from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from app.routers import auth, video, avatar, user
from app.core.config import settings
from app.core.database import engine
from app.models import Base
from app.middleware.security_middleware import SecurityMiddlewareClass, RequestValidationMiddleware

# load environment variables
load_dotenv()

# create database tables
Base.metadata.create_all(bind=engine)

# initialize fastapi app
app = FastAPI(
    title="vidface api",
    description="ai avatar video generator api",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    debug=settings.DEBUG
)

# add CORS middleware FIRST (before any other middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # must be false when allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# temporarily disable security middleware to fix 500 errors
# app.add_middleware(SecurityMiddlewareClass)
# app.add_middleware(RequestValidationMiddleware)

# mount static files with security
app.mount("/static", StaticFiles(directory="static"), name="static")

# mount generated videos outside backend to avoid reloads
import pathlib
_output_env = os.getenv("VIDEO_OUTPUT_DIR")
if _output_env:
    _generated_dir = pathlib.Path(_output_env)
else:
    _generated_dir = pathlib.Path("C:/temp/vidface_videos")  # Use C:/temp to avoid any file watching
_generated_dir.mkdir(parents=True, exist_ok=True)
app.mount("/generated", StaticFiles(directory=str(_generated_dir)), name="generated")

# include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(video.router, prefix="/api/video", tags=["video generation"])
app.include_router(avatar.router, prefix="/api/avatar", tags=["avatar management"])
app.include_router(user.router, prefix="/api/user", tags=["user management"])

@app.get("/")
async def root():
    """root endpoint"""
    return {
        "message": "welcome to vidface api",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "documentation disabled in production"
    }

@app.get("/health")
async def health_check():
    """health check endpoint"""
    return {"status": "healthy", "service": "vidface api"}

@app.get("/status")
async def status_check():
    """detailed status endpoint"""
    import psutil
    return {
        "status": "healthy",
        "service": "vidface api",
        "memory_usage": psutil.virtual_memory().percent,
        "cpu_usage": psutil.cpu_percent(),
        "uptime": "running"
    }

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """custom 404 handler"""
    return JSONResponse({"error": "endpoint not found", "status_code": 404}, status_code=404)

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """custom 500 handler"""
    return JSONResponse({"error": "internal server error", "status_code": 500}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",  # changed from 0.0.0.0 to localhost
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    ) 