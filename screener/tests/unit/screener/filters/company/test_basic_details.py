from unittest import TestCase, mock

from screener.filters.stock.basic_details import basic_details


class TestBasicDetails(TestCase):
    def test_basic_details__update_isinid(self):
        update_report_in_metadata = mock.Mock()
        isinid = 10
        weird = "weird"
        financial_year = "19"
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_isinid=lambda: isinid,
                          get_company_name=lambda: weird,
                          find_financial_year_of_latest_results=lambda: financial_year)

        basic_details(stock)
        update_report_in_metadata.assert_called_with({
            "isinid": str(isinid),
            "name": weird,
            "financial_year": financial_year
        })
