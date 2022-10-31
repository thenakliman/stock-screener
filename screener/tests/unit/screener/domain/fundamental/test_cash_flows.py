import unittest
from unittest import mock

from screener.domain.fundamental.cash_flows import CashFlows
from screener.exceptions.not_found import CashFlowNotFound


class TestCashFlow(unittest.TestCase):
    def setUp(self):
        self.cash_flows = CashFlows([
            mock.Mock(get_financial_year=lambda: 2021,
                      positive_cash_flow=lambda: True,
                      get_cash_flow_from_operating_activities=lambda: 1000),
            mock.Mock(get_financial_year=lambda: 2020,
                      positive_cash_flow=lambda: False,
                      get_cash_flow_from_operating_activities=lambda: 2000),
            mock.Mock(get_financial_year=lambda: 2019,
                      positive_cash_flow=lambda: False,
                      get_cash_flow_from_operating_activities=lambda: 3000)
        ])

    def test_get_latest_financial_year_of_result(self):
        self.assertEqual(self.cash_flows.get_latest_financial_year_of_result(), 2021)

    def test_get_financial_year_of_results(self):
        self.assertTupleEqual(self.cash_flows.get_financial_year_of_results(), (2021, 2020, 2019))

    def test_positive_cash_flow__raise_exception__when_year_not_found(self):
        self.assertRaises(CashFlowNotFound, lambda: self.cash_flows.positive_cash_flow(2023))

    def test_positive_cash_flow__true__when_cash_flow_is_positive(self):
        self.assertTrue(self.cash_flows.positive_cash_flow(2021))

    def test_positive_cash_flow__false__when_cash_flow_is_not_positive(self):
        self.assertFalse(self.cash_flows.positive_cash_flow(2020))

    def test_get_cash_flow(self):
        self.assertEqual(2000, self.cash_flows.get_cash_flow(2020))

    def test_get_cash_flow__for_first_year(self):
        self.assertEqual(1000, self.cash_flows.get_cash_flow(2021))
