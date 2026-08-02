from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.app_logger import logger


def signup_user(db: Session, user_data):

    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        logger.info(f"Signup failed - username or email already exists: {user_data.username}")
        return None

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user signed up: {new_user.username}")

    return new_user


def login_user(db: Session, login_data):

    user = db.query(User).filter(
        User.username == login_data.username
    ).first()

    if not user:
        logger.info(f"Login failed - user not found: {login_data.username}")
        return None

    if not verify_password(login_data.password, user.hashed_password):
        logger.info(f"Login failed - wrong password: {login_data.username}")
        return None

    token = create_access_token({"sub": user.username})

    logger.info(f"User logged in: {user.username}")

    return token
