from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token
)

from app.schemas.user import UserLogin

from app.services.auth_service import (
    signup_user,
    login_user
)

from app.core.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post(
    "/signup",
    response_model=UserResponse
)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    if user.secret_key != settings.SIGNUP_SECRET:

        raise HTTPException(
            status_code=403,
            detail="Invalid signup secret key"
        )


    new_user = signup_user(
        db,
        user
    )


    if not new_user:

        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )


    return new_user




@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = UserLogin(
        username=form_data.username,
        password=form_data.password
    )


    token = login_user(
        db,
        user
    )


    if not token:

        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )


    return {
        "access_token": token,
        "token_type": "bearer"
    }