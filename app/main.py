from fastapi import FastAPI

from app.routers import auth, song, user

app = FastAPI()

app.include_router(auth.router)
app.include_router(song.router)
app.include_router(user.router)
