import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def hash_password(password):

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(
    plain_password,
    hashed_password
):

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    payload = decode_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload