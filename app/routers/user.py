from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user_model
from app.schemas import user_schema
from app.utils import auth

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/signup",
    response_model=user_schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def createUser(user: user_schema.UserBase, db: Session = Depends(get_db)):
    email_check = (
        db.query(user_model.User).filter(user_model.User.email == user.email).first()
    )
    if email_check is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    hashed_password = auth.hash(user.password)
    user.password = hashed_password
    new_user = user_model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=user_schema.UserResponse)
def getUserById(id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} not found!",
        )
    return user


@router.delete("/{id}")
def deleteUserById(id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id)
    user.delete()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User already deleted"
        )
    db.commit()
