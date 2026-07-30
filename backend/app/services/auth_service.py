from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


def signup_user(db: Session, user_data):

    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        return None

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, login_data):

    user = db.query(User).filter(
        User.username == login_data.username
    ).first()

    if not user:
        return None

    if not verify_password(login_data.password, user.hashed_password):
        return None

    token = create_access_token({"sub": user.username})

    return token
