import uuid

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/songs", tags=["Songs"])

cloudinary.config(
    cloud_name="dj8tlh3sm",
    api_key="382619618178785",
    api_secret="ZchlECOIBG4tpCU4SmAeKbTbtMc",
    secure=True,
)


@router.post("/")
async def createSong(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    song_name: str = Form(...),
    hex_code: str = Form(...),
    db: Session = Depends(get_db),
):

    try:
        song_id = str(uuid.uuid4())
        song_file = await song.read()
        song_res = cloudinary.uploader.upload(
            song_file,
            folder=f"songs/{song_id}",
            resource_type="auto",
        )

        thumbnail_file = await thumbnail.read()
        thumbnail_res = cloudinary.uploader.upload(
            thumbnail_file,
            folder=f"songs/{song_id}",
            resource_type="auto",
        )

        return {
            "status": "ok",
            "song_url": song_res["url"],
            "thumbnail_url": thumbnail_res["url"],
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
