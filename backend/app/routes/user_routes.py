from app.security.auth import get_current_user
from app.schemas.login_schema import LoginRequest
from app.security.jwt_handler import create_access_token
from app.security.hash import verify_password
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
@router.post("/login")
def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:
        return {
            "message": "Invalid email or password"
        }

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        return {
            "message": "Invalid email or password"
        }

    token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/profile")
def get_profile(
    current_user=Depends(get_current_user)
):

    return {
        "message": "Protected route working",
        "user": current_user
    }