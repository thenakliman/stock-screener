from unittest import TestCase, mock

from screener.filters.stock.current_ratio import current_ratio_filter_operation, \
    sector_current_ratio_filter_operation, current_ratio_enrich_operation


class TestCurrentRatio(TestCase):
    def test_current_ratio_filter_operation__true__when_current_ratio_is_increasing(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19",
                          increasing_current_ratio=lambda x: True)

        self.assertTrue(current_ratio_filter_operation(stock))

    def test_current_ratio_filter_operation__false__when_current_ratio_is_increasing(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19",
                          increasing_current_ratio=lambda x: False)

        self.assertFalse(current_ratio_filter_operation(stock))

    def test_sector_current_ratio_filter_operation__true__when_current_ratio_is_increasing(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19",
                          current_ratio_is_greater_than_sector=lambda x: True)

        self.assertTrue(sector_current_ratio_filter_operation(stock))

    def test_sector_current_ratio_filter_operation__false__when_current_ratio_is_increasing(self):
        stock = mock.Mock(find_financial_year_of_latest_results=lambda: "19",
                          current_ratio_is_greater_than_sector=lambda x: False)

        self.assertFalse(sector_current_ratio_filter_operation(stock))

    def test_current_ratio_enrich_operation(self):
        update_report_in_metadata = mock.Mock()
        find_current_ratio_by_year = mock.Mock(side_effect=lambda x: {"20": 1, "19": 3, "18": 5}[x])
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_current_ratio=find_current_ratio_by_year,
                          get_financial_year_of_results=lambda: ["18", "19", "20"])

        current_ratio_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "current_ratio": [5, 3, 1]
        })
