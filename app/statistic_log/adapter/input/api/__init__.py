from fastapi import APIRouter

from app.statistic_log.adapter.input.api.v1.statistic import statistic_router as statistic_v1_router

router = APIRouter()
router.include_router(statistic_v1_router, prefix="/api/v1/statistic", tags=["Statistic"])

__all__ = ["router"]
