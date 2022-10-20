from unittest import TestCase, mock

from screener.filters.stock.operating_cash_flow import operating_cash_flow_filter_operation, \
    operating_cash_flow_enrich_operation, cash_flow_greater_than_net_income_filter_operation, \
    cash_flow_greater_than_net_income_enrich_operation


class OperatingCashFlowTest(TestCase):
    def test_operating_cash_flow_filter_operation__true__when_cash_flow_is_positive(self):
        stock = mock.Mock(positive_cash_flow=lambda x: x == "30",
                          find_financial_year_of_latest_results=lambda: "30")

        self.assertTrue(operating_cash_flow_filter_operation(stock))

    def test_operating_cash_flow_filter_operation__false__when_cash_flow_is_not_positive(self):
        stock = mock.Mock(positive_cash_flow=lambda x: x != "30",
                          find_financial_year_of_latest_results=lambda: "30")

        self.assertFalse(operating_cash_flow_filter_operation(stock))

    @staticmethod
    def test_operating_cash_flow_enrich_operation():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_financial_year_of_results=lambda: ["20", "19"],
                          get_operating_cash_flow_ratio=lambda x: {"20": 78, "19": 89}[x],
                          update_report_in_metadata=update_report_in_metadata)

        operating_cash_flow_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({"operating_cash_flow": [78]})

    def test_cash_flow_greater_than_net_income_filter__true__when__cash_flow_greater_than_net_income_filter(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19",
                          cash_flow_greater_than_net_income=lambda x: "19" == x)

        self.assertTrue(cash_flow_greater_than_net_income_filter_operation(stock))

    def test_cash_flow_greater_than_net_income_filter__false__when__cash_flow_less_than_net_income_filter(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19",
                          cash_flow_greater_than_net_income=lambda x: "19" != x)

        self.assertFalse(cash_flow_greater_than_net_income_filter_operation(stock))

    @staticmethod
    def test_cash_flow_greater_than_net_income_enrich_operation():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(
            update_report_in_metadata=update_report_in_metadata,
            get_financial_year_of_results=lambda: ["20", "19"],
            find_cash_flow=lambda x: {"20": 43, "19": 87}[x],
            get_net_income=lambda x: {"20": 23, "19": 89}[x])

        cash_flow_greater_than_net_income_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "cash_flows": [43, 87],
            "incomes": [23, 89]
        })
