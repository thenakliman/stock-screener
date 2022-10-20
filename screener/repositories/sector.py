from typing import List

from screener.common.singleton_metaclass import Singleton
from screener.domain.fundamental.sector import Sector
from screener.factories.domain.sector import get_sectors


class SectorRepository(metaclass=Singleton):
    def __init__(self, stock_client):
        self._stock_client = stock_client

    def get_all_sectors(self) -> List[Sector]:
        stocks = self._stock_client.get_active_stocks()
        return get_sectors(stocks)
