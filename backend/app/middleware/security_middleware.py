from fastapi import Request, HTTPException, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
from typing import Callable

from app.core.config import settings
from app.core.security import RateLimiter, SecurityUtils, SecurityMiddleware

class SecurityMiddlewareClass(BaseHTTPMiddleware):
    """security middleware for request validation and rate limiting"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # rate limiting check
        if not RateLimiter.check_rate_limit(request):
            remaining = RateLimiter.get_remaining_requests(request)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"rate limit exceeded. try again in 60 seconds. remaining requests: {remaining}",
                headers={"Retry-After": "60"}
            )
        
        # host header validation (for prod)
        if not settings.DEBUG and not SecurityMiddleware.validate_host_header(request):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid host header"
            )
        
        # process request
        response = await call_next(request)
        
        # add security headers
        response = SecurityMiddleware.add_security_headers(response)
        
        # add rate limit headers
        remaining = RateLimiter.get_remaining_requests(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
        
        return response

class RequestValidationMiddleware(BaseHTTPMiddleware):
    """middleware for validating request content"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # validate content length
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="file too large"
            )
        
        # process request
        response = await call_next(request)
        return response 