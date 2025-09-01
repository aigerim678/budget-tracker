from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse

from app.redis_scripts import rate_limiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window

    async def dispatch(self, request: Request, call_next):
        try:
            key = f"rl:{request.client.host}"
            allowed = rate_limiter(keys=[key], args=[self.max_requests, self.window])
            if not int(allowed):
                raise HTTPException(status_code=429, detail="Too Many Requests")

            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code,
                                content={"detail": e.detail}
                                )
