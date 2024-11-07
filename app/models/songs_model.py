from sqlalchemy import TIMESTAMP, Column, Integer, String, text

from app.database import Base


class Songs(Base):
    __tablename__ = "songs"

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
