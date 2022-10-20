import unittest
from unittest import mock

from screener.filters.sectoral.net_sale import net_income_enrich_operation


class SectorFilterTest(unittest.TestCase):
    def test_net_income_enrich_operation(self):
        mocked_update_report_in_metadata = mock.Mock()
        sector = mock.Mock(get_net_sales_for_year=lambda y: {2018: 123, 2019: 545, 2020: 387, 2021: 23, 2022: 192}[y],
                           update_report_in_metadata=mocked_update_report_in_metadata)

        net_income_enrich_operation(sector)

        mocked_update_report_in_metadata.assert_called_with({"net_sale": [123, 545, 387, 23, 192]})
