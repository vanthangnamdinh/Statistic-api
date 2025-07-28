from app.statistic_log.adapter.output.persistence.repository_adapter import StatisticRepositoryAdapter
from app.statistic_log.domain.command import CreateStatisticLogCommand
from app.statistic_log.domain.usecase.statistic import StatisticLogUseCase
from core.db import Transactional
from core.helpers.token import TokenHelper


class StatisticService(StatisticLogUseCase):
    def __init__(self, *, repository: StatisticRepositoryAdapter):
        self.repository = repository

    async def create_log(self, *, command: CreateStatisticLogCommand) -> None:
        await self.repository.create_log(data=command)