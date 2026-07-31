from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.ai import router as ai_router
from app.api.workflows import router as workflows_router
from app.api.process_mining import router as process_mining_router
from app.api.copilot import router as copilot_router
from app.api import agents
from app.api import auth


api_router = APIRouter()


api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)

api_router.include_router(
    ai_router,
    prefix="/ai",
    tags=["AI"]
)

api_router.include_router(
    workflows_router,
    prefix="/workflows",
    tags=["Workflows"]
)

api_router.include_router(
    process_mining_router,
    prefix="/process-mining",
    tags=["Process Mining"]
)

api_router.include_router(
    copilot_router,
    tags=["AI Copilot"]
)

api_router.include_router(
    agents.router,
    tags=["AI Agents"]
)

api_router.include_router(
    auth.router,
    tags=["Authentication"]
)