from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.responses import JSONResponse

from app.core.database import get_db
from app.core.auth import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.core.security import SecurityUtils
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.auth import Token

router = APIRouter()

def add_cors_headers(response: Response):
    """add cors headers to response"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@router.options("/register")
async def register_options(response: Response):
    """handle preflight request for register"""
    add_cors_headers(response)
    return JSONResponse({"message": "ok"})

@router.options("/login")
async def login_options(response: Response):
    """handle preflight request for login"""
    add_cors_headers(response)
    return JSONResponse({"message": "ok"})

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db), response: Response = None):
    """register a new user"""
    # add cors headers
    if response:
        add_cors_headers(response)
    
    # check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username already taken"
            )
    
    # create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin, 
    request: Request,
    db: Session = Depends(get_db)
):
    """login user and return access token"""
    client_ip = request.client.host
    
    # check if client is locked out
    if not SecurityUtils.check_login_attempts(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"too many login attempts. try again in {settings.LOGIN_LOCKOUT_MINUTES} minutes"
        )
    
    # find user by email
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        # record failed attempt
        SecurityUtils.record_login_attempt(client_ip, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        # record failed attempt
        SecurityUtils.record_login_attempt(client_ip, success=False)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="inactive user"
        )
    
    # record successful login
    SecurityUtils.record_login_attempt(client_ip, success=True)
    
    # create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user_id": user.id,
        "username": user.username
    }

@router.post("/login/form", response_model=Token)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """login using oauth2 form (for swagger ui)"""
    client_ip = request.client.host if request else "unknown"
    
    # check if client is locked out
    if not SecurityUtils.check_login_attempts(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"too many login attempts. try again in {settings.LOGIN_LOCKOUT_MINUTES} minutes"
        )
    
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        # record failed attempt
        SecurityUtils.record_login_attempt(client_ip, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        # record failed attempt
        SecurityUtils.record_login_attempt(client_ip, success=False)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="inactive user"
        )
    
    # record successful login
    SecurityUtils.record_login_attempt(client_ip, success=True)
    
    # create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user_id": user.id,
        "username": user.username
    } 