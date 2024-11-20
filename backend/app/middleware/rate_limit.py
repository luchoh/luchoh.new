# Project: luchoh.com refactoring
# File: backend/middleware/rate_limit.py

"""Rate limiting middleware for the FastAPI application.

This module provides rate limiting functionality to protect the API
from excessive requests using a token bucket algorithm implemented
with TTLCache.
"""

from typing import Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from cachetools import TTLCache
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware for the FastAPI application.

    This module provides rate limiting functionality to protect the API
    from excessive requests using a token bucket algorithm implemented
    with TTLCache.

    Attributes:
        max_requests (int): Maximum number of requests allowed per window
        window_seconds (int): Time window in seconds for rate limiting
        request_counts (TTLCache): Cache to store request counts per IP
    """

    def __init__(
        self,
        app,
        max_requests: int = 1000,  # Increased from 100
        window_seconds: int = 60,
        max_tokens: Optional[int] = None
    ):
        """Initialize the rate limit middleware.

        Args:
            app: The FastAPI application
            max_requests: Maximum number of requests allowed per window
            window_seconds: Time window in seconds
            max_tokens: Maximum number of tokens to store (defaults to max_requests)
        """
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_counts = TTLCache(
            maxsize=max_tokens or max_requests,
            ttl=window_seconds
        )

    async def dispatch(self, request: Request, call_next):
        """Process the request and apply rate limiting.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            The response from the next handler

        Raises:
            HTTPException: When rate limit is exceeded
        """
        # Get client IP
        client_ip = request.client.host

        # Skip rate limiting for these paths
        skip_paths = [
            "/static/",
            "/uploads/",
            "/favicon.ico",
        ]
        
        # Skip rate limiting for excluded paths
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)

        # Skip rate limiting for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)

        # Get current window key (IP + timestamp rounded to window)
        current_time = int(time.time() / self.window_seconds) * self.window_seconds
        window_key = f"{client_ip}:{current_time}"

        # Update request count for this IP in this window
        current_count = self.request_counts.get(window_key, 0) + 1
        self.request_counts[window_key] = current_count

        # Check if rate limit exceeded
        if current_count > self.max_requests:
            # Calculate reset time
            reset_time = current_time + self.window_seconds
            reset_seconds = int(reset_time - time.time())
            
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Too many requests",
                    "reset_in_seconds": reset_seconds,
                    "limit": self.max_requests,
                    "window_seconds": self.window_seconds
                }
            )

        # Add rate limit headers to response
        response = await call_next(request)
        remaining = self.max_requests - current_count
        
        # Add headers only to Response objects (not StreamingResponse)
        if hasattr(response, "headers"):
            response.headers["X-RateLimit-Limit"] = str(self.max_requests)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(current_time + self.window_seconds)
        
        return response

    def reset_counts(self) -> None:
        """Reset all request counts in the cache."""
        self.request_counts.clear()