from fastapi import FastAPI

from app.routers import user
from app.utils import auth

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
