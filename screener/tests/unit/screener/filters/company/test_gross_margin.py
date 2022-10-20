from unittest import TestCase, mock

from screener.filters.stock.gross_margin import (
    sector_gross_margin_filter_operation,
    gross_margin_enrich_operation,
    gross_margin_filter_operation
)


class GrossMarginTest(TestCase):
    def test_sector_gross_margin_filter_operation__true__when_gross_margin_greater_than_sector_price(self):
        stock = mock.Mock(gross_margin_is_greater_than_sector=mock.Mock(return_value=True),
                          find_financial_year_of_latest_results=lambda: "19")

        self.assertTrue(sector_gross_margin_filter_operation(stock))

    def test_sector_gross_margin_filter_operation__false__when_gross_margin_less_than_sector_price(self):
        stock = mock.Mock(gross_margin_is_greater_than_sector=mock.Mock(return_value=False),
                          find_financial_year_of_latest_results=lambda: "19")

        self.assertFalse(sector_gross_margin_filter_operation(stock))

    def test_gross_margin_filter_operation__true__when_gross_margin_is_increasing(self):
        stock = mock.Mock(increasing_gross_margin=mock.Mock(return_value=True),
                          find_financial_year_of_latest_results=lambda: "19")

        self.assertTrue(gross_margin_filter_operation(stock))

    def test_gross_margin_filter_operation__false__when_gross_margin_is_decreasing(self):
        stock = mock.Mock(increasing_gross_margin=mock.Mock(return_value=False),
                          find_financial_year_of_latest_results=lambda: "19")

        self.assertFalse(gross_margin_filter_operation(stock))

    @staticmethod
    def test_gross_margin_enrich_operation():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_financial_year_of_results=lambda: ["20", "19"],
                          get_gross_margin=lambda x: {"20": 12, "19": 14}[x])

        gross_margin_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({"gross_margin": [12, 14]})
