import unittest
from unittest import mock

from screener.domain.fundamental.income_statements import IncomeStatements
from screener.exceptions.not_found import IncomeStatementNotFound


class IncomeStatementTest(unittest.TestCase):
    def setUp(self) -> None:
        self.income_statement = IncomeStatements([
            mock.Mock(get_financial_year=lambda: 2022,
                      get_net_income=lambda: 208,
                      get_issued_shares=lambda: 130,
                      get_net_sales=lambda: 145,
                      get_gross_margin=lambda: 200,
                      to_dict=lambda: 1),
            mock.Mock(get_financial_year=lambda: 2021,
                      get_net_income=lambda: 120,
                      get_issued_shares=lambda: 10,
                      get_net_sales=lambda: 250,
                      get_gross_margin=lambda: 150,
                      to_dict=lambda: 2),
            mock.Mock(get_financial_year=lambda: 2020,
                      get_issued_shares=lambda: 10,
                      get_net_income=lambda: 50,
                      get_net_sales=lambda: 100,
                      get_gross_margin=lambda: 200,
                      to_dict=lambda: 3),
            mock.Mock(get_financial_year=lambda: 2019,
                      get_net_sales=lambda: 30,
                      get_gross_margin=lambda: 200,
                      to_dict=lambda: 4),

        ])

    def test_get_latest_financial_year_of_result(self):
        self.assertEqual(self.income_statement.get_latest_financial_year_of_result(), 2022)

    def test_get_financial_year_of_results(self):
        self.assertTupleEqual(self.income_statement.get_financial_year_of_results(), (2022, 2021, 2020, 2019))

    def test_net_sale_compare_to_sector__false(self):
        self.assertFalse(self.income_statement.net_sale_compare_to_sector(5, [
            {"year": 2020, "increase": 300},
            {"year": 2021, "increase": 10}
        ]))

    def test_net_sale_compare_to_sector__true(self):
        self.assertTrue(self.income_statement.net_sale_compare_to_sector(5, [
            {"year": 2020, "increase": 100},
            {"year": 2021, "increase": 100}
        ]))

    def test_get_gross_margin(self):
        self.assertEqual(self.income_statement.get_gross_margin(2022), 200)

    def test_increasing_gross_margin__true__when_increasing(self):
        self.assertTrue(self.income_statement.increasing_gross_margin(2022))

    def test_increasing_gross_margin__false__when_decreasing(self):
        self.assertFalse(self.income_statement.increasing_gross_margin(2021))

    def test_increasing_gross_margin__false__when_equal(self):
        self.assertFalse(self.income_statement.increasing_gross_margin(2020))

    def test_get_new_shares_issued(self):
        self.assertEqual(119.99945, self.income_statement.get_new_shares_issued(2022))

    def test_new_shares_issued__true__when_shares_issues(self):
        self.assertTrue(self.income_statement.new_shares_issued(2022))

    def test_new_shares_issued__false__when_shares_are_not_issued(self):
        self.assertFalse(self.income_statement.new_shares_issued(2021))

    def test_new_shares_issued__raise_exception__when_data_is_not_available(self):
        self.assertRaises(IncomeStatementNotFound, lambda: self.income_statement.new_shares_issued(2025))

    def test_get_net_income(self):
        self.assertEqual(self.income_statement.get_net_income(2022), 208)

    def test_get_issued_shares(self):
        self.assertEqual(self.income_statement.get_issued_shares(2022), 130)

    def test_get_net_sales(self):
        self.assertEqual(self.income_statement.get_net_sales(2022), 145)

    def test_net_sale_increased_by__true__when_equal(self):
        self.assertTrue(self.income_statement.net_sale_increased_by(2022, 2, 44))

    def test_net_sale_increased_by__false__when_not_increased_enough(self):
        self.assertFalse(self.income_statement.net_sale_increased_by(2022, 2, 50))

    def test_net_sale_increased_by__true__when_increased_enough(self):
        self.assertTrue(self.income_statement.net_sale_increased_by(2022, 2, 30))

    def test_net_income_increasing__true__when_increasing_enough(self):
        self.assertTrue(self.income_statement.net_income_increasing(2022, 2, 20))

    def test_net_income_increasing__false__when_not_increased_enough(self):
        self.assertFalse(self.income_statement.net_income_increasing(2022, 2, 80))

    def test_net_sale_increasing__true__when_increasing_enough(self):
        self.assertTrue(self.income_statement.net_sale_increasing(2021, 2, 20))

    def test_net_sale_increasing__false__when_not_increased_enough(self):
        self.assertFalse(self.income_statement.net_sale_increasing(2021, 2, 280))

    def test_get_latest_financial_year_of_result__return_current_year(self):
        self.assertEqual(1985, IncomeStatements([]).get_latest_financial_year_of_result())
