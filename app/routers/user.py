from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user_model
from app.schemas import user_schema

router = APIRouter(prefix="/user", tags=["User"])


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
