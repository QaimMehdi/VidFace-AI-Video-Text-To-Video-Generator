import re
import hashlib
import secrets
from typing import Optional, List
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from collections import defaultdict
import os
from pathlib import Path
from passlib.context import CryptContext

from app.core.config import settings

# rate limiting storage (in production, use redis)
rate_limit_storage = defaultdict(list)
login_attempts = defaultdict(list)

# password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityUtils:
    """security utilities for the application"""
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """validate file extension against allowed extensions"""
        if not filename:
            return False
        
        extension = filename.lower().split('.')[-1]
        return extension in settings.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """validate file size against maximum allowed size"""
        return file_size <= settings.MAX_UPLOAD_SIZE
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """sanitize filename to prevent path traversal attacks"""
        # remove any path separators and dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:255-len(ext)] + ext
        return filename
    
    @staticmethod
    def generate_secure_filename(original_filename: str) -> str:
        """generate a secure random filename"""
        extension = Path(original_filename).suffix
        random_name = secrets.token_urlsafe(16)
        return f"{random_name}{extension}"
    
    @staticmethod
    def validate_script_content(script: str) -> bool:
        """validate script content for malicious content"""
        # check for script injection attempts
        dangerous_patterns = [
            r'<script',
            r'javascript:',
            r'on\w+\s*=',
            r'data:text/html',
            r'vbscript:',
            r'<iframe',
            r'<object',
            r'<embed'
        ]
        
        script_lower = script.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, script_lower):
                return False
        
        return True
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """validate password strength: 8+ chars, at least one digit, at least one symbol"""
        if len(password) < 8:
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[^A-Za-z0-9]', password):
            return False
        return True
    
    @staticmethod
    def hash_password(password: str) -> str:
        """hash password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """verify password against bcrypt hash"""
        return pwd_context.verify(password, hashed)
    
    @staticmethod
    def check_login_attempts(client_ip: str) -> bool:
        """check if client is locked out due to too many login attempts"""
        current_time = time.time()
        
        # clean old attempts (older than lockout period)
        login_attempts[client_ip] = [
            attempt for attempt in login_attempts[client_ip]
            if current_time - attempt < settings.LOGIN_LOCKOUT_MINUTES * 60
        ]
        
        # check if too many attempts
        if len(login_attempts[client_ip]) >= settings.MAX_LOGIN_ATTEMPTS:
            return False
        
        return True
    
    @staticmethod
    def record_login_attempt(client_ip: str, success: bool):
        """record a login attempt"""
        current_time = time.time()
        
        if success:
            # clear failed attempts on successful login
            login_attempts[client_ip] = []
        else:
            # record failed attempt
            login_attempts[client_ip].append(current_time)

class RateLimiter:
    """rate limiting implementation"""
    
    @staticmethod
    def check_rate_limit(request: Request, limit: int = None) -> bool:
        """check if request is within rate limit"""
        if limit is None:
            limit = settings.RATE_LIMIT_PER_MINUTE
        
        client_ip = request.client.host
        current_time = time.time()
        
        # clean old entries (older than 1 minute)
        rate_limit_storage[client_ip] = [
            timestamp for timestamp in rate_limit_storage[client_ip]
            if current_time - timestamp < 60
        ]
        
        # check if limit exceeded
        if len(rate_limit_storage[client_ip]) >= limit:
            return False
        
        # add current request
        rate_limit_storage[client_ip].append(current_time)
        return True
    
    @staticmethod
    def get_remaining_requests(request: Request, limit: int = None) -> int:
        """get remaining requests for client"""
        if limit is None:
            limit = settings.RATE_LIMIT_PER_MINUTE
        
        client_ip = request.client.host
        current_time = time.time()
        
        # clean old entries
        rate_limit_storage[client_ip] = [
            timestamp for timestamp in rate_limit_storage[client_ip]
            if current_time - timestamp < 60
        ]
        
        return max(0, limit - len(rate_limit_storage[client_ip]))

class SecurityMiddleware:
    """security middleware for additional protection"""
    
    @staticmethod
    def validate_host_header(request: Request) -> bool:
        """validate host header"""
        host = request.headers.get('host', '')
        return any(allowed_host in host for allowed_host in settings.ALLOWED_HOSTS)
    
    @staticmethod
    def add_security_headers(response):
        """add security headers to response"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # content security policy
        csp_parts = [
            f"default-src {settings.CSP_DEFAULT_SRC}",
            f"script-src {settings.CSP_SCRIPT_SRC}",
            f"style-src {settings.CSP_STYLE_SRC}",
            f"img-src {settings.CSP_IMG_SRC}",
            f"font-src {settings.CSP_FONT_SRC}",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'"
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_parts)
        
        # additional security headers
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response 