from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.statistic_log.adapter.output.persistence.repository_adapter import StatisticRepositoryAdapter
from app.statistic_log.adapter.output.persistence.sqlalchemy.statistic import StatisticLogRepo
from app.statistic_log.adapter.output.persistence.sqlalchemy.statistic_sqlalchemy import StatisticLogSQLAlchemyRepo
from app.statistic_log.application.service.statistic import StatisticService


class StatisticContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    # Option 1: Use the original asynch-based repository
    statistic_log_repo = Singleton(StatisticLogRepo)
    
    # Option 2: Use the new SQLAlchemy-based repository (recommended)
    statistic_log_sqlalchemy_repo = Singleton(StatisticLogSQLAlchemyRepo)
    
    # Use SQLAlchemy repository by default
    statistic_repository_adapter = Factory(
        StatisticRepositoryAdapter,
        statistic_repo=statistic_log_sqlalchemy_repo,
    )
    statistic_service = Factory(StatisticService, repository=statistic_repository_adapter)
