from unittest import TestCase, mock

from screener.filters.stock.sector_filter import sector_filter_operation, sector_enrich_operation


class SectorTest(TestCase):
    def test_sector_filter_operation__true__when_sector_matches_exactly(self):
        stock = mock.Mock(get_sector_name=lambda: "Some Value")

        self.assertTrue(sector_filter_operation(stock, ["some", "value", "Some Value", "Some", "Value"]))

    def test_sector_filter_operation__true__when_sector_matches_lower_case(self):
        stock = mock.Mock(get_sector_name=lambda: "some value")

        self.assertTrue(sector_filter_operation(stock, ["some", "value", "Some Value", "Some", "Value"]))

    def test_sector_filter_operation__false__when_sector_matches_partially(self):
        stock = mock.Mock(get_sector_name=lambda: "some value")

        self.assertFalse(sector_filter_operation(stock, ["some", "value", "Some", "Value"]))

    def test_sector_filter_operation__false__when_sector_does_not_match(self):
        stock = mock.Mock(get_sector_name=lambda: "weird")

        self.assertFalse(sector_filter_operation(stock, ["some", "value", "Some", "Value"]))

    @staticmethod
    def test_sector_enrich_operation():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_sector_name=lambda: "Pharma")

        sector_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "sector": "Pharma"
        })
