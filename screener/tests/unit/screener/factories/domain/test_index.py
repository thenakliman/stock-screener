from unittest import TestCase, mock

from screener.factories.domain.index import get_index


class TestIndex(TestCase):
    @mock.patch("screener.factories.domain.index.get_historical_prices", return_value=[5, 6])
    @mock.patch("screener.factories.domain.index.HistoricalValues", side_effect=lambda x: [1, 2])
    @mock.patch("screener.factories.domain.index.Index", return_value="i-n-d-e-x")
    def test_get_index(self, mocked_data_source, mocked_historical_prices, mocked_get_historical_price):
        data_source_ids = get_index({
            "name": "hero",
            "stocks": ["a", "b"],
            "historical_values": [{"date": 1, "value": 101}, {"date": 2, "value": 102}],
            "current_value": 3124,
            "pe": 3.4,
            "pb": 43.4,
            "free_float": 423343.2,
            "full": 12343,
            "code": "21",
            "category": "ctgry"
        })

        mocked_data_source.assert_called_with(
            "hero",
            ["a", "b"],
            [1, 2],
            3124,
            3.4,
            43.4,
            423343.2,
            12343,
            "21",
            "ctgry")

        self.assertEqual("i-n-d-e-x", data_source_ids)
        mocked_get_historical_price.assert_called()
        mocked_historical_prices.assert_called_with([5, 6])
