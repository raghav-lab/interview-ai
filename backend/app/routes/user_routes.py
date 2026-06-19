from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate
from app.security.hash import hash_password

from app.database.connection import get_db
from app.database.models import User

router = APIRouter()

@router.get("/test")
def test_route():
    return {"message": "User routes working"}

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }