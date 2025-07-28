from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.statistic_log.adapter.output.persistence.repository_adapter import StatisticRepositoryAdapter
from app.statistic_log.adapter.output.persistence.sqlalchemy.statistic import StatisticLogRepo
from app.statistic_log.application.service.statistic import StatisticService


class StatisticContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    statistic_log_repo = Singleton(StatisticLogRepo)
    statistic_repository_adapter = Factory(
        StatisticRepositoryAdapter,
        repository=statistic_log_repo,
    )
    statistic_service = Factory(StatisticService, repository=statistic_repository_adapter)
