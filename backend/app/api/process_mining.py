"""
Process Mining API - Enterprise AI Platform (ML-048)
Exposes process discovery and bottleneck analysis over HTTP.
"""

from fastapi import APIRouter, HTTPException
from app.services.process_mining import discover_process_map, find_bottlenecks

router = APIRouter()

# Path to the event log CSV (relative to where uvicorn is run, i.e. backend/)
CSV_PATH = "dataset/workflow_events.csv"


@router.get("/discover")
def discover():
    """
    Returns the discovered process map: total cases, activities,
    start/end activities, and the top 10 most frequent transitions.
    """
    try:
        return discover_process_map(CSV_PATH)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Event log not found at '{CSV_PATH}'. Make sure workflow_events.csv is in the dataset/ folder."
        )


@router.get("/bottlenecks")
def bottlenecks(top_n: int = 5):
    """
    Returns the slowest transitions (average hours between activities),
    highlighting likely bottlenecks in the process.
    """
    try:
        return find_bottlenecks(CSV_PATH, top_n=top_n)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Event log not found at '{CSV_PATH}'. Make sure workflow_events.csv is in the dataset/ folder."
        )
