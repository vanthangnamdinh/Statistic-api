from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.statistic_log.application.service.statistic import StatisticService
from app.statistic_log.adapter.output.persistence.repository_adapter import StatisticRepositoryAdapter
from app.statistic_log.adapter.output.persistence.sqlalchemy.statistic import StatisticLogRepo


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    statistic_log_repo = Singleton(StatisticLogRepo)
    statistic_repo_adapter = Factory(StatisticRepositoryAdapter, statistic_repo=statistic_log_repo)
    statistic_service = Factory(StatisticService, repository=statistic_repo_adapter)
