from unittest import TestCase, mock

from screener.common import date
from screener.exceptions.not_found import DataNotFound
from screener.factories.domain.sector import create_sector


class TestSector(TestCase):
    def setUp(self):
        def _side_effect(data):
            def func(key):
                if key in data:
                    return data[key]
                raise DataNotFound()

            return func

        self.stock1 = mock.Mock(
            get_market_capital=lambda: 20,
            get_pe=lambda: 4,
            get_price_to_book_value=lambda: 7,
            calculate_asset_turnover=lambda x: 2,
            find_financial_year_of_latest_results=lambda: 20,
            find_financial_year_of_latest_income_statement=lambda: 20,
            get_isinid=lambda: "isinid-1",
            get_current_ratio=lambda x: 5,
            get_debt_to_equity_ratio=lambda x: 3,
            get_gross_margin=lambda x: 4,
            calculate_return_on_asset=lambda x: 3,
            get_company_name=lambda: 'hero',
            get_net_sales_for_year=_side_effect({19: 29, 20: 100, 21: 10}),
            get_historical_prices=lambda: [{
                "date": "01-01-2020", "value": 100
            }, {
                "date": "02-01-2020", "value": 105
            }, {
                "date": "03-01-2020", "value": 110
            }, {
                "date": "04-01-2020", "value": 108
            }]
        )

        self.stock2 = mock.Mock(
            get_market_capital=lambda: 50,
            get_pe=lambda: 5,
            get_price_to_book_value=lambda: 3,
            get_debt_to_equity_ratio=lambda x: 1,
            calculate_asset_turnover=lambda x: 2,
            find_financial_year_of_latest_results=lambda: 20,
            find_financial_year_of_latest_income_statement=lambda: 20,
            get_isinid=lambda: "isinid-2",
            get_current_ratio=lambda x: 2,
            get_gross_margin=lambda x: 1,
            calculate_return_on_asset=lambda x: 6,
            get_company_name=lambda: 'bajaj',
            get_net_sales_for_year=_side_effect({19: 23, 20: 300, 21: 100}),
            get_historical_prices=lambda: [{
                "date": "01-01-2020", "value": 220
            }, {
                "date": "02-01-2020", "value": 240
            }, {
                "date": "03-01-2020", "value": 230
            }, {
                "date": "04-01-2020", "value": 200
            }]
        )

        self.stock3 = mock.Mock(
            get_market_capital=lambda: 30,
            get_pe=lambda: 3,
            get_debt_to_equity_ratio=lambda x: 2,
            get_price_to_book_value=lambda: 5,
            calculate_asset_turnover=lambda x: 5,
            find_financial_year_of_latest_results=lambda: 20,
            find_financial_year_of_latest_income_statement=lambda: 20,
            get_isinid=lambda: "isinid-3",
            get_current_ratio=lambda x: 2,
            get_gross_margin=lambda x: 1,
            calculate_return_on_asset=lambda x: 3,
            get_company_name=lambda: 'motocorp',
            get_net_sales_for_year=_side_effect({19: 20, 20: 200, 21: 220}),
            get_historical_prices=lambda: [{
                "date": "01-01-2020", "value": 580
            }, {
                "date": "02-01-2020", "value": 540
            }, {
                "date": "03-01-2020", "value": 500
            }, {
                "date": "04-01-2020", "value": 520
            }]
        )

    @mock.patch.object(date, "current_year", return_value=21)
    @mock.patch("screener.factories.domain.sector.Sector", return_value="sector")
    def test_get_sector_name(self, mocked_sector, mocked_date):
        self.assertEquals("sector", create_sector("auto", [self.stock1, self.stock2, self.stock3]))
        mocked_sector.assert_called_with(
            name='auto',
            market_leader=self.stock2,
            pe=4,
            price_to_book=5,
            asset_turn_over=3,
            current_ratio=3,
            gross_margin=2,
            net_sales=[{'year': 19, 'sale': 72}, {'year': 20, 'sale': 600}, {'year': 21, 'sale': 330}],
            return_on_asset=4,
            debt_to_equity=2,
            market_capital=100,
            historical_values=[],
            stocks=[self.stock1, self.stock2, self.stock3]
        )
        mocked_date.assert_called_with()

    def test_update_and_fetch_metadata__return_one_metadata(self):
        sector = create_sector("auto", [self.stock1, self.stock2, self.stock3])
        sector.update_report_in_metadata("kuch", 3242)
        self.assertDictEqual(sector.get_metadata(), {"report": {"kuch": 3242}})

    def test_update_and_fetch_metadata__update_metadata(self):
        sector = create_sector("auto", [self.stock1, self.stock2, self.stock3])
        sector.update_report_in_metadata("kuch", 3242)
        sector.update_report_in_metadata("bhi", 3242)
        self.assertDictEqual(sector.get_metadata(), {'report': {'bhi': 3242, 'kuch': 3242}})
