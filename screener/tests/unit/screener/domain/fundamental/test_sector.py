from unittest import TestCase, mock

from screener.domain.fundamental.sector import Sector
from screener.exceptions.not_found import DataNotFound


class TestSector(TestCase):
    @staticmethod
    def _side_effect(data):
        def func(key):
            if key in data:
                return data[key]
            raise DataNotFound()

        return func

    def _sector(self):
        return {
            "name": "auto",
            "stocks": [self.stock1, self.stock2, self.stock3],
            "market_leader": self.stock2,
            "market_capital": 100,
            "pe": 3.8,
            "price_to_book": 2.3,
            "asset_turn_over": 3.4,
            "current_ratio": 1.2,
            "gross_margin": 2.3,
            "net_sales": [{"year": 2019, "sale": 100}, {"year": 2020, "sale": 200}, {"year": 2021, "sale": 300}],
            "return_on_asset": 2.4,
            "debt_to_equity": 0.3,
            "historical_values": [
                {"value": 1}, {"value": 2}, {"value": 3}, {"value": 1}]

        }

    def setUp(self):
        self.stock1 = mock.Mock(
            get_net_sales_for_year=self._side_effect({"20": 100, 2: 10}),
            find_financial_year_of_latest_results=lambda: "20",
            get_company_name=lambda: "hero"
        )
        self.stock2 = mock.Mock(
            get_net_sales_for_year=self._side_effect({"20": 300, 2: 100}),
            find_financial_year_of_latest_results=lambda: "20",
            get_company_name=lambda: "bajaj"
        )
        self.stock3 = mock.Mock(
            get_net_sales_for_year=self._side_effect({"20": 200, 2: 220}),
            find_financial_year_of_latest_results=lambda: "20",
            get_company_name=lambda: "motocorp"
        )

        self.sector = Sector(**self._sector())

    def test_get_sector_name(self):
        self.assertEqual("auto", self.sector.get_sector_name())

    def test_get_market_leader(self):
        self.assertEqual(self.stock2, self.sector.get_market_leader())

    def test_get_market_capital(self):
        self.assertEqual(100, self.sector.get_market_capital())

    def test_get_stocks(self):
        self.assertListEqual([self.stock1, self.stock2, self.stock3], self.sector.get_stocks())

    def test_get_sector_pe(self):
        self.assertEqual(self.sector.get_pe(), 3.8)

    def test_get_price_book_value(self):
        self.assertEqual(self.sector.get_price_to_book_value(), 2.3)

    def test_get_asset_turnover(self):
        self.assertEqual(self.sector.get_asset_turnover(), 3.4)

    def test_get_current_ratio(self):
        self.assertEqual(self.sector.get_current_ratio(), 1.2)

    def test_get_gross_margin(self):
        self.assertEqual(self.sector.get_gross_margin(), 2.3)

    def test_get_return_on_asset(self):
        self.assertEqual(self.sector.get_return_on_asset(), 2.4)

    def test_get_debt_to_equity(self):
        self.assertEqual(self.sector.get_debt_to_equity(), 0.3)

    def test_market_share_of_sale(self):
        self.assertListEqual(
            self.sector.market_share_of_sale(),
            [{'hero': 100}, {'bajaj': 300}, {'motocorp': 200}]
        )

    def test_update_and_fetch_metadata__return_one_metadata(self):
        self.sector.update_report_in_metadata("kuch", 3242)
        self.assertDictEqual(self.sector.get_metadata(), {"report": {"kuch": 3242}})

    def test_update_and_fetch_metadata__update_metadata(self):
        self.sector.update_report_in_metadata("kuch", 3242)
        self.sector.update_report_in_metadata("bhi", 3242)
        self.assertDictEqual(self.sector.get_metadata(), {'report': {'bhi': 3242, 'kuch': 3242}})

    def test_get_more_than_minimum_price(self):
        self.assertEqual(self.sector.get_more_than_minimum_price(0.01), 200)

    def test_get_more_than_minimum_price__when_historical_prices_is_not_available(self):
        sector = self._sector()
        sector["historical_values"] = []
        sector = Sector(**sector)
        self.assertEqual(sector.get_more_than_minimum_price(1), 1000)

    def test_get_less_than_maximum_price__return_100__when_no_stocks(self):
        sector = self._sector()
        sector["historical_values"] = []
        sector = Sector(**sector)
        self.assertEqual(sector.get_less_than_maximum_price(0), 1000)

    def test_get_less_than_maximum_price(self):
        self.assertEqual(self.sector.get_less_than_maximum_price(0.02), 33.333333333333336)

    def test_get_less_than_maximum_price__when_historical_prices_is_less_than_to_be_analysed(self):
        self.assertEqual(self.sector.get_less_than_maximum_price(1), 33.333333333333336)

    def test_increase_in_sales(self):
        self.assertListEqual([{"year": 2020, "increase": 100}, {"year": 2021, "increase": 50}],
                             self.sector.increase_in_sales(2))

    def test_get_net_sales_for_year__when_sales_not_found_for_year(self):
        self.assertListEqual([{"year": 2019, "sale": 100}, {"year": 2020, "sale": 200}, {"year": 2021, "sale": 300}],
                             self.sector.get_net_sales())

    def test_to_dict(self):
        self.assertDictEqual(self.sector.to_dict(), {
            'name': 'auto',
            'pe': 3.8,
            'price_to_book': 2.3,
            'asset_turnover': 3.4,
            'current_ratio': 1.2,
            'gross_margin': 2.3,
            'return_on_asset': 2.4,
            'more_than_minimum': 100.0,
            'less_than_maximum': 33.333333333333336
        })
