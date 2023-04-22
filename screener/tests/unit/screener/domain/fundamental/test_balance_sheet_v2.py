from unittest import TestCase

from screener.domain.fundamental.balance_sheet import BalanceSheet


class TestBalanceSheet(TestCase):
    def setUp(self):
        self.balance_sheet = BalanceSheet(
            financial_year=2021,
            total_current_liability=1293.3,
            total_current_asset=342.3,
            total_non_current_asset=53.5,
            total_shareholders_funds=1293,
            total_asset=2938,
            long_term_borrowings=934,
            short_term_borrowings=10,
            date_created="12-12-2020",
            last_date_updated="12-12-2021"
        )

    def test_get_total_assets(self):
        self.assertEqual(2938, self.balance_sheet.get_total_assets())

    def test_get_current_ratio(self):
        self.assertEqual(0.26467176989097657, self.balance_sheet.get_current_ratio())

    def test_get_long_term_debts(self):
        self.assertEqual(934, self.balance_sheet.get_long_term_debts())

    def test_get_total_debt(self):
        self.assertEqual(944, self.balance_sheet.get_total_debt())

    def test_get_total_asset(self):
        self.assertEqual(2938, self.balance_sheet.get_total_asset())

    def test_get_financial_year(self):
        self.assertEqual(2021, self.balance_sheet.get_financial_year())

    def test_get_debt_to_equity_ratio(self):
        self.assertEqual(0.7300850734725445, self.balance_sheet.get_debt_to_equity_ratio())

    def test_get_shareholders_fund(self):
        self.assertEqual(1293, self.balance_sheet.get_shareholders_fund())
