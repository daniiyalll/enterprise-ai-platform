from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.dashboard_service import get_dashboard_stats
from app.core.permissions import require_manager


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def stats(
    db: Session = Depends(get_db),
    current_user=Depends(require_manager)
):

    return get_dashboard_stats(db)