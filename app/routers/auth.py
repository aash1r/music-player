from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import oauth2, utils
from app.database import get_db
from app.models import user_model
from app.schemas import user_schema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=user_schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(user: user_schema.UserBase, db: Session = Depends(get_db)):
    email_check = (
        db.query(user_model.User).filter(user_model.User.email == user.email).first()
    )
    if email_check is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = user_model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(
    user_credits: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(user_model.User)
        .filter(user_model.User.email == user_credits.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not utils.verify(user_credits.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Passwords do not match!"
        )

    access_token = oauth2.createAccessToken(data={"user id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}
