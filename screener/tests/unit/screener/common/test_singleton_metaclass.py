from unittest import TestCase

from screener.common.singleton_metaclass import Singleton


class TestClass(metaclass=Singleton):
    def __init__(self, a):
        self.a = a


class TestSingleton(TestCase):
    def test_should_create_an_instance_of_class(self):
        test = TestClass(2)

        self.assertIsNotNone(test)
        self.assertTrue(isinstance(test, TestClass))

    def test_should_create_only_one_instance(self):
        test1 = TestClass(2)
        test2 = TestClass(3)
        test3 = TestClass(4)

        self.assertEqual(id(test1), id(test2))
        self.assertEqual(id(test1), id(test3))
