from fastapi import FastAPI

from app.routers import songs, user
from app.utils import auth

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(songs.router)
