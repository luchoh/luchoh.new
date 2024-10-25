from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from cachetools import TTLCache

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Using TTLCache with key expiration
        self.request_counts = TTLCache(
            maxsize=10000,  # Max number of IPs to track
            ttl=window_seconds  # Automatic cleanup after window expires
        )

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Skip rate limiting for static files and admin paths
        if request.url.path.startswith(("/static/", "/admin/")):
            return await call_next(request)

        # Update request count for this IP
        current_count = self.request_counts.get(client_ip, 0) + 1
        self.request_counts[client_ip] = current_count

        # Check if rate limit exceeded
        if current_count > self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

        return await call_next(request)