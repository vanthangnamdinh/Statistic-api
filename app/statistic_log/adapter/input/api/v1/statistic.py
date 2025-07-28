from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.statistic_log.adapter.input.api.v1.request import StatisticLogRequest
from app.statistic_log.adapter.input.api.v1.response import StatisticLogResponse
from app.statistic_log.domain.command import CreateStatisticLogCommand
from app.statistic_log.domain.usecase.statistic import StatisticLogUseCase
from core.fastapi.dependencies import PermissionDependency
import uvicorn
import logging
logger = logging.getLogger('uvicorn.error')

statistic_router = APIRouter()

@statistic_router.post(
    "/log",
    response_model=StatisticLogResponse,
)
@inject
async def log(
    request: StatisticLogRequest,
    usecase: StatisticLogUseCase = Depends(Provide[Container.statistic_service]),
):
    command = CreateStatisticLogCommand(**request.model_dump())
    await usecase.create_log(command=command)
    return {"status_code": 0, "status": "Success"}