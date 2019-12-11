import unittest

from arithmetic import add, substract, multiply, divide


class ArithmeticTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(3, 7), 10, 'Should be 10')

    def test_substract(self):
        self.assertEqual(substract(9, 4), 5, 'Should be 5')
        self.assertEqual(substract(4, 9), -5, 'Should be -5')

    def test_multiply(self):
        self.assertEqual(multiply(25, 5), 125, 'Should be 125')

    def test_divide(self):
        self.assertEqual(divide(4, 2), 2.0, 'Should be 2.0')
        self.assertEqual(divide(2, 4), 0.5, 'Should be 0.5')
        self.assertEqual(divide(0, 3), 0.0, 'Should be 0.0')
        with self.assertRaises(ZeroDivisionError):
            divide(3, 0)
        # self.assertRaises(ZeroDivisionError, divide, 3, 0)
