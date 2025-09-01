import uvicorn
from fastapi import FastAPI

from app.routers import category, user, auth, expense
from app.settings import config
from app.middlewares import RateLimitMiddleware

app = FastAPI()

app.add_middleware(RateLimitMiddleware, max_requests=10, window=60)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(expense.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=config.host, port=config.port, reload=True)
