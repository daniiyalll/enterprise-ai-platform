from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.core.roles import require_role


router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)


@router.get("/")
def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):

    users = db.query(User).all()

    return users


@router.put("/{user_id}/role")
def update_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):

    allowed_roles = [
        "admin",
        "manager",
        "employee"
    ]

    if role not in allowed_roles:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = role

    db.commit()
    db.refresh(user)

    return {
        "message": "Role updated successfully",
        "username": user.username,
        "new_role": user.role
    }