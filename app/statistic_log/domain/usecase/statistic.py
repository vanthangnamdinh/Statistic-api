import json
from abc import ABC, abstractmethod

from app.statistic_log.domain.command import CreateStatisticLogCommand


class StatisticLogUseCase(ABC):
    @abstractmethod
    async def create_log(self, *, command: CreateStatisticLogCommand) -> None:
        """Create log"""
