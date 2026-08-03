from fastapi import APIRouter, Depends, HTTPException

from app.services.process_mining import (
    discover_process_map,
    find_bottlenecks
)

from app.core.permissions import require_manager


router = APIRouter()

CSV_PATH = "dataset/workflow_events.csv"


@router.get("/discover")
def discover(
    current_user=Depends(require_manager)
):

    try:
        return discover_process_map(CSV_PATH)

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail=f"Event log not found at '{CSV_PATH}'."
        )


@router.get("/bottlenecks")
def bottlenecks(
    top_n: int = 5,
    current_user=Depends(require_manager)
):

    try:
        return find_bottlenecks(
            CSV_PATH,
            top_n=top_n
        )

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail=f"Event log not found at '{CSV_PATH}'."
        )