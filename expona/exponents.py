"""
exponents.py
"""

import copy
from itertools import chain, product
from utils.expona_logging import logger_factory


logger = logger_factory("ExponentCalculator")


class ExponentCalculator:
    """
    Stateful exponent calculator.
    """

    def __init__(self, exponents=None):
        if not exponents:
            exponents = []
        self._exponents = None
        self.exponents = exponents

    @property
    def exponents(self):
        """Get exponents."""

        if not self._exponents:
            self._exponents = []

        return copy.deepcopy(self._exponents)

    @exponents.setter
    def exponents(self, exponent_list):
        """Set exponents."""

        try:
            self._exponents = iter(exponent_list)
        except TypeError:
            logger.error("Could not set exponent list to %s for %r.", str(exponent_list), self)

    def add_exponents(self, exponents):
        """Add new exponents."""

        try:
            self.exponents = chain(self.exponents, exponents)
        except TypeError:
            logger.error("Could not expand exponent list with %s for %r.", str(exponents), self)

    def expon(self, numbers):
        """Exponentiate numbers."""

        cartesian = product(numbers, self.exponents)
        for x, y in cartesian:
            yield "({x})^({y}) = {z}".format(x=x, y=y, z=x**y)
