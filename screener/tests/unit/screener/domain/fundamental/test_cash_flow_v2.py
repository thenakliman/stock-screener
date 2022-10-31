import unittest

from screener.domain.fundamental.cash_flow import CashFlow


class TestCashFlow(unittest.TestCase):
    def setUp(self):
        self.cash_flow = CashFlow(
            financial_year=2021,
            cash_flow_from_operating_activities=2932,
            date_created="20-01-2021",
            last_date_updated="21-01-2021"
        )

    def test_get_financial_year(self):
        self.assertEqual(2021, self.cash_flow.get_financial_year())

    def test_get_cash_flow_from_operating_activities(self):
        self.assertEqual(2932, self.cash_flow.get_cash_flow_from_operating_activities())

    def test_positive_cash_flow__true__when_cash_flow_is_positive(self):
        self.assertTrue(self.cash_flow.positive_cash_flow())

    def test_positive_cash_flow__false__when_cash_flow_is_positive(self):
        self.assertFalse(CashFlow(
            financial_year=2021,
            cash_flow_from_operating_activities=-1,
            date_created="20-01-2021",
            last_date_updated="21-01-2021"
        ).positive_cash_flow())
