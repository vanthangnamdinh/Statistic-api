from abc import ABC, abstractmethod


class StatisticRepo(ABC):
    @abstractmethod
    async def create_log(self, *, data) -> None:
        """Save log"""
