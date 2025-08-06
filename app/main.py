import uvicorn
from fastapi import FastAPI

from app.routers import category, user, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8080, reload=True)
