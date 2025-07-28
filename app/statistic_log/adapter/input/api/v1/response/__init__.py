from pydantic import BaseModel, Field


class StatisticLogResponse(BaseModel):
    status: str = Field(..., description="Status")
    status_code: int = Field(..., description="Status code")
