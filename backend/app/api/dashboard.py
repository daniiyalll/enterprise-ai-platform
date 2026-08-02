from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.dashboard_service import get_dashboard_stats
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_dashboard_stats(db)
