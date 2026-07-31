from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.ai import router as ai_router
from app.api.workflows import router as workflows_router
from app.api.process_mining import router as process_mining_router
from app.api.copilot import router as copilot_router
from app.api.decisions import router as decisions_router

from app.api import agents
from app.api import auth


api_router = APIRouter()


# Health APIs
api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)


# AI Prediction APIs
api_router.include_router(
    ai_router,
    prefix="/ai",
    tags=["AI"]
)


# Workflow APIs
api_router.include_router(
    workflows_router,
    prefix="/workflows",
    tags=["Workflows"]
)


# Process Mining APIs
api_router.include_router(
    process_mining_router,
    prefix="/process-mining",
    tags=["Process Mining"]
)


# AI Copilot APIs
api_router.include_router(
    copilot_router,
    tags=["AI Copilot"]
)


# Decision Engine APIs
api_router.include_router(
    decisions_router,
    tags=["Decision Engine"]
)


# AI Agents APIs
api_router.include_router(
    agents.router,
    tags=["AI Agents"]
)


# Authentication APIs
api_router.include_router(
    auth.router,
    tags=["Authentication"]
)