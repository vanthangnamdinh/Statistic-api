from app.statistic_log.domain.repository.statistic import StatisticRepo


class StatisticRepositoryAdapter:
    def __init__(self, *, statistic_repo: StatisticRepo):
        self.statistic_repo = statistic_repo

    async def create_log(self, *, data) -> None:
        await self.statistic_repo.create_log(data=data)
