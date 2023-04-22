from unittest import TestCase, mock

from screener.filters.stock.return_on_equity import (
    return_on_equity_filter_operation,
    sector_return_on_equity_filter_operation,
    return_on_equity_filter_operation_enrich_operation
)


class ReturnOnAssetTest(TestCase):
    def test_sector_return_on_equity_filter_operation__true__return_on_equity_greater_than_given(self):
        get_return_on_equity = mock.Mock(return_value=49)
        stock = mock.Mock(get_return_on_equity=get_return_on_equity,
                          find_financial_year_of_latest_results=lambda: "34")

        self.assertTrue(return_on_equity_filter_operation(stock, 45))
        get_return_on_equity.assert_called_with("34")

    def test_sector_return_on_equity_filter_operation__true__return_on_equity_equals_given(self):
        get_return_on_equity = mock.Mock(return_value=49)
        stock = mock.Mock(get_return_on_equity=get_return_on_equity,
                          find_financial_year_of_latest_results=lambda: "34")

        self.assertTrue(return_on_equity_filter_operation(stock, 49))
        get_return_on_equity.assert_called_with("34")

    def test_sector_return_on_equity_filter_operation__false__return_on_equity_less_than_given(self):
        calculate_return_on_equity = mock.Mock(return_value=49)
        stock = mock.Mock(get_return_on_equity=calculate_return_on_equity,
                          find_financial_year_of_latest_results=lambda: "34")

        self.assertFalse(return_on_equity_filter_operation(stock, 50))
        calculate_return_on_equity.assert_called_with("34")

    def test_sector_return_on_equity_filter_operation__true__when_roe_greater_than_sector(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "89",
                          sector_return_on_equity_filter_operation=lambda x: x == "89")

        self.assertTrue(sector_return_on_equity_filter_operation(stock))

    def test_sector_return_on_equity_filter_operation__false__when_roe_greater_than_sector(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "89",
                          return_on_equity_is_greater_than_sector=lambda x: x != "89")

        self.assertFalse(sector_return_on_equity_filter_operation(stock))

    @staticmethod
    def test_return_on_equity_report():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_return_on_equity=lambda x: {"20": 34, "19": 98}[x],
                          get_financial_year_of_results=lambda: ["20", "19"])

        return_on_equity_filter_operation_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "return_on_equities": [34]
        })
