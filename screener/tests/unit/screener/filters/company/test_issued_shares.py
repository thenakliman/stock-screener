from unittest import TestCase, mock

from screener.filters.stock.issued_shares import issued_shares_filter_operation, issued_shares_enrich_operation


class Test(TestCase):
    def test_issued_shares_filter_operation__true__when_new_shares_are_not_issued(self):
        new_shares_issued = mock.Mock(return_value=False)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "20",
                          new_shares_issued=new_shares_issued)

        self.assertTrue(issued_shares_filter_operation(stock))
        new_shares_issued.assert_called_with("20")

    def test_issued_shares_filter_operation__false__when_new_shares_are_issued(self):
        new_shares_issued = mock.Mock(return_value=True)
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "20",
                          new_shares_issued=new_shares_issued)

        self.assertFalse(issued_shares_filter_operation(stock))
        new_shares_issued.assert_called_with("20")

    def test_issued_shares_enrich_operation(self):
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_issued_shares=lambda x: {"20": 12, "19": 9}[x],
                          get_new_issued_shares=lambda x: {"20": 10, "19": 19}[x],
                          get_financial_year_of_results=lambda: ["20", "19"],
                          update_report_in_metadata=update_report_in_metadata)

        issued_shares_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "total_issued_shares": [12, 9],
            "new_issued_shares": [10]
        })
