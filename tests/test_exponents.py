"""
test_exponents.py
"""

from expona.exponents import ExponentCalculator
from unittest import TestCase, main


class ExponentCalculatorTests(TestCase):

    def setUp(self):
        self.ec = ExponentCalculator()

    def test_set_exponents(self):
        exponents = [1, 2, 3]
        self.ec.exponents = exponents
        self.assertListEqual(list(self.ec.exponents), exponents)

    def test_multiple_get(self):
        exponents = [1, 2, 3]
        self.ec.exponents = exponents
        self.assertListEqual(list(self.ec.exponents), exponents)
        self.assertListEqual(list(self.ec.exponents), exponents)

    def test_add_exponent(self):
        exponents = [1, 2, 3]
        next_exponents = [4, 5, 6]
        self.ec.exponents = exponents
        self.ec.add_exponents(next_exponents)
        self.assertListEqual(list(self.ec.exponents), exponents + next_exponents)

    def test_expon(self):
        exponents = [1, 2]
        numbers = [2, 3]
        
        self.ec.exponents = exponents
        result = list(self.ec.expon(numbers))
        
        expected = [
                "(2)^(1) = 2",
                "(2)^(2) = 4",
                "(3)^(1) = 3",
                "(3)^(2) = 9"
                ]

        self.assertListEqual(result, expected)
