from unittest import TestCase, mock

from screener.filters.stock.debt_filter import (
    debt_filter_operation,
    debt_enrich_operation,
    debt_to_equity_filter_operation,
    debt_to_equity_enrich_operation,
    debt_to_equity_less_than_industry_filter_operation)


class TestDebtFilter(TestCase):
    def test_debt_filter_operation__true__when_debt_is_less_than_given_value(self):
        stock = mock.Mock(
            get_long_term_debts=lambda x: 10 if x == 20 else -1,
            find_financial_year_of_latest_results=lambda: 20
        )

        self.assertTrue(debt_filter_operation(stock, 20))

    def test_debt_filter_operation__false__when_debt_is_less_than_given_value(self):
        stock = mock.Mock(
            get_long_term_debts=lambda x: 10 if x == 20 else -1,
            find_financial_year_of_latest_results=lambda: 20
        )

        self.assertFalse(debt_filter_operation(stock, 6))

    def test_debt_to_equity_filter_operation__false__when_debt_equity_is_greater_than_given_value(self):
        stock = mock.Mock(
            get_debt_to_equity_ratio=lambda x: 10 if x == 20 else -1,
            find_financial_year_of_latest_results=lambda: 20
        )

        self.assertFalse(debt_to_equity_filter_operation(stock, 9))

    def test_debt_to_equity_filter_operation__true__when_debt_equity_is_equal_to_given_value(self):
        stock = mock.Mock(
            get_debt_to_equity_ratio=lambda x: 10 if x == 20 else -1,
            find_financial_year_of_latest_results=lambda: 20
        )

        self.assertTrue(debt_to_equity_filter_operation(stock, 10))

    def test_debt_to_equity_less_than_industry_filter_operation__false(self):
        stock = mock.Mock(debt_to_equity_is_less_than_industry=lambda x: False)

        self.assertFalse(debt_to_equity_less_than_industry_filter_operation(stock, 9))

    def test_debt_to_equity_less_than_industry_filter_operation__true(self):
        stock = mock.Mock(debt_to_equity_is_less_than_industry=lambda x: True)

        self.assertTrue(debt_to_equity_less_than_industry_filter_operation(stock, 10))

    def test_debt_to_equity_filter_operation__true__when_debt_equity_is_less_to_given_value(self):
        stock = mock.Mock(
            get_debt_to_equity_ratio=lambda x: 10 if x == 20 else -1,
            find_financial_year_of_latest_results=lambda: 20
        )

        self.assertTrue(debt_to_equity_filter_operation(stock, 11))

    def test_debt_enrich_operation__true__when_debt_is_less_than_given_value(self):
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_debt=lambda x: {"20": 1, "19": 3, "18": 5}[x],
                          get_financial_year_of_results=lambda: ["18", "19", "20"],
                          update_report_in_metadata=update_report_in_metadata)

        debt_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "debt": [5, 3, 1]
        })

    def test_debt_to_equity_enrich_operations(self):
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_debt_to_equity_ratio=lambda x: {"20": 1, "19": 3, "18": 5}[x],
                          get_financial_year_of_results=lambda: ["18", "19", "20"],
                          update_report_in_metadata=update_report_in_metadata,
                          get_sector_debt_to_equity=lambda: 1,
                          find_financial_year_of_latest_results=lambda: "20")

        debt_to_equity_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "debt_to_equity": [5, 3, 1],
            'latest_debt_to_equity': 1,
            'industry_debt_to_equity': 1
        })
