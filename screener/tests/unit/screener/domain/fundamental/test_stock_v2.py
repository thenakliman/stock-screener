from unittest import TestCase, mock

from screener.domain.fundamental.sector import Sector
from screener.domain.fundamental.stock import Stock
from screener.domain.technical.day_value import DayValue
from screener.domain.technical.historical_prices import HistoricalValues
from screener.exceptions.not_found import DataNotFound, CurrentPriceNotFound


class TestStock(TestCase):
    def setUp(self):
        stock_details = self._get_stock_details()
        self.balance_sheet = mock.Mock(
            get_financial_year_of_results=lambda: [2020, 2019, 2018, 2017, 2016])

        self.income_statement = mock.Mock(get_financial_year_of_results=lambda: [2020, 2019, 2018, 2017])
        self.cash_flow = mock.Mock(get_financial_year_of_results=lambda: [2020, 2019, 2018, 2017, 2016])
        self.financial_ratios = mock.Mock(
            find_financial_year_of_latest_results=lambda: 2020,
            get_financial_year_of_results=lambda: [2020, 2019, 2018]
        )
        self.stock = Stock(
            stock_details,
            self.balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)
        self.sector = Sector("consumer", self.stock, 12, 75, 3.4, 2.3, 1.2, 3.4, [{}], 3.4, 2.1, 0.1, [], [self.stock])
        self.stock.update_sector(self.sector)

    @staticmethod
    def _get_stock_details():
        return {
            "industry_pe": 69.28,
            "pe": 73.22,
            "market_capital_full": 502534.84,
            "isinid": "INE030A01027",
            "name": "Hindustan Unilever",
            "put_to_call": 64.4,
            "eps_twelve_month": 29.21,
            "group": "A",
            "face_value": 1.0,
            "dividend_percentage": 3450.0,
            "book_value": 34.26,
            "cash_eps": 35.46,
            "price": 2202.05,
            "industry": "MAN",
            "active": True,
            "sub_industry": "Personal Care",
            "historical_prices": HistoricalValues([
                DayValue("2020-06-19", 2100.8, 2079.0, 2070.0, 2100.0, 4673557),
                DayValue("2020-06-22", 2092.75, 2110.0, 2070.0, 2118.9, 2487252),
            ]),
            "tags": [
                "S&P BSE SENSEX",
                "S&P BSE 100",
                "S&P BSE 200",
                "S&P BSE 500"
            ],
            "sector": "consumer",
            "_id": "INE030A01027",
            "date_created": "20-12-2020",
            "last_date_updated": "26-12-2020",
            "balance_sheet": {
                "total_current_liabilities": [
                    {
                        "year": 2020,
                        "value": 9104.0
                    },
                    {
                        "year": 2019,
                        "value": 8353.0
                    },
                    {
                        "year": 2018,
                        "value": 8636.0
                    },
                    {
                        "year": 2017,
                        "value": 7202.0
                    },
                    {
                        "year": 2016,
                        "value": 6652.0
                    }
                ],
                "total_current_asset": [
                    {
                        "year": 2020,
                        "value": 11908.0
                    },
                    {
                        "year": 2019,
                        "value": 11374.0
                    },
                    {
                        "year": 2018,
                        "value": 11139.0
                    },
                    {
                        "year": 2017,
                        "value": 9365.0
                    },
                    {
                        "year": 2016,
                        "value": 9530.0
                    }
                ],
                "total_non_current_asset": [
                    {
                        "year": 2020,
                        "value": 7694.0
                    },
                    {
                        "year": 2019,
                        "value": 6491.0
                    },
                    {
                        "year": 2018,
                        "value": 6010.0
                    },
                    {
                        "year": 2017,
                        "value": 5386.0
                    },
                    {
                        "year": 2016,
                        "value": 4368.0
                    }
                ],
                "total_shareholders_funds": [
                    {
                        "year": 2020,
                        "value": 8031.0
                    },
                    {
                        "year": 2019,
                        "value": 7659.0
                    },
                    {
                        "year": 2018,
                        "value": 7075.0
                    },
                    {
                        "year": 2017,
                        "value": 6490.0
                    },
                    {
                        "year": 2016,
                        "value": 6279.0
                    }
                ],
                "total_asset": [
                    {
                        "year": 2020,
                        "value": 19602.0
                    },
                    {
                        "year": 2019,
                        "value": 17865.0
                    },
                    {
                        "year": 2018,
                        "value": 17149.0
                    },
                    {
                        "year": 2017,
                        "value": 14751.0
                    },
                    {
                        "year": 2016,
                        "value": 13920.0
                    }
                ],
                "long_term_borrowing": [
                    {
                        "value": 0,
                        "year": 2020
                    },
                    {
                        "value": 0,
                        "year": 2019
                    },
                    {
                        "value": 0,
                        "year": 2018
                    },
                    {
                        "value": 0,
                        "year": 2017
                    },
                    {
                        "value": 0,
                        "year": 2016
                    }
                ],
                "short_term_borrowings": [
                    {
                        "value": 0,
                        "year": 2020
                    },
                    {
                        "value": 0,
                        "year": 2019
                    },
                    {
                        "value": 0,
                        "year": 2018
                    },
                    {
                        "value": 0,
                        "year": 2017
                    },
                    {
                        "value": 0,
                        "year": 2016
                    }
                ]
            },
            "profit_loss_statement": {
                "incomes": [
                    {
                        "year": 2020,
                        "value": 6738.0
                    },
                    {
                        "year": 2019,
                        "value": 6036.0
                    },
                    {
                        "year": 2018,
                        "value": 5237.0
                    },
                    {
                        "year": 2017,
                        "value": 4490.0
                    },
                    {
                        "year": 2016,
                        "value": 4137.0
                    }
                ],
                "net_sales": [
                    {
                        "year": 2020,
                        "value": 38785.0
                    },
                    {
                        "year": 2019,
                        "value": 38224.0
                    },
                    {
                        "year": 2018,
                        "value": 34525.0
                    },
                    {
                        "year": 2017,
                        "value": 31890.0
                    },
                    {
                        "year": 2016,
                        "value": 31061.0
                    }
                ],
                "total_expenses": [
                    {
                        "year": 2020,
                        "value": 29306.0
                    },
                    {
                        "year": 2019,
                        "value": 29575.0
                    },
                    {
                        "year": 2018,
                        "value": 27320.0
                    },
                    {
                        "year": 2017,
                        "value": 25687.0
                    },
                    {
                        "year": 2016,
                        "value": 25225.0
                    }
                ],
                "issued_shares": [
                    {
                        "year": 2020,
                        "value": 21647.04
                    },
                    {
                        "year": 2019,
                        "value": 21647.04
                    },
                    {
                        "year": 2018,
                        "value": 21645.29
                    },
                    {
                        "year": 2017,
                        "value": 21643.5
                    },
                    {
                        "year": 2016,
                        "value": 21639.37
                    }
                ]
            },
            "cash_flows": {
                "cash_flows": [
                    {
                        "year": 2020,
                        "value": 7305.0
                    },
                    {
                        "year": 2019,
                        "value": 5728.0
                    },
                    {
                        "year": 2018,
                        "value": 5916.0
                    },
                    {
                        "year": 2017,
                        "value": 4953.0
                    },
                    {
                        "year": 2016,
                        "value": 3974.0
                    }
                ]
            },
            "financial_ratios": {
                "current_ratios": [
                    {
                        "year": 2020,
                        "value": 1.08
                    },
                    {
                        "year": 2019,
                        "value": 1.0
                    },
                    {
                        "year": 2018,
                        "value": 0.94
                    },
                    {
                        "year": 2017,
                        "value": 0.82
                    },
                    {
                        "year": 2016,
                        "value": 1.03
                    }
                ],
                "gross_margins": [
                    {
                        "year": 2020,
                        "value": 22.33
                    },
                    {
                        "year": 2019,
                        "value": 21.22
                    },
                    {
                        "year": 2018,
                        "value": 19.69
                    },
                    {
                        "year": 2017,
                        "value": 17.72
                    },
                    {
                        "year": 2016,
                        "value": 17.47
                    }
                ],
                "asset_turnover_ratios": [
                    {
                        "year": 2020,
                        "value": 4.94
                    },
                    {
                        "year": 2019,
                        "value": 5.19
                    },
                    {
                        "year": 2018,
                        "value": 5.09
                    },
                    {
                        "year": 2017,
                        "value": 4.99
                    },
                    {
                        "year": 2016,
                        "value": 6.21
                    }
                ],
                "return_on_assets": [
                    {
                        "year": 2020,
                        "value": 37.1
                    },
                    {
                        "year": 2019,
                        "value": 35.38
                    },
                    {
                        "year": 2018,
                        "value": 32.69
                    },
                    {
                        "year": 2017,
                        "value": 29.99
                    },
                    {
                        "year": 2016,
                        "value": 29.02
                    }
                ]
            }
        }

    def test_get_price_to_book_value(self):
        self.assertEqual(64.25590895827256, self.stock.get_price_to_book_value())

    def test_mark_leader(self):
        self.stock.mark_market_leader()
        self.assertTrue(self.stock._market_leader)

    def test_default_value_of_market_leader_is_false(self):
        self.stock.market_leader()
        self.assertFalse(self.stock.market_leader())

    def test_find_financial_year_of_latest_balance_sheet(self):
        stock_details = self._get_stock_details()
        self.stock = Stock(stock_details,
                           mock.Mock(get_latest_financial_year_of_result=lambda: 2020), None, None, None)

        self.assertEquals(2020, self.stock.find_financial_year_of_latest_balance_sheet())

    def test_find_financial_year_of_latest_balance_sheet__returns_21__when(self):
        stock_details = self._get_stock_details()
        balance_sheet = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2021))

        self.stock = Stock(stock_details, balance_sheet, None, None, None)

        self.assertEquals(2021, self.stock.find_financial_year_of_latest_balance_sheet())

    def test_find_financial_year_of_latest_balance_sheet__returns_21__when_balance_sheet_has_latest_info(self):
        stock_details = self._get_stock_details()
        balance_sheet = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2021))
        income_statement = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2020))
        cash_flow = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2020))

        self.stock = Stock(stock_details, balance_sheet, income_statement, cash_flow, None)

        self.assertEquals(2020, self.stock.find_financial_year_of_latest_results())

    def test_find_financial_year_of_latest_balance_sheet__returns_21__when_income_statement_has_latest_info(self):
        stock_details = self._get_stock_details()
        balance_sheet = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2020))
        income_statement = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2021))
        cash_flow = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2020))

        self.stock = Stock(stock_details, balance_sheet, income_statement, cash_flow, None)

        self.assertEquals(2020, self.stock.find_financial_year_of_latest_results())

    def test_find_financial_year_of_latest_balance_sheet__returns_21__when_cash_flow_has_latest_info(self):
        stock_details = self._get_stock_details()
        balance_sheet = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2020))
        income_statement = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2020))
        cash_flow = mock.Mock(get_latest_financial_year_of_result=mock.Mock(return_value=2021))

        self.stock = Stock(stock_details, balance_sheet, income_statement, cash_flow, None)

        self.assertEquals(2020, self.stock.find_financial_year_of_latest_results())

    def test_default_value_of_market_leader_is_overridable(self):
        self.stock.mark_market_leader()
        self.assertTrue(self.stock.market_leader())

    def test_get_price_to_book_value__defined_value__when_book_value_is_zero(self):
        stock_details = self._get_stock_details()
        stock_details["book_value"] = 0

        price_to_book_value = Stock(stock_details,
                                    self.balance_sheet,
                                    self.income_statement,
                                    self.cash_flow,
                                    self.financial_ratios).get_price_to_book_value()

        self.assertEqual(220205.0, price_to_book_value)

    def test_get_industry_price_to_book_value(self):
        stock_details = self._get_stock_details()
        stock_details["book_value"] = 0
        stock = Stock(stock_details, self.balance_sheet, self.income_statement, self.cash_flow, self.financial_ratios)
        stock.update_sector(mock.Mock(get_price_to_book_value=lambda: 1))
        price_to_book_value = stock.get_industry_price_to_book_value()

        self.assertEqual(1, price_to_book_value)

    def test_price_to_book_less_than_industry__true(self):
        stock_details = self._get_stock_details()
        stock_details["book_value"] = 200
        stock = Stock(stock_details, self.balance_sheet, self.income_statement, self.cash_flow, self.financial_ratios)
        stock.update_sector(mock.Mock(get_price_to_book_value=lambda: 12))
        self.assertTrue(stock.price_to_book_less_than_industry(5))

    def test_price_to_book_less_than_industry__false(self):
        stock_details = self._get_stock_details()
        stock_details["book_value"] = 150
        stock = Stock(stock_details, self.balance_sheet, self.income_statement, self.cash_flow, self.financial_ratios)
        stock.update_sector(mock.Mock(get_price_to_book_value=lambda: 12))
        self.assertFalse(stock.price_to_book_less_than_industry(5))

    def test_has_tags__true__stock_has_tagged(self):
        self.assertTrue(self.stock.has_tags(["S&P BSE 200"]))

    def test_has_tags__false__stock_does_not_have_tag(self):
        self.assertFalse(self.stock.has_tags(["S&P BSE"]))

    def test_has_tags__true__tag_checks_are_case_insensitive(self):
        self.assertTrue(self.stock.has_tags(["s&p BSe sENsEx"]))

    def test_has_tags__true__when_multiple_tags_match(self):
        self.assertTrue(self.stock.has_tags(["s&p BSe sENsEx", "S&P BSE 200"]))

    def test_get_pe(self):
        self.assertEqual(73.22, self.stock.get_pe())

    def test_pe_is_less_than_sector_pe__true__pe_is_less_than_sector_pe(self):
        self.assertTrue(self.stock.pe_is_less_than_sector_pe())

    def test_pe_is_less_than_sector_pe__false__pe_is_greater_than_sector_pe(self):
        sector = mock.Mock(get_pe=lambda: 78)
        self.stock.update_sector(sector)

        self.assertTrue(self.stock.pe_is_less_than_sector_pe())

    def test_pe_is_less_than_sector_pe__true__pe_is_equal_to_sector_pe(self):
        sector = mock.Mock(get_pe=lambda: 73.22)
        self.stock.update_sector(sector)
        self.assertTrue(self.stock.pe_is_less_than_sector_pe())

    def test_get_isinid(self):
        self.assertEqual("INE030A01027", self.stock.get_isinid())

    def test_get_industry_pe(self):
        self.assertEqual(69.28, self.stock.get_industry_pe())

    def test_get_market_capital(self):
        self.assertEqual(502534.84, self.stock.get_market_capital())

    def test_number_of_days_stock_in_market(self):
        stock_details = self._get_stock_details()
        number_of_days_stock_in_market = mock.Mock(return_value=1020)
        historical_prices = mock.Mock(number_of_days_stock_in_market=number_of_days_stock_in_market)
        stock_details["historical_prices"] = historical_prices

        stock = Stock(stock_details, None, None, None, None)

        self.assertEqual(1020, stock.number_of_days_stock_in_market())
        number_of_days_stock_in_market.assert_called_with()

    def test_minimum_price_in_given_days(self):
        stock_details = self._get_stock_details()
        minimum_price_in_given_days = mock.Mock(return_value=1020)
        historical_prices = mock.Mock(minimum_price_in_given_days=minimum_price_in_given_days)
        stock_details["historical_prices"] = historical_prices

        stock = Stock(stock_details, None, None, None, None)

        self.assertEqual(1020, stock.minimum_price_in_given_days(5))
        minimum_price_in_given_days.assert_called_with(5)

    def test_maximum_price_in_given_days(self):
        stock_details = self._get_stock_details()
        maximum_price_in_given_days = mock.Mock(return_value=1020)
        historical_prices = mock.Mock(maximum_price_in_given_days=maximum_price_in_given_days)
        stock_details["historical_prices"] = historical_prices

        stock = Stock(stock_details, None, None, None, None)

        self.assertEqual(1020, stock.maximum_price_in_given_days(5))
        maximum_price_in_given_days.assert_called_with(5)

    def test_get_current_price(self):
        stock_details = self._get_stock_details()
        get_current_price = mock.Mock(return_value=12323.65)
        historical_prices = mock.Mock(get_current_price=get_current_price)
        stock_details["historical_prices"] = historical_prices

        self.stock = Stock(stock_details, None, None, None, None)

        self.assertEqual(12323.65, self.stock.get_current_price())

    def test_get_current_price__raise_exception__when_price_is_none(self):
        stock_details = self._get_stock_details()
        get_current_price = mock.Mock(return_value=None)
        historical_prices = mock.Mock(get_current_price=get_current_price)
        stock_details["historical_prices"] = historical_prices

        self.stock = Stock(stock_details, None, None, None, None)

        with self.assertRaises(CurrentPriceNotFound):
            self.stock.get_current_price()

    def test_get_company_name(self):
        self.assertEqual("Hindustan Unilever", self.stock.get_company_name())

    def test_get_group(self):
        self.assertEqual("A", self.stock.get_group())

    def test_increasing_current_ratio__true__when_current_ratio_is_increasing(self):
        increasing_current_ratio = mock.Mock(return_value=True)
        balance_sheet = mock.Mock(increasing_current_ratio=increasing_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(self.stock.increasing_current_ratio(2020))
        increasing_current_ratio.assert_called_with(2020)

    def test_increasing_current_ratio__false__when_current_ratio_is_decreasing(self):
        increasing_current_ratio = mock.Mock(return_value=False)
        balance_sheet = mock.Mock(increasing_current_ratio=increasing_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertFalse(self.stock.increasing_current_ratio(2020))
        increasing_current_ratio.assert_called_with(2020)

    def test_increasing_current_ratio__true__when_current_ratio_increasing__balance_sheet_is_none(self):
        increasing_current_ratio = mock.Mock(return_value=True)
        financial_ratio = mock.Mock(increasing_current_ratio=increasing_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            None,
            self.income_statement,
            self.cash_flow,
            financial_ratio)

        self.assertTrue(self.stock.increasing_current_ratio(2020))
        increasing_current_ratio.assert_called_with(2020)

    def test_increasing_current_ratio__false__when_current_ratio_decreasing__balance_sheet_is_none(self):
        increasing_current_ratio = mock.Mock(return_value=False)
        financial_ratios = mock.Mock(increasing_current_ratio=increasing_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            None,
            self.income_statement,
            self.cash_flow,
            financial_ratios)

        self.assertFalse(self.stock.increasing_current_ratio(2020))
        increasing_current_ratio.assert_called_with(2020)

    def test_current_ratio_is_greater_than_sector__true__when_current_ratio_is_greater_than_sector(self):
        calculate_current_ratio = mock.Mock(return_value=1.3)
        balance_sheet = mock.Mock(get_current_ratio=calculate_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_current_ratio=lambda: 1)
        self.stock.update_sector(sector)

        self.assertTrue(self.stock.current_ratio_is_greater_than_sector(2020))
        calculate_current_ratio.assert_called_with(2020)

    def test_current_ratio_is_greater_than_sector__false__when_current_ratio_is_less_than_sector(self):
        calculate_current_ratio = mock.Mock(return_value=1.1)
        balance_sheet = mock.Mock(get_current_ratio=calculate_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_current_ratio=lambda: 1.2)
        self.stock.update_sector(sector)

        self.assertFalse(self.stock.current_ratio_is_greater_than_sector(2020))
        calculate_current_ratio.assert_called_with(2020)

    def test_current_ratio_is_greater_than_sector__true__when_current_ratio_is_equal_to_sector(self):
        calculate_current_ratio = mock.Mock(return_value=1.2)
        balance_sheet = mock.Mock(get_current_ratio=calculate_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_current_ratio=lambda: 1.1)
        self.stock.update_sector(sector)

        self.assertTrue(self.stock.current_ratio_is_greater_than_sector(2020))
        calculate_current_ratio.assert_called_with(2020)

    def test_current_ratio_is_greater_than_sector__true__balance_sheet_is_none(self):
        get_current_ratio = mock.Mock(return_value=1.3)
        financial_ratios = mock.Mock(get_current_ratio=get_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            None,
            self.income_statement,
            self.cash_flow,
            financial_ratios)
        sector = mock.Mock(get_current_ratio=lambda: 1)
        self.stock.update_sector(sector)

        self.assertTrue(self.stock.current_ratio_is_greater_than_sector(2020))
        get_current_ratio.assert_called_with(2020)

    def test_current_ratio_is_greater_than_sector__false__balance_sheet_is_none(self):
        get_current_ratio = mock.Mock(return_value=1.1)
        financial_ratio = mock.Mock(get_current_ratio=get_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            None,
            self.income_statement,
            self.cash_flow,
            financial_ratio)
        sector = mock.Mock(get_current_ratio=lambda: 1.2)
        self.stock.update_sector(sector)

        self.assertFalse(self.stock.current_ratio_is_greater_than_sector(2020))
        get_current_ratio.assert_called_with(2020)

    def test_current_ratio_is_greater_than_sector__true__when_equal_current_and_balance_none(self):
        calculate_current_ratio = mock.Mock(return_value=1.2)
        balance_sheet = mock.Mock(get_current_ratio=calculate_current_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_current_ratio=lambda: 1.1)
        self.stock.update_sector(sector)

        self.assertTrue(self.stock.current_ratio_is_greater_than_sector(2020))
        calculate_current_ratio.assert_called_with(2020)

    def test_get_graham_number__0__when_maximum_allowed_eps_is_zero(self):
        self.assertEqual(0, self.stock.get_graham_number(0, 1))

    def test_get_graham_number__0__when_maximum_allowed_book_value(self):
        self.assertEqual(0, self.stock.get_graham_number(1, 0))

    def test_get_graham_number(self):
        self.assertEqual(316.3438951520955, self.stock.get_graham_number(10, 10))

    def test_add_prices(self):
        stock_details = self._get_stock_details()
        add_latest_price = mock.Mock(return_value=1232)
        historical_prices = mock.Mock(add_latest_price=add_latest_price)
        stock_details["historical_prices"] = historical_prices
        stock = Stock(stock_details, None, None, None, None)

        prices = [DayValue("12-12-2020", 12, 12, 12, 12, 23)]
        stock.add_prices(prices)

        add_latest_price.mock_assert_called_with(prices)

    def test_get_debt(self):
        get_total_debt = mock.Mock(return_value=2300)
        balance_sheet = mock.Mock(get_total_debt=get_total_debt)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(2300, self.stock.get_debt(2020))
        get_total_debt.assert_called_with(2020)

    def test_decreasing_long_term_debt_ratio_by_year__true__when_long_term_debt_decreasing(self):
        decreasing_long_term_debt_ratio_by_year = mock.Mock(return_value=True)
        balance_sheet = mock.Mock(decreasing_long_term_debt_ratio_by_year=decreasing_long_term_debt_ratio_by_year)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(self.stock.decreasing_long_term_debt_ratio_by_year(2020))
        decreasing_long_term_debt_ratio_by_year.assert_called_with(2020)

    def test_decreasing_long_term_debt_ratio_by_year__false__when_long_term_debt_increasing(self):
        decreasing_long_term_debt_ratio_by_year = mock.Mock(return_value=False)
        balance_sheet = mock.Mock(decreasing_long_term_debt_ratio_by_year=decreasing_long_term_debt_ratio_by_year)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertFalse(self.stock.decreasing_long_term_debt_ratio_by_year(2020))
        decreasing_long_term_debt_ratio_by_year.assert_called_with(2020)

    def test_get_long_term_debts(self):
        get_long_term_debts = mock.Mock(return_value=3948)
        balance_sheet = mock.Mock(get_long_term_debts=get_long_term_debts)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(3948, self.stock.get_long_term_debts(2020))
        get_long_term_debts.assert_called_with(2020)

    def test_get_debt_to_equity_ratio(self):
        get_debt_to_equity_ratio = mock.Mock(return_value=384)
        balance_sheet = mock.Mock(get_debt_to_equity_ratio=get_debt_to_equity_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(384, self.stock.get_debt_to_equity_ratio(2020))
        get_debt_to_equity_ratio.assert_called_with(2020)

    def test_get_debt_to_equity_ratio__when_fails(self):
        get_debt_to_equity_ratio = mock.Mock(side_effect=Exception)
        balance_sheet = mock.Mock(get_debt_to_equity_ratio=get_debt_to_equity_ratio)
        self.stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(-1, self.stock.get_debt_to_equity_ratio(2020))
        get_debt_to_equity_ratio.assert_called_with(2020)

    def test_get_sector_debt_to_equity(self):
        self.stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            self.income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.stock.update_sector(mock.Mock(get_debt_to_equity=lambda: 100))
        self.assertEqual(100, self.stock.get_sector_debt_to_equity())

    def test_debt_to_equity_is_less_than_industry__true(self):
        self.stock = Stock(
            self._get_stock_details(),
            mock.Mock(get_latest_financial_year_of_result=lambda: 2020,
                      get_debt_to_equity_ratio=lambda: 94),
            mock.Mock(get_latest_financial_year_of_result=lambda: 2020),
            mock.Mock(get_latest_financial_year_of_result=lambda: 2020),
            mock.Mock(get_latest_financial_year_of_result=lambda: 2020)
        )

        self.stock.update_sector(mock.Mock(get_debt_to_equity=lambda: 100))
        self.assertTrue(self.stock.debt_to_equity_is_less_than_industry(5))

    def test_debt_to_equity_is_less_than_industry__false(self):
        self.stock = Stock(
            self._get_stock_details(),
            mock.Mock(get_latest_financial_year_of_result=lambda: 2020,
                      get_debt_to_equity_ratio=lambda x: 96),
            mock.Mock(get_latest_financial_year_of_result=lambda: 2020),
            mock.Mock(get_latest_financial_year_of_result=lambda: 2020),
            mock.Mock(get_latest_financial_year_of_result=lambda: 2020)
        )

        self.stock.update_sector(mock.Mock(get_debt_to_equity=lambda: 100))
        self.assertFalse(self.stock.debt_to_equity_is_less_than_industry(5))

    def test_increasing_gross_margin__true__when_gross_margin_increasing(self):
        increasing_gross_margin = mock.Mock(return_value=True)
        income_statement = mock.Mock(increasing_gross_margin=increasing_gross_margin)
        self.stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(self.stock.increasing_gross_margin(2020))
        increasing_gross_margin.assert_called_with(2020)

    def test_increasing_gross_margin__false__when_gross_margin_increasing(self):
        increasing_gross_margin = mock.Mock(return_value=False)
        income_statement = mock.Mock(increasing_gross_margin=increasing_gross_margin)
        self.stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertFalse(self.stock.increasing_gross_margin(2020))
        increasing_gross_margin.assert_called_with(2020)

    def test_increasing_gross_margin__true__income_statement_is_none(self):
        increasing_gross_margin = mock.Mock(return_value=True)
        financial_ratios = mock.Mock(increasing_gross_margin=increasing_gross_margin)
        self.stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            None,
            self.cash_flow,
            financial_ratios)

        self.assertTrue(self.stock.increasing_gross_margin(2020))
        increasing_gross_margin.assert_called_with(2020)

    def test_increasing_gross_margin__false__when_income_statement_is_none(self):
        increasing_gross_margin = mock.Mock(return_value=False)
        financial_ratios = mock.Mock(increasing_gross_margin=increasing_gross_margin)
        self.stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            None,
            self.cash_flow,
            financial_ratios)

        self.assertFalse(self.stock.increasing_gross_margin(2020))
        increasing_gross_margin.assert_called_with(2020)

    def test_gross_margin_is_greater_than_sector__true__when_gross_margin_more_than_sector(self):
        get_gross_margin = mock.Mock(return_value=0.35)
        income_statement = mock.Mock(get_gross_margin=get_gross_margin)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_gross_margin=lambda: 0.34)
        stock.update_sector(sector)

        self.assertTrue(stock.gross_margin_is_greater_than_sector(2020))
        get_gross_margin.assert_called_with(2020)

    def test_gross_margin_is_greater_than_sector__false__when_gross_margin_less_than_sector(self):
        get_gross_margin = mock.Mock(return_value=0.33)
        income_statement = mock.Mock(get_gross_margin=get_gross_margin)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_gross_margin=lambda: 0.34)
        stock.update_sector(sector)

        self.assertFalse(stock.gross_margin_is_greater_than_sector(2020))
        get_gross_margin.assert_called_with(2020)

    def test_gross_margin_is_greater_than_sector__false__when_gross_margin_equal_to_sector(self):
        get_gross_margin = mock.Mock(return_value=0.34)
        income_statement = mock.Mock(get_gross_margin=get_gross_margin)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_gross_margin=lambda: 0.34)
        stock.update_sector(sector)

        self.assertTrue(stock.gross_margin_is_greater_than_sector(2020))
        get_gross_margin.assert_called_with(2020)

    def test_get_net_income(self):
        get_net_income = mock.Mock(return_value=67876)
        income_statement = mock.Mock(get_net_income=get_net_income)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(67876, stock.get_net_income(2020))
        get_net_income.assert_called_with(2020)

    def test_get_issued_shares(self):
        get_issued_shares = mock.Mock(return_value=67876)
        income_statement = mock.Mock(get_issued_shares=get_issued_shares)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(67876, stock.get_issued_shares(2020))
        get_issued_shares.assert_called_with(2020)

    def test_new_shares_issued(self):
        new_shares_issued = mock.Mock(return_value=42343)
        income_statement = mock.Mock(new_shares_issued=new_shares_issued)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(42343, stock.new_shares_issued(2020))

    def test_get_new_issued_shares(self):
        get_new_shares_issued = mock.Mock(return_value=42343)
        income_statement = mock.Mock(get_new_shares_issued=get_new_shares_issued)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(42343, stock.get_new_issued_shares(2020))

    def test_increasing_return_on_asset(self):
        financial_ratios = mock.Mock(increasing_return_on_asset=lambda x: True)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            None,
            self.cash_flow,
            financial_ratios)

        self.assertTrue(stock.increasing_return_on_asset(2020))

    def test_increasing_return_on_asset__true__when_roa_is_increasing(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 763443, 2019: 684258}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 823443, 2019: 986879, 2018: 999999}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.increasing_return_on_asset(2020))

    def test_increasing_return_on_asset__false__when_roa_is_decreasing(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 684258, 2019: 763443}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 986879, 2019: 823443, 2018: 12435}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertFalse(stock.increasing_return_on_asset(2020))

    def test_increasing_return_on_asset__true__when_roa_is_equal(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 6, 2019: 5, 2018: 2312}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 30, 2019: 25, 2018: 35}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.increasing_return_on_asset(2020))

    def test_calculate_return_on_asset__zero__when_income_zero(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 0, 2019: 684258}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 823443, 2019: 986879}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(0, stock.calculate_return_on_asset(2020))

    def test_calculate_return_on_asset(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 684258, 2019: 684258}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 823443, 2019: 986879}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(0.6933555107226366, stock.calculate_return_on_asset(2020))

    def test_calculate_return_on_asset_is_greater_than_sector__true(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 684258, 2019: 684258}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 823443, 2019: 986879}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_return_on_asset=lambda: 0.6)
        stock.update_sector(sector)

        self.assertTrue(stock.return_on_asset_is_greater_than_sector(2020))

    def test_calculate_return_on_asset_is_greater_than_sector__false(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 684258, 2019: 684258}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 823443, 2019: 986879}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_return_on_asset=lambda: 0.7)
        stock.update_sector(sector)

        self.assertFalse(stock.return_on_asset_is_greater_than_sector(2020))

    def test_calculate_return_on_asset_is_greater_than_sector__true__when_equal(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 684258, 2019: 684258}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 823443, 2019: 986879}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_return_on_asset=lambda: 0.6933555107226366)
        stock.update_sector(sector)

        self.assertTrue(stock.return_on_asset_is_greater_than_sector(2020))

    def test_net_sale_increasing__true__when_sale_increasing(self):
        income_statement = mock.Mock(get_net_income=lambda x: {2020: 684258, 2019: 684258}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 823443, 2019: 986879}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_return_on_asset=lambda: 0.6933555107226366)
        stock.update_sector(sector)

        self.assertTrue(stock.return_on_asset_is_greater_than_sector(2020))

    def test_net_sale_increasing__true__when_sales_increasing(self):
        net_sale_increasing = mock.Mock(return_value=True)
        income_statement = mock.Mock(net_sale_increasing=net_sale_increasing)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.net_sale_increasing(2020, 3))
        net_sale_increasing.assert_called_with(2020, 3, 0.1)

    def test_net_sale_increasing__false__when_sales_decreasing(self):
        net_sale_increasing = mock.Mock(return_value=False)
        income_statement = mock.Mock(net_sale_increasing=net_sale_increasing)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertFalse(stock.net_sale_increasing(2020, 3))
        net_sale_increasing.assert_called_with(2020, 3, 0.1)

    def test_net_sale_increasing__true__when_sales_are_equal(self):
        net_sale_increasing = mock.Mock(return_value=True)
        income_statement = mock.Mock(net_sale_increasing=net_sale_increasing)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.net_sale_increasing(2020, 3))
        net_sale_increasing.assert_called_with(2020, 3, 0.1)

    def test_net_sale_compare_to_sector(self):
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            mock.Mock(net_sale_compare_to_sector=lambda x, y: [1, 2, 3]),
            self.cash_flow,
            self.financial_ratios)

        sector = mock.Mock(increase_in_sales=lambda x: [{"increase": 20, "year": 2021}])
        stock.update_sector(sector)

        self.assertEquals([1, 2, 3], stock.net_sale_compare_to_sector(2, 5))

    def test_net_income_increasing__true__when_sales_increasing(self):
        net_income_increasing = mock.Mock(return_value=True)
        income_statement = mock.Mock(net_income_increasing=net_income_increasing)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.net_income_increasing(2020, 3, 0.1))
        net_income_increasing.assert_called_with(2020, 3, 0.1)

    def test_net_income_increasing__false__when_sales_decreasing(self):
        net_income_increasing = mock.Mock(return_value=False)
        income_statement = mock.Mock(net_income_increasing=net_income_increasing)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertFalse(stock.net_income_increasing(2020, 3, 0.1))
        net_income_increasing.assert_called_with(2020, 3, 0.1)

    def test_net_income_increasing__true__when_sales_are_equal(self):
        net_income_increasing = mock.Mock(return_value=True)
        income_statement = mock.Mock(net_income_increasing=net_income_increasing)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.net_income_increasing(2020, 3, 0.1))
        net_income_increasing.assert_called_with(2020, 3, 0.1)

    def test_get_date_of_latest_available_price(self):
        stock_details = self._get_stock_details()
        historical_prices = mock.Mock(get_date_of_latest_available_price=lambda: "13-12-2020")
        stock_details["historical_prices"] = historical_prices
        stock = Stock(
            stock_details,
            self.balance_sheet,
            None,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual("13-12-2020", stock.get_date_of_latest_available_price())

    def test_get_historical_prices(self):
        stock_details = self._get_stock_details()
        historical_prices = mock.Mock(to_dict=lambda: "dictionary")
        stock_details["historical_prices"] = historical_prices
        stock = Stock(
            stock_details,
            self.balance_sheet,
            None,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual("dictionary", stock.get_historical_prices())

    def test_increasing_asset_turnover_ratio__true__when_asset_turnover_is_increasing(self):
        income_statement = mock.Mock(
            get_net_sales=lambda x: {2020: 963443, 2019: 684258, 2018: 694258}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 823443, 2019: 986879, 2018: 867687}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.increasing_asset_turnover_ratio(2020))

    def test_increasing_asset_turnover_ratio__false__when_asset_turnover_is_decreasing(self):
        income_statement = mock.Mock(
            get_net_sales=lambda x: {2020: 2, 2019: 3, 2018: 4}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 4, 2019: 12, 2018: 15}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertFalse(stock.increasing_asset_turnover_ratio(2020))

    def test_increasing_asset_turnover_ratio__true__when_asset_turnover_is_equal(self):
        income_statement = mock.Mock(
            get_net_sales=lambda x: {2020: 3, 2019: 3, 2018: 4}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 4, 2019: 15, 2018: 15}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.increasing_asset_turnover_ratio(2020))

    def test_net_sale_increased_by__true(self):
        stock = Stock(
            self._get_stock_details(),
            mock.Mock(),
            mock.Mock(net_sale_increased_by=lambda x, y, z: True),
            self.cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.net_sale_increased_by(2020, 5, 20))

    def test_net_sale_increased_by__false(self):
        stock = Stock(
            self._get_stock_details(),
            mock.Mock(),
            mock.Mock(net_sale_increased_by=lambda x, y, z: False),
            self.cash_flow,
            self.financial_ratios)

        self.assertFalse(stock.net_sale_increased_by(2020, 5, 20))

    def test_increasing_asset_turnover_ratio__income_statement_is_none(self):
        financial_ratios = mock.Mock(increasing_asset_turnover_ratio=lambda x: "weird")
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            None,
            self.cash_flow,
            financial_ratios)

        self.assertEqual("weird", stock.increasing_asset_turnover_ratio(2020))

    def test_asset_turnover_is_greater_than_sector__true__sector_at_gt_stock(self):
        income_statement = mock.Mock(
            get_net_sales=lambda x: {2020: 8, 2019: 4, 2018: 2}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 16, 2019: 6, 2018: 2}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_asset_turnover=lambda: 0.2)
        stock.update_sector(sector)

        self.assertTrue(stock.asset_turnover_is_greater_than_sector(2020))

    def test_asset_turnover_is_greater_than_sector__false__when_asset_turnover_is_decreasing(self):
        income_statement = mock.Mock(
            get_net_sales=lambda x: {2020: 2, 2019: 3, 2018: 4}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 4, 2019: 12, 2018: 15}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_asset_turnover=lambda: 0.2)
        stock.update_sector(sector)

        self.assertFalse(stock.asset_turnover_is_greater_than_sector(2020))

    def test_asset_turnover_is_greater_than_sector_ratio__true__when_asset_turnover_is_equal(self):
        income_statement = mock.Mock(
            get_net_sales=lambda x: {2020: 3, 2019: 3, 2018: 4}[x])
        balance_sheet = mock.Mock(get_asset=lambda x: {2020: 4, 2019: 15, 2018: 15}[x])
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        sector = mock.Mock(get_asset_turnover=lambda: 0.19986675549633579)
        stock.update_sector(sector)

        self.assertTrue(stock.asset_turnover_is_greater_than_sector(2020))

    def test_positive_cash_flow(self):
        cash_flow = mock.Mock(positive_cash_flow=lambda x: "weird" if x == 2020 else "invalid")
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            self.income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertEqual("weird", stock.positive_cash_flow(2020))

    def test_positive_cash_flow__return_false__when_cash_flow_data_not_found(self):
        cash_flow = mock.Mock(positive_cash_flow=mock.Mock(side_effect=DataNotFound))
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            self.income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertFalse(stock.positive_cash_flow(2020))

    def test_get_operating_cash_flow_ratio(self):
        get_asset = mock.Mock(return_value=67808)
        balance_sheet = mock.Mock(get_asset=get_asset)
        get_cash_flow = mock.Mock(return_value=65453)
        cash_flow = mock.Mock(get_cash_flow=get_cash_flow)
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertEqual(0.9652694423564414, stock.get_operating_cash_flow_ratio(2020))
        get_asset.assert_called_with(2019)
        get_cash_flow.assert_called_with(2020)

    def test_get_cash_flow_ratio__return_minus_one__when_balance_sheet_data_not_found_exception(self):
        get_asset = mock.Mock(side_effect=DataNotFound)
        balance_sheet = mock.Mock(get_asset=get_asset)
        get_cash_flow = mock.Mock(return_value=65453)
        cash_flow = mock.Mock(get_cash_flow=get_cash_flow)
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertEqual(-1, stock.get_operating_cash_flow_ratio(2020))
        get_asset.assert_called_with(2019)
        get_cash_flow.assert_called_with(2020)

    def test_get_cash_flow_ratio__return_minus_one__when_cash_flow_data_not_found_exception(self):
        get_asset = mock.Mock(return_value=67808)
        balance_sheet = mock.Mock(get_asset=get_asset)
        get_cash_flow = mock.Mock(side_effect=DataNotFound)
        cash_flow = mock.Mock(get_cash_flow=get_cash_flow)
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertEqual(-1, stock.get_operating_cash_flow_ratio(2020))
        get_cash_flow.assert_called_with(2020)

    def test_get_operating_cash_flow_ratio__when_asset_is_zero_in_previous_year(self):
        get_asset = mock.Mock(return_value=0)
        balance_sheet = mock.Mock(get_asset=get_asset)
        get_cash_flow = mock.Mock(return_value=2)
        cash_flow = mock.Mock(get_cash_flow=get_cash_flow)
        stock = Stock(
            self._get_stock_details(),
            balance_sheet,
            self.income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertEqual(200, stock.get_operating_cash_flow_ratio(2020))
        get_asset.assert_called_with(2019)
        get_cash_flow.assert_called_with(2020)

    def test_update_cash_flow(self):
        positive_cash_flow = mock.Mock()
        cash_flow = mock.Mock(positive_cash_flow=positive_cash_flow)

        self.stock.update_cash_flow(cash_flow)
        self.stock.positive_cash_flow(2020)

        positive_cash_flow.assert_called_with(2020)

    def test_update_sector(self):
        self.stock.update_sector(mock.Mock(get_pe=lambda: 100))

        self.assertTrue(self.stock.pe_is_less_than_sector_pe())

        self.stock.update_sector(mock.Mock(get_pe=lambda: 43))
        self.assertFalse(self.stock.pe_is_less_than_sector_pe())

        self.stock.update_sector(mock.Mock(get_pe=lambda: 73.22))
        self.assertTrue(self.stock.pe_is_less_than_sector_pe())

    def test_update_balance_sheet(self):
        get_total_debt = mock.Mock()
        balance_sheet = mock.Mock(get_total_debt=get_total_debt)

        self.stock.update_balance_sheets(balance_sheet)
        self.stock.get_debt(2012)

        get_total_debt.assert_called_with(2012)

    def test_update_profit_loss_statement(self):
        get_net_income = mock.Mock()
        income_statement = mock.Mock(get_net_income=get_net_income)

        self.stock.update_profit_loss_statement(income_statement)
        self.stock.get_net_income(2020)

        get_net_income.assert_called_with(2020)

    def test_update_financial_ratios(self):
        financial_ratios = mock.Mock(increasing_current_ratio=lambda x: 'weird')

        stock = Stock(self._get_stock_details(), None, self.income_statement, self.cash_flow, financial_ratios)
        stock.update_financial_ratios(financial_ratios)

        self.assertEqual('weird', stock.increasing_current_ratio('mar10'))

    def test_get_sector_name(self):
        self.assertEqual("consumer", self.stock.get_sector_name())

    def test_get_cash_flow(self):
        get_cash_flow = mock.Mock(return_value=2938)
        cash_flow = mock.Mock(get_cash_flow=get_cash_flow)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            self.income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertEqual(2938, stock.find_cash_flow(2020))
        get_cash_flow.assert_called_with(2020)

    def test_cash_flow_greater_than_net_income__true(self):
        get_cash_flow = mock.Mock(return_value=2938)
        cash_flow = mock.Mock(get_cash_flow=get_cash_flow)
        get_net_income = mock.Mock(return_value=1232)
        income_statement = mock.Mock(get_net_income=get_net_income)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.cash_flow_greater_than_net_income(2020))
        get_cash_flow.assert_called_with(2020)
        get_net_income.assert_called_with(2020)

    def test_cash_flow_greater_than_net_income__false(self):
        get_cash_flow = mock.Mock(return_value=938)
        cash_flow = mock.Mock(get_cash_flow=get_cash_flow)
        get_net_income = mock.Mock(return_value=1232)
        income_statement = mock.Mock(get_net_income=get_net_income)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertFalse(stock.cash_flow_greater_than_net_income(2020))
        get_cash_flow.assert_called_with(2020)
        get_net_income.assert_called_with(2020)

    def test_cash_flow_greater_than_net_income__true__when_equal(self):
        get_cash_flow = mock.Mock(return_value=1232)
        cash_flow = mock.Mock(get_cash_flow=get_cash_flow)
        get_net_income = mock.Mock(return_value=1232)
        income_statement = mock.Mock(get_net_income=get_net_income)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            cash_flow,
            self.financial_ratios)

        self.assertTrue(stock.cash_flow_greater_than_net_income(2020))
        get_cash_flow.assert_called_with(2020)
        get_net_income.assert_called_with(2020)

    def test_add_metadata__adds_metadata(self):
        self.stock.add_metadata("some-key", "some-value")

        self.assertEqual("some-value", self.stock.get_metadata()["some-key"])

    def test_add_metadata__update_score_to(self):
        self.stock.update_score_to(7)

        score = self.stock.get_metadata()["score"]
        self.assertEqual(score, 7)

    def test_remove_metadata__delete_key(self):
        self.stock.add_metadata("some-key", "some-value")
        self.stock.remove_metadata("some-key")

        self.assertDictEqual(dict(), self.stock.get_metadata())

    def test_remove_metadata__does_not_delete_other_keys(self):
        self.stock.add_metadata("some-key", "some-value")
        self.stock.add_metadata("hmm-key", "hmm-value")
        self.stock.remove_metadata("some-key")

        self.assertEqual("hmm-value", self.stock.get_metadata()["hmm-key"])

    def test_cleanup_metadata(self):
        self.stock.add_metadata("some-key", "some-value")
        self.stock.add_metadata("hmm-key", "hmm-value")
        self.stock.cleanup_metadata()

        self.assertDictEqual(dict(), self.stock.get_metadata())

    def test_update_score__update_score__when_score_is_present(self):
        self.stock.update_score_by(1)

        self.assertEqual(1, self.stock.get_metadata()["score"])

    def test_update_score__update_score__when_score_is_not_present(self):
        self.stock.update_score_by(1)

        self.stock.update_score_by(1)

        self.assertEqual(2, self.stock.get_metadata()["score"])

    def test_update_score__update_score__when_score_to_be_updated_is_more_than_one(self):
        self.stock.update_score_by(1)

        self.stock.update_score_by(3)

        self.assertEqual(4, self.stock.get_metadata()["score"])

    def test_update_success_operation_status__when_there_are_no_satisfied_strategy(self):
        self.stock.update_success_operation_status("some-operation")

        self.assertListEqual(["some-operation"], self.stock.get_metadata()["satisfied_criteria"])

    def test_update_success_operation_status__do_not_add_duplicate_operation(self):
        self.stock.update_success_operation_status("some-operation")
        self.stock.update_success_operation_status("some-operation")

        self.assertListEqual(["some-operation"], self.stock.get_metadata()["satisfied_criteria"])

    def test_update_success_operation_status__when_there_are_already_satisfied_strategy(self):
        self.stock.update_success_operation_status("some-operation")
        self.stock.update_success_operation_status("some-other-operation")

        self.assertListEqual(["some-operation", "some-other-operation"],
                             self.stock.get_metadata()["satisfied_criteria"])

    def test_update_failed_operation_status__when_there_are_no_satisfied_strategy(self):
        self.stock.update_failed_operation_status("some-failure-operation")

        self.assertListEqual(["some-failure-operation"], self.stock.get_metadata()["missed_criteria"])

    def test_update_failed_operation_status__do_not_add_duplicate_operations(self):
        self.stock.update_failed_operation_status("some-failure-operation")
        self.stock.update_failed_operation_status("some-failure-operation")

        self.assertListEqual(["some-failure-operation"], self.stock.get_metadata()["missed_criteria"])

    def test_update_update_failed_operation_status__when_there_are_already_satisfied_strategy(self):
        self.stock.update_failed_operation_status("some-failure-operation")
        self.stock.update_failed_operation_status("some-other-failure-operation")

        self.assertListEqual(["some-failure-operation", "some-other-failure-operation"],
                             self.stock.get_metadata()["missed_criteria"])

    def test_update_satisfied_strategy__when_there_are_no_satisfied_strategy(self):
        self.stock.update_satisfied_strategy("some-operation")

        self.assertListEqual(["some-operation"], self.stock.get_metadata()["satisfied_strategies"])

    def test_update_satisfied_strategy__when_there_are_already_satisfied_strategy(self):
        self.stock.update_satisfied_strategy("some-operation")
        self.stock.update_satisfied_strategy("some-other-operation")

        self.assertListEqual(["some-operation", "some-other-operation"],
                             self.stock.get_metadata()["satisfied_strategies"])

    def test_update_report_in_metadata__when_report_is_not_present(self):
        self.stock.update_report_in_metadata({"some-key": "random-value"})

        self.assertDictEqual({"some-key": "random-value"},
                             self.stock.get_metadata()["report_data"])

    def test_update_report_in_metadata__when_report_present(self):
        self.stock.update_report_in_metadata({"some-key": "random-value"})
        self.stock.update_report_in_metadata({"some-other-key": "confused-random-value"})

        self.assertDictEqual({"some-key": "random-value", "some-other-key": "confused-random-value"},
                             self.stock.get_metadata()["report_data"])

    def test_get_report_from_metadata(self):
        self.stock.update_report_in_metadata({"some-key": "random-value"})

        self.assertDictEqual({"some-key": "random-value"}, self.stock.get_report_from_metadata())

    def test_get_tags(self):
        self.assertListEqual([
            "S&P BSE SENSEX",
            "S&P BSE 100",
            "S&P BSE 200",
            "S&P BSE 500"
        ], self.stock.get_tags())

    def test_get_last_date_updated(self):
        self.assertEqual("26-12-2020", self.stock.get_last_date_updated())

    def test_add_tags(self):
        self.stock.add_tag("fmcg")
        self.assertIn("fmcg", self.stock.get_tags())

    def test_add_tags__do_not_add_duplicate_tag(self):
        self.stock.add_tag("fmcg")
        self.stock.add_tag("fmcg")
        self.assertListEqual(['S&P BSE SENSEX', 'S&P BSE 100', 'S&P BSE 200', 'S&P BSE 500', 'fmcg'],
                             self.stock.get_tags())

    def test_get_industry(self):
        self.assertEqual('MAN', self.stock.get_industry())

    def test_get_sub_industry(self):
        self.assertEqual('Personal Care', self.stock.get_sub_industry())

    def test_get_sector(self):
        self.assertEqual(self.sector, self.stock.get_sector())

    def test_has_latest_data__true__when_date_is_latest(self):
        stock_details = self._get_stock_details()
        get_date_of_latest_available_price = mock.Mock(return_value="12-12-2020")
        historical_prices = mock.Mock(get_date_of_latest_available_price=get_date_of_latest_available_price)
        stock_details["historical_prices"] = historical_prices
        self.stock = Stock(stock_details, None, None, None, None)

        self.assertTrue(self.stock.has_latest_data("12-12-2020"))
        get_date_of_latest_available_price.assert_called_with()

    def test_has_latest_data__false__when_date_is_not_latest(self):
        stock_details = self._get_stock_details()
        get_date_of_latest_available_price = mock.Mock(return_value="12-12-2020")
        historical_prices = mock.Mock(get_date_of_latest_available_price=get_date_of_latest_available_price)
        stock_details["historical_prices"] = historical_prices
        self.stock = Stock(stock_details, None, None, None, None)

        self.assertFalse(self.stock.has_latest_data("13-12-2020"))
        get_date_of_latest_available_price.assert_called_with()

    def test_get_net_sales(self):
        stock_details = self._get_stock_details()
        get_net_sales = mock.Mock(return_value=43)
        income_statement = mock.Mock(get_net_sales=get_net_sales)
        stock = Stock(stock_details,
                      self.balance_sheet,
                      income_statement,
                      self.cash_flow,
                      self.financial_ratios)

        self.assertEqual(43, stock.get_net_sales_for_year(2020))

        get_net_sales.assert_called_with(2020)

    def test_get_financial_year_of_results(self):
        self.assertListEqual([2020, 2019, 2018, 2017], self.stock.get_financial_year_of_results())

    def test_get_return_on_equity(self):
        get_net_income = mock.Mock(return_value=200)
        income_statement = mock.Mock(get_net_income=get_net_income)
        get_share_holders_fund = mock.Mock(return_value=99.99)
        self.balance_sheet = mock.Mock(get_shareholders_fund=get_share_holders_fund)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)

        self.assertEqual(stock.get_return_on_equity(2021), 2)
        get_net_income.assert_called_with(2021)
        get_share_holders_fund.assert_called_with(2021)

    def test_get_return_on_equity__false__when_greater_than_sector(self):
        get_net_income = mock.Mock(return_value=200)
        income_statement = mock.Mock(get_net_income=get_net_income)
        get_share_holders_fund = mock.Mock(return_value=99.99)
        self.balance_sheet = mock.Mock(get_shareholders_fund=get_share_holders_fund)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        stock.update_sector(self.sector)
        self.assertFalse(stock.return_on_equity_is_greater_than_sector(2021), 2)
        get_net_income.assert_called_with(2021)
        get_share_holders_fund.assert_called_with(2021)

    def test_get_return_on_equity__true__when_greater_than_sector(self):
        get_net_income = mock.Mock(return_value=200)
        income_statement = mock.Mock(get_net_income=get_net_income)
        get_share_holders_fund = mock.Mock(return_value=9.99)
        self.balance_sheet = mock.Mock(get_shareholders_fund=get_share_holders_fund)
        stock = Stock(
            self._get_stock_details(),
            self.balance_sheet,
            income_statement,
            self.cash_flow,
            self.financial_ratios)
        stock.update_sector(self.sector)
        self.assertTrue(stock.return_on_equity_is_greater_than_sector(2021))
        get_net_income.assert_called_with(2021)
        get_share_holders_fund.assert_called_with(2021)
