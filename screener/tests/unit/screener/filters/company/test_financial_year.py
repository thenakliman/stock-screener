from unittest import TestCase, mock

from screener.filters.stock.financial_year import latest_financial_year_filter_operation, \
    latest_financial_year_enrich_operation


class FinancialYearTest(TestCase):
    @mock.patch("screener.filters.stock.financial_year.is_latest_financial_year", return_value=True)
    def test_latest_financial_year_filter_operation__true__when_financial_year_is_latest(self, mocked_is_latest_year):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19")

        self.assertTrue(latest_financial_year_filter_operation(stock))

        mocked_is_latest_year.assert_called_with("19")

    @mock.patch("screener.filters.stock.financial_year.is_latest_financial_year", return_value=False)
    def test_latest_financial_year_filter_operation__false__when_financial_year_is_latest(self, mocked_is_latest_year):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19")

        self.assertFalse(latest_financial_year_filter_operation(stock))

        mocked_is_latest_year.assert_called_with("19")

    @staticmethod
    def test_latest_financial_year_enrich_operation__false__when_financial_year_is_latest():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19",
                          update_report_in_metadata=update_report_in_metadata)

        latest_financial_year_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "financial_year": "19"
        })
