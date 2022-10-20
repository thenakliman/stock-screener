from unittest import TestCase, mock

from screener.filters.stock.pe_filter import pe_filter_operation, sector_pe_filter_operation, \
    pe_enrich_operation, max_pe_filter


class PEFilterTest(TestCase):
    def test_pe_filter_operation__true__when_pe_is_less_than_percentage_of_industry_pe(self):
        stock = mock.Mock(get_pe=lambda: 80,
                          get_industry_pe=lambda: 100)

        self.assertTrue(pe_filter_operation(stock, 81))

    def test_pe_filter_operation__false__when_pe_is_less_than_0(self):
        stock = mock.Mock(get_pe=lambda: -1,
                          get_industry_pe=lambda: 100)

        self.assertFalse(pe_filter_operation(stock, 81))

    def test_pe_filter_operation__true__when_pe_is_equal_of_industry_pe(self):
        stock = mock.Mock(get_pe=lambda: 80,
                          get_industry_pe=lambda: 100)

        self.assertTrue(pe_filter_operation(stock, 80))

    def test_pe_filter_operation__false__when_pe_is_greater_than_percentage_of_industry_pe(self):
        stock = mock.Mock(get_pe=lambda: 80,
                          get_industry_pe=lambda: 100)

        self.assertFalse(pe_filter_operation(stock, 79))

    def test_sector_pe_filter_operation__true__when_pe_is_less_than_sector_pe(self):
        stock = mock.Mock(pe_is_less_than_sector_pe=lambda: True)

        self.assertTrue(sector_pe_filter_operation(stock))

    def test_sector_pe_filter_operation__false__when_pe_is_not_less_than_sector_pe(self):
        stock = mock.Mock(pe_is_less_than_sector_pe=lambda: False)

        self.assertFalse(sector_pe_filter_operation(stock))

    def test_max_pe_filter__true__when_pe_is_less_than_given_pe(self):
        stock = mock.Mock(get_pe=lambda: 33)

        self.assertTrue(max_pe_filter(stock, 34))

    def test_max_pe_filter__true__when_pe_is_equal_to_given_pe(self):
        stock = mock.Mock(get_pe=lambda: 33)

        self.assertTrue(max_pe_filter(stock, 33))

    def test_max_pe_filter__false__when_pe_is_greater_than_given_pe(self):
        stock = mock.Mock(get_pe=lambda: 33)

        self.assertFalse(max_pe_filter(stock, 32))

    def test_pe_enrich_operation(self):
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_pe=lambda: 10.12,
                          get_industry_pe=lambda: 12)

        pe_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "pe": 10.12,
            "industry_pe": 12
        })
