import unittest
from unittest import mock

from screener.common import date
from screener.domain.technical.day_value import DayValue
from screener.domain.fundamental.index import Index


class IndexTest(unittest.TestCase):
    def test_get_name(self):
        index = Index("bse-sensex", [mock.Mock()], mock.Mock(), 1232, 12, 32, 312321, 423433, "16")

        self.assertEqual(index.get_name(), "bse-sensex")

    def test_get_current_value(self):
        index = Index("bse-sensex", [mock.Mock()],
                      mock.Mock(get_latest_price=lambda: DayValue("12", 1232, 10, 8, 14, 1000)),
                      1232, 12, 32, 312321, 423433, "16")

        self.assertEqual(index.get_current_value(), 1232)

    def test_get_stocks(self):
        stocks = [mock.Mock()]
        index = Index("bse-sensex", stocks, mock.Mock(), 1232, 12, 32, 312321, 423433, "16")
        self.assertListEqual(stocks, index.get_stocks())

    def test_update_metadata(self):
        index = Index("bse-sensex", [mock.Mock()], mock.Mock(), 1232, 12, 32, 312321, 423433, "16")
        metadata = {"key": "value", "k": "v"}
        index.update_report_in_metadata(metadata)
        self.assertDictEqual(metadata, index.get_metadata())

    def test_get_historical_prices(self):
        stocks = [mock.Mock()]
        index = Index("bse-sensex", stocks, mock.Mock(), 1232, 12, 32, 312321, 423433, "16")
        self.assertListEqual(stocks, index.get_stocks())

    def test_update_historical_prices(self):
        stocks = [mock.Mock()]
        historical_prices = mock.Mock()
        index = Index("bse-sensex", stocks, historical_prices, 1232, 12, 32, 312321, 423433, "16")
        prices = [mock.Mock(), mock.Mock()]

        index.update_historical_prices(prices)

        historical_prices.add_latest_price.assert_called_with(prices)

    def test_get_date_of_latest_available_value(self):
        stocks = [mock.Mock()]
        historical_prices = mock.Mock(get_date_of_latest_available_price=lambda: 117)
        index = Index("bse-sensex", stocks, historical_prices, 1232, 12, 32, 312321, 423433, "16")

        self.assertEquals(index.get_date_of_latest_available_value(), 117)

    def test_number_of_days_since_index_formed(self):
        stocks = [mock.Mock()]
        historical_prices = mock.Mock(number_of_days_stock_in_market=lambda: 137)
        index = Index("bse-sensex", stocks, historical_prices, 1232, 12, 32, 312321, 423433, "16")

        self.assertEquals(index.number_of_days_since_index_formed(), 137)

    def test_get_code(self):
        stocks = [mock.Mock()]
        historical_prices = mock.Mock()
        index = Index("bse-sensex", stocks, historical_prices, 1232, 12, 32, 312321, 423433, "16")

        self.assertEqual(index.get_code(), "16")

    def test_maximum_value_in_given_days__when_number_of_historical_prices_greater_than_number(self):
        index = Index("bse-sensex", [mock.Mock()], mock.Mock(maximum_price_in_given_days=lambda x: 14), 10, 12, 32,
                      312321, 423433, "16")
        self.assertEqual(14, index.maximum_value_in_given_days(20))

    def test_maximum_value_in_given_days(self):
        index = Index("bse-sensex",
                      [mock.Mock()],
                      mock.Mock(maximum_price_in_given_days=lambda x: 12), 10, 12, 32, 312321, 423433, "16")
        self.assertEqual(12, index.maximum_value_in_given_days(3))

    def test_minimum_value_in_given_days__when_number_of_historical_prices_greater_than_number(self):
        index = Index("bse-sensex",
                      [mock.Mock()],
                      mock.Mock(maximum_price_in_given_days=lambda x: 14.0), 10, 12, 32, 312321, 423433, "16")
        self.assertEqual(14.0, index.maximum_value_in_given_days(8))

    def test_minimum_value_in_given_days(self):
        index = Index("bse-sensex",
                      [mock.Mock()],
                      mock.Mock(minimum_price_in_given_days=lambda x: 10.0), 10, 12, 32, 312321, 423433, "16")
        self.assertEqual(10.0, index.minimum_value_in_given_days(3))

    def test_category(self):
        index = Index("bse-sensex",
                      [mock.Mock()],
                      mock.Mock(minimum_price_in_given_days=lambda x: 10.0), 10, 12, 32, 312321, 423433, "16", "osk")
        self.assertEqual("osk", index.get_category())

    def test_update_satisfied_strategy__when_one_flow(self):
        index = Index("bse-sensex", [mock.Mock()], mock.Mock(), 1232, 12, 32, 312321, 423433, "16")

        index.update_satisfied_strategy("good-return")

        satisfied_strategies = index.get_satisfied_strategies()
        self.assertListEqual(satisfied_strategies, ["good-return"])

    def test_update_satisfied_strategy__when_multiple_flow(self):
        index = Index("bse-sensex", [mock.Mock()], mock.Mock(), 1232, 12, 32, 312321, 423433, "16")

        index.update_satisfied_strategy("good-return")
        index.update_satisfied_strategy("good-fundamental")

        satisfied_strategies = index.get_satisfied_strategies()
        self.assertListEqual(satisfied_strategies, ["good-return", "good-fundamental"])

    @mock.patch.object(date, "today", return_value="12-12-2020")
    def test_to_dict__return_today_date__for_default_value_of_date_created(self, mocked_date):
        index = Index("bse-sensex", [], mock.Mock(), 1232, 12, 32, 312321, 423433, "16")

        self.assertEqual("12-12-2020", index.to_dict()["date_created"])

    @mock.patch.object(date, "today", return_value="12-12-2020")
    def test_to_dict__return_today_date__for_default_value_of_last_date_updated(self, mocked_date):
        index = Index("bse-sensex", [], mock.Mock(), 1232, 12, 32, 312321, 423433, "16")

        self.assertEqual("12-12-2020", index.to_dict()["last_date_updated"])

    def test_to_dict(self):
        stocks = [mock.Mock(get_isinid=lambda: 1)]
        prices = [1, 2, 3]
        historical_prices = mock.Mock(to_dict=lambda: prices,
                                      get_latest_price=lambda: DayValue("12", 1232, 10, 8, 14, 1000))
        index = Index("bse-sensex", stocks, historical_prices, 1232,
                      12, 32, 312321, 423433, "16", "digd", "20-12-2020", "26-12-2020")

        self.assertDictEqual({
            "name": "bse-sensex",
            "stocks": [1],
            "historical_values": prices,
            "current_value": 1232.0,
            "pe": 12,
            "pb": 32,
            "free_float": 312321,
            "full": 423433,
            "code": "16",
            "_id": "16",
            "category": "digd",
            "date_created": "20-12-2020",
            "last_date_updated": "26-12-2020"
        }, index.to_dict())
