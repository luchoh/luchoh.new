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
        max_requests: int = 100,
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

    def reset_counts(self) -> None:
        """Reset all request counts in the cache.

        This method can be useful for testing or manual intervention.
        """
        self.request_counts.clear()
