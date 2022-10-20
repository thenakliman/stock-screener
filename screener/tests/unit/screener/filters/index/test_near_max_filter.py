from unittest import TestCase, mock

from screener.filters.index.near_max_filter import maximum_value_filter_operation, maximum_value_enrich_operation


class NearMaxFilterTest(TestCase):
    def test_true_when_filter_criteria_match_and_number_of_maximum_days_do_not_limit_days_to_consider(self):
        number_of_days_since_index_formed = mock.Mock(return_value=6)
        maximum_value_in_given_days = mock.Mock(return_value=100)
        get_current_value = mock.Mock(return_value=20)
        mocked_index = mock.Mock(number_of_days_since_index_formed=number_of_days_since_index_formed,
                                 maximum_value_in_given_days=maximum_value_in_given_days,
                                 get_current_value=get_current_value)

        self.assertTrue(maximum_value_filter_operation(
            mocked_index,
            years=0.02,
            less_than_maximum_value_in_percentage=19))
        number_of_days_since_index_formed.assert_called_with()
        maximum_value_in_given_days.assert_called_with(4)
        get_current_value.assert_called_with()

    def test_false_when_filter_criteria_do_not_match_and_number_of_maximum_days_do_not_limit_days_to_consider(self):
        number_of_days_since_index_formed = mock.Mock(return_value=6)
        maximum_value_in_given_days = mock.Mock(return_value=100)
        get_current_value = mock.Mock(return_value=119)
        mocked_index = mock.Mock(number_of_days_since_index_formed=number_of_days_since_index_formed,
                                 maximum_value_in_given_days=maximum_value_in_given_days,
                                 get_current_value=get_current_value)

        self.assertFalse(maximum_value_filter_operation(
            mocked_index,
            years=0.10,
            less_than_maximum_value_in_percentage=20))
        number_of_days_since_index_formed.assert_called_with()
        maximum_value_in_given_days.assert_called_with(6)
        get_current_value.assert_called_with()

    def test_true_when_filter_criteria_match_and_number_of_maximum_days_limit_days_to_consider(self):
        number_of_days_since_index_formed = mock.Mock(return_value=6)
        maximum_value_in_given_days = mock.Mock(return_value=100)
        get_current_value = mock.Mock(return_value=79)
        mocked_index = mock.Mock(number_of_days_since_index_formed=number_of_days_since_index_formed,
                                 maximum_value_in_given_days=maximum_value_in_given_days,
                                 get_current_value=get_current_value)

        self.assertTrue(maximum_value_filter_operation(
            mocked_index,
            years=0.10,
            less_than_maximum_value_in_percentage=20))
        number_of_days_since_index_formed.assert_called_with()
        maximum_value_in_given_days.assert_called_with(6)
        get_current_value.assert_called_with()

    def test_false_when_filter_criteria_do_not_match_and_number_of_maximum_days_limit_days_to_consider(self):
        number_of_days_since_index_formed = mock.Mock(return_value=6)
        maximum_value_in_given_days = mock.Mock(return_value=100)
        get_current_value = mock.Mock(return_value=120)
        mocked_index = mock.Mock(number_of_days_since_index_formed=number_of_days_since_index_formed,
                                 maximum_value_in_given_days=maximum_value_in_given_days,
                                 get_current_value=get_current_value)

        self.assertFalse(maximum_value_filter_operation(
            mocked_index,
            years=0.10,
            less_than_maximum_value_in_percentage=22))
        number_of_days_since_index_formed.assert_called_with()
        maximum_value_in_given_days.assert_called_with(6)
        get_current_value.assert_called_with()

    @staticmethod
    def test_minimum_price_enrich_operation():
        maximum_value_in_given_days = mock.Mock(return_value=100)
        update_report_in_metadata = mock.Mock()
        index = mock.Mock(get_current_value=lambda: 80,
                          maximum_value_in_given_days=maximum_value_in_given_days,
                          number_of_days_since_index_formed=lambda: 10,
                          update_report_in_metadata=update_report_in_metadata)

        maximum_value_enrich_operation(index, 0.5)
        update_report_in_metadata.assert_called_with({
            "maximum_value": 100,
            "current_value": 80,
            "less_than_maximum_value": 20.0})

        maximum_value_in_given_days.assert_called_with(10)
