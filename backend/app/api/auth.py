from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import signup_user, login_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):

    new_user = signup_user(db, user)

    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )

    return new_user


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):

    token = login_user(db, user)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
