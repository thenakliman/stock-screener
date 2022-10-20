from unittest import TestCase, mock

from screener.common import math
from screener.domain.technical.day_value import DayValue
from screener.domain.technical.historical_prices import HistoricalValues
from screener.exceptions.not_found import HistoricalPricesIsNotAvailable


class TestHistoricalPrices(TestCase):
    def assert_dict_to_time_value(self, values_dict, time_values):
        for index, time_value in enumerate(time_values):
            self.assertEqual(values_dict[index]["value"], time_value.get_value())
            self.assertEqual(values_dict[index]["date"], time_value.get_date())

    def test_get_simple_moving_average_when_all_values_are_the_same(self):
        day_values = HistoricalValues([DayValue("1", 2, 2, 1, 2, 100),
                                       DayValue("2", 2, 2, 1, 2, 100),
                                       DayValue("3", 2, 2, 1, 2, 100),
                                       DayValue("4", 2, 2, 1, 2, 100),
                                       DayValue("5", 2, 2, 1, 2, 100)])

        simple_averages = day_values.get_simple_moving_averages(2)

        expected_values = [{'date': '2', 'value': 2.0},
                           {'date': '3', 'value': 2.0},
                           {'date': '4', 'value': 2.0},
                           {'date': '5', 'value': 2.0}]
        self.assert_dict_to_time_value(expected_values, simple_averages)

    def test_get_simple_moving_average_when_values_are_different(self):
        day_values = HistoricalValues([DayValue("1", 4, 4, 1, 2, 100),
                                       DayValue("2", 2, 2, 1, 2, 100),
                                       DayValue("3", 10, 10, 1, 2, 100),
                                       DayValue("4", 4, 4, 1, 2, 100),
                                       DayValue("5", 5, 5, 1, 2, 100)])

        simple_averages = day_values.get_simple_moving_averages(2)

        expected_values = [{'date': '2', 'value': 3.0},
                           {'date': '3', 'value': 6.0},
                           {'date': '4', 'value': 7.0},
                           {'date': '5', 'value': 4.5}]
        self.assert_dict_to_time_value(expected_values, simple_averages)

    def test_get_exponential_moving_averages_when_all_values_are_the_same(self):
        day_values = HistoricalValues([DayValue("1", 2.0, 2.0, 1, 2, 100),
                                       DayValue("2", 2.0, 2.0, 1, 2, 100),
                                       DayValue("3", 2.0, 2.0, 1, 2, 100),
                                       DayValue("4", 2.0, 2.0, 1, 2, 100),
                                       DayValue("5", 2.0, 2.0, 1, 2, 100)])

        exponential_average = day_values.get_exponential_moving_averages(2)

        self.assert_dict_to_time_value([{'date': '2', 'value': 2.0},
                                        {'date': '3', 'value': 2.0},
                                        {'date': '4', 'value': 2.0},
                                        {'date': '5', 'value': 2.0}],
                                       exponential_average)

    def test_get_exponential_moving_averages_when_values_are_different(self):
        day_values = HistoricalValues([DayValue("1", 4, 4, 1, 2, 100),
                                       DayValue("2", 2.0, 2.0, 1, 2, 100),
                                       DayValue("3", 10, 10, 1, 2, 100),
                                       DayValue("4", 4, 4, 1, 2, 100),
                                       DayValue("5", 5, 5, 1, 2, 100)])

        exponential_averages = day_values.get_exponential_moving_averages(2)

        self.assert_dict_to_time_value([{'date': '2', 'value': 3.0},
                                        {'date': '3', 'value': 7.666666666666666},
                                        {'date': '4', 'value': 5.222222222222222},
                                        {'date': '5', 'value': 5.074074074074074}],
                                       exponential_averages)

    def test_get_exponential_moving_averages_when_values_are_different_and_number_of_days_one(self):
        day_values = HistoricalValues([DayValue("1", 4, 4, 1, 2, 100),
                                       DayValue("2", 2, 2, 1, 2, 100),
                                       DayValue("3", 10, 10, 1, 2, 100),
                                       DayValue("4", 4, 4, 1, 2, 100),
                                       DayValue("5", 5, 5, 1, 2, 100)])

        exponential_averages = day_values.get_exponential_moving_averages(1)

        self.assert_dict_to_time_value([{'date': '1', 'value': 4.0},
                                        {'date': '2', 'value': 2.0},
                                        {'date': '3', 'value': 10.0},
                                        {'date': '4', 'value': 4.0},
                                        {'date': '5', 'value': 5.0}],
                                       exponential_averages)

    def test_golden_cross_when_return_true_when_golden_point_just_crossed(self):
        day_values = HistoricalValues([DayValue("1", 4, 4, 1, 2, 100),
                                       DayValue("2", 14, 14, 1, 2, 100),
                                       DayValue("3", 10, 10, 1, 2, 100),
                                       DayValue("4", 14, 14, 1, 2, 100),
                                       DayValue("5", 15, 15, 1, 2, 100)])

        golden_cross = day_values.golden_cross(3, 2)

        self.assertTrue(golden_cross)

    def test_golden_cross_when_return_true_when_short_term_and_long_term_equals(self):
        day_values = HistoricalValues([DayValue("1", 2, 2, 1, 2, 100),
                                       DayValue("2", 6, 6, 1, 2, 100),
                                       DayValue("3", 3, 3, 1, 2, 100),
                                       DayValue("4", 4, 4, 1, 2, 100),
                                       DayValue("5", 2, 2, 1, 2, 100)])

        golden_cross = day_values.golden_cross(3, 2)

        self.assertTrue(golden_cross)

    def test_golden_cross_when_return_false_when_golden_cross_is_not_reached(self):
        day_values = HistoricalValues([DayValue("1", 2, 2, 1, 2, 100),
                                       DayValue("2", 6, 6, 1, 2, 100),
                                       DayValue("3", 4, 4, 1, 2, 100),
                                       DayValue("4", 4, 4, 1, 2, 100),
                                       DayValue("5", 3, 3, 1, 2, 100)])

        golden_cross = day_values.golden_cross(3, 2)

        self.assertFalse(golden_cross)

    def test_golden_cross_when_return_false_when_golden_cross_is_already_reached(self):
        day_values = HistoricalValues([DayValue("1", 2, 2, 1, 2, 100),
                                       DayValue("2", 6, 6, 1, 2, 100),
                                       DayValue("3", 4, 4, 1, 2, 100),
                                       DayValue("4", 4, 4, 1, 2, 100),
                                       DayValue("5", 3, 3, 1, 2, 100)])

        golden_cross = day_values.golden_cross(2, 1)

        self.assertFalse(golden_cross)

    def test_death_cross_when_return_true_when_death_point_just_crossed(self):
        day_values = HistoricalValues([DayValue("1", 5, 5, 1, 2, 100),
                                       DayValue("2", 4, 4, 1, 2, 100),
                                       DayValue("3", 5, 5, 1, 2, 100),
                                       DayValue("4", 5, 5, 1, 2, 100),
                                       DayValue("5", 1, 1, 1, 2, 100)])

        death_cross = day_values.death_cross(3, 2)

        self.assertTrue(death_cross)

    def test_death_cross_when_return_true_when_short_term_and_long_term_equals(self):
        day_values = HistoricalValues([DayValue("1", 5, 5, 1, 2, 100),
                                       DayValue("2", 4, 4, 1, 2, 100),
                                       DayValue("3", 5, 5, 1, 2, 100),
                                       DayValue("4", 5, 5, 1, 2, 100),
                                       DayValue("5", 5, 5, 1, 2, 100)])

        death_cross = day_values.death_cross(3, 2)

        self.assertTrue(death_cross)

    def test_death_cross_when_return_false_when_death_cross_is_not_reached(self):
        day_values = HistoricalValues([DayValue("1", 2, 2, 1, 2, 100),
                                       DayValue("2", 6, 6, 1, 2, 100),
                                       DayValue("3", 4, 4, 1, 2, 100),
                                       DayValue("4", 4, 4, 1, 2, 100),
                                       DayValue("5", 6, 6, 1, 2, 100)])

        death_cross = day_values.death_cross(3, 2)

        self.assertFalse(death_cross)

    def test_death_cross_when_return_false_when_death_cross_is_already_reached(self):
        day_values = HistoricalValues([DayValue("1", 5, 5, 1, 2, 100),
                                       DayValue("2", 4, 4, 1, 2, 100),
                                       DayValue("3", 3, 3, 1, 2, 100),
                                       DayValue("4", 2, 2, 1, 2, 100),
                                       DayValue("5", 1, 1, 1, 2, 100)])

        death_cross = day_values.death_cross(2, 1)

        self.assertFalse(death_cross)

    @staticmethod
    def _side_effect_standard_deviation_band(values, extractor):
        if values[0].get_value() == 5:
            return 2
        elif values[0].get_value() == 4:
            return 2.4
        elif values[0].get_value() == 7:
            return 2.3

    @mock.patch.object(math, "standard_deviation")
    @mock.patch.object(math, "average")
    def test_bollinger_band(self, mocked_math_average, mocked_standard_deviation):
        day_values = HistoricalValues([DayValue("1", 5, 5, 1, 2, 100),
                                       DayValue("2", 4, 4, 1, 2, 100),
                                       DayValue("3", 7, 7, 1, 2, 100),
                                       DayValue("4", 2, 2, 1, 2, 100),
                                       DayValue("5", 8, 8, 1, 2, 100)])

        mocked_math_average.return_value = 2.7777777778
        mocked_standard_deviation.side_effect = TestHistoricalPrices._side_effect_standard_deviation_band

        bollinger_bands = day_values.get_bollinger_band(3, 1)

        self.assertEqual(bollinger_bands[0].get_upper_band(), 4.7777777778)
        self.assertEqual(bollinger_bands[0].get_lower_band(), 0.7777777777999999)

        self.assertEqual(bollinger_bands[1].get_upper_band(), 4.844444444466666)
        self.assertEqual(bollinger_bands[1].get_lower_band(), 0.04444444446666651)

        self.assertEqual(bollinger_bands[2].get_upper_band(), 5.18888888891111)
        self.assertEqual(bollinger_bands[2].get_lower_band(), 0.5888888889111108)

    def test_rsi_when_price_is_increasing(self):
        day_values = HistoricalValues([DayValue("1", 100, 100, 1, 2, 100),
                                       DayValue("2", 102, 102, 1, 2, 100),
                                       DayValue("3", 104, 104, 1, 2, 100),
                                       DayValue("4", 106, 106, 1, 2, 100),
                                       DayValue("5", 108, 108, 1, 2, 100)])

        relative_strengths = day_values.get_relative_strength_index(2)

        self.assertEqual(len(relative_strengths), 4)
        expected_rsi = [{
            "date": "2",
            "value": 99.50248756218906,
        }, {
            "date": "3",
            "value": 99.74816058466249,
        }, {
            "date": "4",
            "value": 99.83033194033212,
        }, {
            "date": "5",
            "value": 99.87147609444018,
        }]
        for index, rsi in enumerate(relative_strengths):
            self._assert_rsi(rsi, expected_rsi[index])

    def test_rsi_when_price_is_decreasing(self):
        day_values = HistoricalValues([DayValue("1", 110, 110, 1, 2, 100),
                                       DayValue("2", 108, 108, 1, 2, 100),
                                       DayValue("3", 106, 106, 1, 2, 100),
                                       DayValue("4", 104, 104, 1, 2, 100),
                                       DayValue("5", 102, 102, 1, 2, 100)])

        relative_strengths = day_values.get_relative_strength_index(2)

        self.assertEqual(len(relative_strengths), 4)
        expected_rsi = [{
            "date": "2",
            "value": 0,
        }, {
            "date": "3",
            "value": 0,
        }, {
            "date": "4",
            "value": 0,
        }, {
            "date": "5",
            "value": 0,
        }]
        for index, rsi in enumerate(relative_strengths):
            self._assert_rsi(rsi, expected_rsi[index])

    def test_rsi_when_price_is_first_increasing_then_decreasing(self):
        day_values = HistoricalValues([DayValue("1", 110, 110, 1, 2, 100),
                                       DayValue("2", 112, 112, 1, 2, 100),
                                       DayValue("3", 106, 106, 1, 2, 100),
                                       DayValue("4", 104, 104, 1, 2, 100),
                                       DayValue("5", 102, 102, 1, 2, 100)])

        relative_strengths = day_values.get_relative_strength_index(2)

        self.assertEqual(len(relative_strengths), 4)
        expected_rsi = [{
            "date": "2",
            "value": 99.45300845350572,
        }, {
            "date": "3",
            "value": 25.304101071809427,
        }, {
            "date": "4",
            "value": 20.041427954442753,
        }, {
            "date": "5",
            "value": 16.536150337229643,
        }]
        for index, rsi in enumerate(relative_strengths):
            self._assert_rsi(rsi, expected_rsi[index])

    def test_stochastic_oscillator_should_have_zero_when_lowest_decreasing(self):
        day_values = HistoricalValues([DayValue("1", 110, 110, 1, 2, 100),
                                       DayValue("2", 108, 108, 1, 2, 100),
                                       DayValue("3", 106, 106, 1, 2, 100),
                                       DayValue("4", 104, 104, 1, 2, 100),
                                       DayValue("5", 102, 102, 1, 2, 100)])

        stochastic_value = day_values.get_stochastic_oscillator(2, 2)

        expected_stochastic_oscillator = [{
            "date": "2",
            "slow_oscillator": 0,
            "fast_oscillator": 0
        }, {
            "date": "3",
            "slow_oscillator": 0,
            "fast_oscillator": 0
        }, {
            "date": "4",
            "slow_oscillator": 0,
            "fast_oscillator": 0
        }, {
            "date": "5",
            "slow_oscillator": 0,
            "fast_oscillator": 0
        }]

        for index, stochastic_oscillator in enumerate(stochastic_value):
            self._assert_stochastic_oscillator(stochastic_oscillator, expected_stochastic_oscillator[index])

    def test_stochastic_oscillator_should_have_100_when_increasing(self):
        day_values = HistoricalValues([DayValue("1", 102, 102, 1, 2, 100),
                                       DayValue("2", 104, 104, 1, 2, 100),
                                       DayValue("3", 106, 106, 1, 2, 100),
                                       DayValue("4", 108, 108, 1, 2, 100),
                                       DayValue("5", 110, 110, 1, 2, 100)])

        stochastic_values = day_values.get_stochastic_oscillator(2, 2)

        expected_stochastic_oscillator = [{
            "date": "2",
            "slow_oscillator": 99.50248756218907,
            "fast_oscillator": 49.75124378109454
        }, {
            "date": "3",
            "slow_oscillator": 99.50248756218907,
            "fast_oscillator": 99.50248756218907
        }, {
            "date": "4",
            "slow_oscillator": 99.50248756218907,
            "fast_oscillator": 99.50248756218909
        }, {
            "date": "5",
            "slow_oscillator": 99.50248756218907,
            "fast_oscillator": 99.50248756218909
        }]

        for index, stochastic_oscillator in enumerate(stochastic_values):
            self._assert_stochastic_oscillator(stochastic_oscillator, expected_stochastic_oscillator[index])

    def test_to_dict(self):
        historical_prices = HistoricalValues([DayValue("1", 102, 102, 1, 2, 100),
                                              DayValue("2", 104, 104, 1, 2, 100)])

        prices_as_dict = historical_prices.to_dict()

        self.assertListEqual([{
            "date": "1",
            "open": 102,
            "value": 102,
            "low": 1,
            "high": 2,
            "volume": 100
        }, {
            "date": "2",
            "open": 104,
            "value": 104,
            "low": 1,
            "high": 2,
            "volume": 100
        }], prices_as_dict)

    def test_number_of_days_stock_in_market(self):
        historical_prices = HistoricalValues([DayValue("1", 102, 102, 1, 2, 100),
                                              DayValue("2", 104, 104, 1, 2, 100)])

        self.assertEqual(2, historical_prices.number_of_days_stock_in_market())

    @staticmethod
    def _get_historical_prices():
        return HistoricalValues([
            DayValue("19-06-2020", 2079.0, 2100.8, 2100.0, 4673557.0, 209275),
            DayValue("22-06-2020", 2110.0, 2092.75, 2118.9, 2487252.0, 21008),
            DayValue("23-06-2020", 2115.0, 2155.95, 2172.0, 4309193.0, 215595),
            DayValue("24-06-2020", 2172.0, 2130.3, 2176.9, 3023031.0, 21303),
            DayValue("25-06-2020", 2114.3, 2173.15, 2189.9, 8208083.0, 217315),
            DayValue("26-06-2020", 2179.95, 2154.2, 2179.95, 3176495.0, 21542),
            DayValue("29-06-2020", 2151.35, 2382.95, 2195.9, 3295050.0, 218295),
            DayValue("30-06-2020", 2193.8, 2180.0, 2199.95, 2373121.0, 21800),
            DayValue("01-07-2020", 2183.0, 2170.4, 2191.8, 1532935.0, 21704),
            DayValue("02-07-2020", 2167.75, 2151.75, 2177.65, 2588845.0, 215175),
            DayValue("03-07-2020", 2165.5, 2173.7, 2188.0, 1946326.0, 21737),
            DayValue("06-07-2020", 2180.0, 2161.6, 2180.0, 2375701.0, 21616),
            DayValue("07-07-2020", 2175.5, 2154.15, 2175.5, 2014697.0, 215415),
            DayValue("08-07-2020", 2153.6, 2186.05, 2194.0, 3350115.0, 218605),
            DayValue("09-07-2020", 2183.0, 2175.85, 2219.95, 3039821.0, 217585),
            DayValue("10-07-2020", 2170.0, 2223.8, 2232.0, 3179517.0, 22238),
            DayValue("13-07-2020", 2239.0, 2265.25, 2275.0, 4556688.0, 226525),
            DayValue("14-07-2020", 2264.8, 2234.75, 2269.95, 2403257.0, 223475),
            DayValue("15-07-2020", 2237.25, 2275.15, 2291.0, 2474553.0, 227515),
            DayValue("16-07-2020", 2275.25, 2287.85, 2291.3, 2495150.0, 228785),
            DayValue("17-07-2020", 2285.0, 2334.55, 2340.0, 3088773.0, 233455),
            DayValue("20-07-2020", 2334.55, 2330.95, 2343.3, 2816285.0, 233095),
            DayValue("21-07-2020", 2348.0, 2318.0, 2350.0, 3037830.0, 23180),
            DayValue("22-07-2020", 2330.0, 2248.5, 2330.0, 6950011.0, 22485),
            DayValue("23-07-2020", 2260.0, 2211.35, 2267.15, 3936886.0, 221135),
            DayValue("24-07-2020", 2200.0, 2209.3, 2220.0, 4203390.0, 22093),
            DayValue("27-07-2020", 2217.75, 2221.5, 2235.95, 2209431.0, 22215),
            DayValue("28-07-2020", 2230.95, 2242.55, 2244.9, 1567889.0, 224255),
            DayValue("29-07-2020", 2235.0, 2231.3, 2262.2, 2404989.0, 22313),
            DayValue("30-07-2020", 2231.3, 2195.6, 2238.05, 2046188.0, 21956),
            DayValue("31-07-2020", 2197.5, 2209.9, 2221.95, 1715834.0, 22099),
            DayValue("03-08-2020", 2209.8, 2204.5, 2223.05, 1683798.0, 22045),
            DayValue("04-08-2020", 2209.9, 2197.8, 2218.9, 1981721.0, 21978),
            DayValue("05-08-2020", 2202.0, 2194.55, 2209.9, 1715481.0, 219455),
            DayValue("06-08-2020", 2200.0, 2220.45, 2229.0, 1824540.0, 222045),
            DayValue("07-08-2020", 2223.0, 2210.55, 2234.8, 1778051.0, 221055),
            DayValue("10-08-2020", 2218.0, 2206.75, 2226.75, 1476389.0, 220675),
            DayValue("11-08-2020", 2209.05, 2210.65, 2233.0, 1665204.0, 221065),
            DayValue("12-08-2020", 2200.05, 2195.1, 2209.05, 1170455.0, 21951),
            DayValue("13-08-2020", 2200.0, 2198.65, 2217.0, 1453429.0, 219865),
            DayValue("14-08-2020", 2204.0, 2173.9, 2216.0, 1341691.0, 21739),
            DayValue("17-08-2020", 2181.0, 2196.05, 2203.65, 1559579.0, 219605),
            DayValue("18-08-2020", 2204.0, 2214.35, 2216.8, 1339002.0, 221435),
            DayValue("19-08-2020", 2206.0, 2193.6, 2221.5, 1585132.0, 21936),
            DayValue("20-08-2020", 2186.0, 2185.7, 2197.8, 1768939.0, 21857),
            DayValue("21-08-2020", 2199.0, 2202.05, 2208.7, 1374412.0, 220205)
        ])

    def test_minimum_price_in_given_days__when_stock_in_market_more_than_given_days(self):
        self.assertEqual(2181.0, self._get_historical_prices().minimum_price_in_given_days(5))

    def test_minimum_price_in_given_days__when_stock_in_market_less_than_given_days(self):
        self.assertEqual(2079.0, self._get_historical_prices().minimum_price_in_given_days(200))

    def test_minimum_price_in_given_days__when_stock_in_market_equal_given_days(self):
        self.assertEqual(2079.0, self._get_historical_prices().minimum_price_in_given_days(46))

    def test_maximum_price_in_given_days__when_stock_in_market_more_than_given_days(self):
        self.assertEqual(2206.0, self._get_historical_prices().maximum_price_in_given_days(5))

    def test_maximum_price_in_given_days__when_stock_in_market_more_than_given_days_and_price_is_in_string(self):
        historical_prices = HistoricalValues([
            DayValue("19-06-2020", "2079.0", "2100.8", "2100.0", "4673557.0", 209275),
            DayValue("22-06-2020", "2110.0", "2092.75", "2118.9", "2487252.0", 21008),
            DayValue("23-06-2020", "2115.0", "2155.95", "2172.0", "4309193.0", 215595)])
        self.assertEqual(2115.0, historical_prices.maximum_price_in_given_days(2))

    def test_maximum_price_in_given_days__when_stock_in_market_less_than_given_days(self):
        self.assertEqual(2348.0, self._get_historical_prices().maximum_price_in_given_days(200))

    def test_maximum_price_in_given_days__when_stock_in_market_equal_given_days(self):
        self.assertEqual(2348.0, self._get_historical_prices().maximum_price_in_given_days(46))

    def test_get_latest_price__raise_exception__when_no_exception_is_raised(self):
        with self.assertRaises(HistoricalPricesIsNotAvailable):
            HistoricalValues().get_latest_price()

    def test_get_latest_price(self):
        latest_price = HistoricalValues([1, 2]).get_latest_price()
        self.assertEqual(2, latest_price)

    def test_add_latest_price(self):
        day_value1 = DayValue("1", 1, 1, 1, 1, 1)
        day_value2 = DayValue("2", 1, 1, 1, 1, 1)
        historical_prices = HistoricalValues([day_value1, day_value2])
        day_value3 = DayValue("3", 1, 1, 1, 1, 1)
        historical_prices.add_latest_price([day_value3])
        self.assertListEqual([day_value1, day_value2, day_value3], historical_prices._day_values)

    def test_get_current_price(self):
        day_value1 = DayValue("1", 1, 1, 1, 1, 1)
        day_value2 = DayValue("2", 1.5, 1, 1, 1, 1)
        historical_prices = HistoricalValues([day_value1, day_value2])
        current_price = historical_prices.get_current_price()
        self.assertEqual(1.5, current_price)

    def test_get_current_price__return_None__when_prices_not_found(self):
        historical_prices = HistoricalValues([])
        self.assertIsNone(historical_prices.get_current_price())

    def test_get_date_of_latest_available_price__return_01_01_1990__when_there_is_not_any_historical_price(self):
        self.assertEqual("01-01-1990", HistoricalValues().get_date_of_latest_available_price())

    def test_get_date_of_latest_available_price_price(self):
        latest_date = HistoricalValues(
            [mock.Mock(get_date=lambda: 1), mock.Mock(get_date=lambda: 2)]).get_date_of_latest_available_price()
        self.assertEqual(2, latest_date)

    def test_stochastic_oscillator(self):
        day_values = HistoricalValues([DayValue("1", 102, 102, 1, 2, 100),
                                       DayValue("2", 104, 104, 1, 2, 100),
                                       DayValue("3", 101, 101, 1, 2, 100),
                                       DayValue("4", 102, 102, 1, 2, 100),
                                       DayValue("5", 110, 110, 1, 2, 100),
                                       DayValue("6", 105, 105, 1, 2, 100),
                                       DayValue("7", 109, 109, 1, 2, 100)])

        stochastic_values = day_values.get_stochastic_oscillator(3, 3)

        expected_stochastic_oscillator = [{
            "date": "3",
            "slow_oscillator": 0,
            "fast_oscillator": 0
        }, {
            "date": "4",
            "slow_oscillator": 33.222591362126245,
            "fast_oscillator": 11.074197120708748
        }, {
            "date": "5",
            "slow_oscillator": 99.88901220865705,
            "fast_oscillator": 44.37053452359443
        }, {
            "date": "6",
            "slow_oscillator": 37.453183520599254,
            "fast_oscillator": 56.854929030460845
        }, {
            "date": "7",
            "slow_oscillator": 79.84031936127745,
            "fast_oscillator": 72.39417169684458
        }]

        for index, stochastic_oscillator in enumerate(stochastic_values):
            self._assert_stochastic_oscillator(stochastic_oscillator, expected_stochastic_oscillator[index])

    def _assert_stochastic_oscillator(self, actual, expected):
        self.assertEqual(expected["date"], actual.get_date())
        self.assertEqual(expected["slow_oscillator"], actual.get_slow_oscillator())
        self.assertEqual(expected["fast_oscillator"], actual.get_fast_oscillator())

    def _assert_rsi(self, actual, expected):
        self.assertEqual(actual.get_value(), expected["value"])
        self.assertEqual(actual.get_date(), expected["date"])
