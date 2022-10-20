import unittest

from screener.common.u_dict import merge_dict


class TestUtil(unittest.TestCase):
    def _test_dict_merge(self, dict1, dict2, exp_dict):
        merge_dict(dict1, dict2)
        self.assertDictEqual(dict1, exp_dict)

    def test_merge_one_empty_one_not(self):
        dict1 = {}
        dict2 = {1: 3, 2: 'r'}
        exp_dict = {1: 3, 2: 'r'}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_both_non_empty(self):
        dict1 = {'a': 2, 'b': 3}
        dict2 = {'c': 1}
        exp_dict = {'a': 2, 'b': 3, 'c': 1}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_one_nested_dict(self):
        dict1 = {'a': 2, 'b': 3, 'd': {'e': 1}}
        dict2 = {'c': 1}
        exp_dict = {'a': 2, 'b': 3, 'c': 1, 'd': {'e': 1}}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_two_nested_non_overlapping_key_dicts(self):
        dict1 = {'a': 2, 'd': {'e': 1}}
        dict2 = {'c': 1, 'f': {'g': 2}, 'h': [1, 2]}
        exp_dict = {'a': 2, 'c': 1, 'h': [1, 2], 'd': {'e': 1}, 'f': {'g': 2}}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_two_nested_having_set(self):
        dict1 = {'a': 2, 'h': "abc"}
        dict2 = {'c': 1, 'h': "cde"}
        exp_dict = {'a': 2, 'c': 1, 'h': 'abc'}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_two_nested_overlapping_key_dicts(self):
        dict1 = {
            'a': 2,
            'd': {
                'e': 1,
                'k': {
                    'l': [2, 3]
                }
            },
            'n': [1]
        }
        dict2 = {
            'c': 1,
            'd': {
                'g': 2,
                'k': {
                    'm': {'n': 2}
                }
            },
            'h': [1, 2],
            'n': [4]
        }
        exp_dict = {
            'a': 2,
            'c': 1,
            'h': [1, 2],
            'd': {
                'e': 1,
                'g': 2,
                'k': {
                    'l': [2, 3],
                    'm': {'n': 2}
                }
            },
            'n': [1, 4]
        }
        self._test_dict_merge(dict1, dict2, exp_dict)
