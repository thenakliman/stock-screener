from unittest import TestCase, mock

from screener.common.singleton_metaclass import Singleton
from screener.repositories.sector import SectorRepository


class TestSectorClient(TestCase):
    def tearDown(self) -> None:
        Singleton._instances = {}

    @mock.patch("screener.repositories.sector.get_sectors")
    def test_find_all(self, mocked_get_sectors):
        mocked_get = mock.Mock(return_value=[1, 2, 3])
        stock_client = mock.Mock(get_active_stocks=mocked_get)
        mocked_get_sectors.return_value = ["a", "b"]

        sectors = SectorRepository(stock_client).get_all_sectors()

        self.assertListEqual(sectors, ["a", "b"])
        mocked_get.assert_called_with()
        mocked_get_sectors.assert_called_with([1, 2, 3])
