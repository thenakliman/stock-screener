import unittest

from screener.domain.fundamental.income_statement import IncomeStatement


class IncomeStatementTest(unittest.TestCase):
    def setUp(self) -> None:
        self.income_statement = IncomeStatement(
            financial_year=2019,
            incomes=1203.23,
            net_sale=1202.5,
            expenses=600.4,
            issued_shares=123.2,
            date_created="20-01-2019",
            last_date_updated="20-02-2020"
        )

    def test_get_net_sales(self):
        self.assertEqual(self.income_statement.get_net_sales(), 1202.5)

    def test_get_gross_margin(self):
        self.assertEqual(self.income_statement.get_gross_margin(), 0.5007068607068608)

    def test_get_net_income(self):
        self.assertEqual(self.income_statement.get_net_income(), 1203.23)

    def test_get_issued_shares(self):
        self.assertEqual(self.income_statement.get_issued_shares(), 123.2)

    def test_get_financial_year(self):
        self.assertEqual(self.income_statement.get_financial_year(), 2019)

    def test_to_dict(self):
        self.assertDictEqual(self.income_statement.to_dict(), {
            "income": 1203.23,
            "net_sale": 1202.5,
            "total_expense": 600.4,
            "issued_shares": 123.2,
            "date_created": "20-01-2019",
            "last_date_updated": "20-02-2020",
            "financial_year": 2019
        })
