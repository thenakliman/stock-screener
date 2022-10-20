from unittest import TestCase, mock

from screener.filters.index.near_min_filter import minimum_index_filter, minimum_price_enrich_operation


class NearMinFilterTest(TestCase):
    def test_minimum_value_enrich_operation(self):
        number_of_days_since_index_formed = mock.Mock(return_value=6)
        minimum_value_in_given_days = mock.Mock(return_value=100)
        get_current_value = mock.Mock(return_value=119)
        mocked_index = mock.Mock(number_of_days_since_index_formed=number_of_days_since_index_formed,
                                 minimum_value_in_given_days=minimum_value_in_given_days,
                                 get_current_value=get_current_value)

        self.assertTrue(minimum_index_filter(
            mocked_index,
            years=0.02,
            not_more_than_min_by_percentage=20))
        number_of_days_since_index_formed.assert_called_with()
        minimum_value_in_given_days.assert_called_with(4)
        get_current_value.assert_called_with()

    def test_minimum_value_enrich_operation_consider_minimum_days_in_market(self):
        number_of_days_since_index_formed = mock.Mock(return_value=6)
        minimum_value_in_given_days = mock.Mock(return_value=100)
        get_current_value = mock.Mock(return_value=119)
        mocked_index = mock.Mock(number_of_days_since_index_formed=number_of_days_since_index_formed,
                                 minimum_value_in_given_days=minimum_value_in_given_days,
                                 get_current_value=get_current_value)

        self.assertTrue(minimum_index_filter(
            mocked_index,
            years=0.10,
            not_more_than_min_by_percentage=20))
        number_of_days_since_index_formed.assert_called_with()
        minimum_value_in_given_days.assert_called_with(6)
        get_current_value.assert_called_with()

    def test_minimum_value_enrich_operation_return_false(self):
        number_of_days_since_index_formed = mock.Mock(return_value=6)
        minimum_value_in_given_days = mock.Mock(return_value=100)
        get_current_value = mock.Mock(return_value=120)
        mocked_index = mock.Mock(number_of_days_since_index_formed=number_of_days_since_index_formed,
                                 minimum_value_in_given_days=minimum_value_in_given_days,
                                 get_current_value=get_current_value)

        self.assertFalse(minimum_index_filter(
            mocked_index,
            years=0.02,
            not_more_than_min_by_percentage=19))
        number_of_days_since_index_formed.assert_called_with()
        minimum_value_in_given_days.assert_called_with(4)
        get_current_value.assert_called_with()

    def test_minimum_value_enrich_operation_consider_minimum_days_in_market_return_false(self):
        number_of_days_since_index_formed = mock.Mock(return_value=6)
        minimum_value_in_given_days = mock.Mock(return_value=100)
        get_current_value = mock.Mock(return_value=120)
        mocked_index = mock.Mock(number_of_days_since_index_formed=number_of_days_since_index_formed,
                                 minimum_value_in_given_days=minimum_value_in_given_days,
                                 get_current_value=get_current_value)

        self.assertFalse(minimum_index_filter(
            mocked_index,
            years=0.10,
            not_more_than_min_by_percentage=19))
        number_of_days_since_index_formed.assert_called_with()
        minimum_value_in_given_days.assert_called_with(6)
        get_current_value.assert_called_with()

    @staticmethod
    def test_minimum_price_enrich_operation():
        minimum_value_in_given_days = mock.Mock(return_value=80)
        update_report_in_metadata = mock.Mock()
        index = mock.Mock(get_current_value=lambda: 100,
                          minimum_value_in_given_days=minimum_value_in_given_days,
                          number_of_days_since_index_formed=lambda: 10,
                          update_report_in_metadata=update_report_in_metadata)

        minimum_price_enrich_operation(index, 0.5)
        update_report_in_metadata.assert_called_with({
            "minimum_value": 80,
            "current_value": 100,
            "more_than_minimum_value": 25.0})

        minimum_value_in_given_days.assert_called_with(10)
