from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINS = settings.access_token_expire_mins

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=("login"))


def createAccessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)

    to_encode.update({"expire": expire.timestamp()})
    jwt_encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encoded
