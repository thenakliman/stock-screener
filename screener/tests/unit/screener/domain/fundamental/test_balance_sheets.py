from unittest import TestCase, mock

from screener.domain.fundamental.balance_sheets import BalanceSheets
from screener.exceptions.not_found import BalanceSheetNotFound


class TestBalanceSheets(TestCase):
    def setUp(self):
        self.balance_sheet = BalanceSheets([mock.Mock(
            get_financial_year=lambda: 2021,
            get_current_ratio=lambda: 1.2,
            get_total_debt=lambda: 340,
            get_long_term_debts=lambda: 550,
            get_debt_to_equity_ratio=lambda: 0.3,
            get_shareholders_fund=lambda: 13,
            get_total_asset=lambda: 2900,
        ), mock.Mock(
            get_financial_year=lambda: 2020,
            get_current_ratio=lambda: 1.1,
            get_total_debt=lambda: 335,
            get_long_term_debts=lambda: 590,
            get_debt_to_equity_ratio=lambda: 0.4,
            get_shareholders_fund=lambda: 17,
            get_total_asset=lambda: 2930,
        )])

    def test_get_latest_financial_year_of_result(self):
        self.assertEqual(self.balance_sheet.get_latest_financial_year_of_result(), 2021)

    def test_get_latest_financial_year_of_result__when_data_is_not_available_return_current_year(self):
        self.assertEqual(BalanceSheets([]).get_latest_financial_year_of_result(), 1985)

    def test_get_current_ratio(self):
        self.assertEqual(self.balance_sheet.get_current_ratio(2021), 1.2)

    def test_get_financial_year_of_results(self):
        self.assertTupleEqual(self.balance_sheet.get_financial_year_of_results(), (2021, 2020))

    def test_increasing_current_ratio__true__when_current_ratio_increasing(self):
        self.assertTrue(self.balance_sheet.increasing_current_ratio(2021))

    def test_increasing_current_ratio__true__when_current_ratio_is_equal(self):
        self.assertTrue(
            BalanceSheets([
                mock.Mock(get_financial_year=lambda: 2021, get_current_ratio=lambda: 1.1),
                mock.Mock(get_financial_year=lambda: 2020, get_current_ratio=lambda: 1.1)]
            ).increasing_current_ratio(2021)
        )

    def test_increasing_current_ratio__false__when_current_ratio_is_decreasing(self):
        self.assertFalse(
            BalanceSheets([
                mock.Mock(get_financial_year=lambda: 2021, get_current_ratio=lambda: 1.1),
                mock.Mock(get_financial_year=lambda: 2020, get_current_ratio=lambda: 1.2)]
            ).increasing_current_ratio(2021)
        )

    def test_decreasing_long_term_debt_ratio_by_year__true__when_long_term_debt_decreasing(self):
        self.assertTrue(self.balance_sheet.decreasing_long_term_debt_ratio_by_year(2021))

    def test_decreasing_long_term_debt_ratio_by_year__true__when_current_ratio_is_equal(self):
        self.assertTrue(
            BalanceSheets([
                mock.Mock(get_financial_year=lambda: 2021, get_long_term_debts=lambda: 1.1),
                mock.Mock(get_financial_year=lambda: 2020, get_long_term_debts=lambda: 1.1)]
            ).decreasing_long_term_debt_ratio_by_year(2021)
        )

    def test_decreasing_long_term_debt_ratio_by_year__false__when_long_term_debt_is_increasing(self):
        self.assertFalse(
            BalanceSheets([
                mock.Mock(get_financial_year=lambda: 2021, get_long_term_debts=lambda: 1.3),
                mock.Mock(get_financial_year=lambda: 2020, get_long_term_debts=lambda: 1.2)]
            ).decreasing_long_term_debt_ratio_by_year(2021)
        )

    def test_get_current_ratio__when_data_is_not_first_element_of_list(self):
        self.assertEqual(self.balance_sheet.get_current_ratio(2020), 1.1)

    def test_get_current_ratio__raise_exception__when_data_not_found(self):
        self.assertRaises(BalanceSheetNotFound, lambda: self.balance_sheet.get_current_ratio(2023))

    def test_get_total_debt(self):
        self.assertEqual(self.balance_sheet.get_total_debt(2021), 340)

    def test_get_total_debt__when_data_is_not_first_element_of_list(self):
        self.assertEqual(self.balance_sheet.get_total_debt(2020), 335)

    def test_get_total_debt__raise_exception__when_data_not_found(self):
        self.assertRaises(BalanceSheetNotFound, lambda: self.balance_sheet.get_total_debt(2023))

    def test_get_debt_to_equity_ratio(self):
        self.assertEqual(self.balance_sheet.get_debt_to_equity_ratio(2021), 0.3)

    def test_get_long_term_debts(self):
        self.assertEqual(self.balance_sheet.get_long_term_debts(2021), 550)

    def test_get_long_term_debts__when_data_is_not_first_element_of_list(self):
        self.assertEqual(self.balance_sheet.get_long_term_debts(2020), 590)

    def test_get_long_term_debts__raise_exception__when_data_not_found(self):
        self.assertRaises(BalanceSheetNotFound, lambda: self.balance_sheet.get_long_term_debts(2023))

    def test_get_asset(self):
        self.assertEqual(self.balance_sheet.get_asset(2020), 2930)

    def test_get_asset__when_data_is_first_element_of_list(self):
        self.assertEqual(self.balance_sheet.get_asset(2021), 2900)

    def test_get_asset__raise_exception__when_data_not_found(self):
        self.assertRaises(BalanceSheetNotFound, lambda: self.balance_sheet.get_asset(2023))

    def test_get_shareholders_fund__raise_exception__when_balance_sheet_not_found(self):
        self.assertRaises(BalanceSheetNotFound, lambda: self.balance_sheet.get_shareholders_fund(2023))

    def test_get_shareholders_fund(self):
        self.assertEqual(13, self.balance_sheet.get_shareholders_fund(2021))
