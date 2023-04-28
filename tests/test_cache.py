from unittest import TestCase

from code_genie import Genie
from code_genie import PandasGenie


class Test(TestCase):

    @staticmethod
    def _get_add_genie(override=False):
        return Genie(instructions="add num1 and num2",
                     inputs={"num1": "int", "num2": "int"},
                     allowed_imports=["math"],
                     override=override)

    @staticmethod
    def _get_mean_genie(override=False):
        # use genie to get a method to get the mean of a list of numbers
        return PandasGenie(instructions="sum of mean of columns x and y",
                               columns=["x", "y"],
                           override=override)

    def test_genie(self):
        # use genie to get a method to add 2 numbers
        add_1 = self._get_add_genie(override=True)
        add_2 = self._get_add_genie()
        self.assertEqual(add_1.code, add_2.code)

    def test_pd_genie(self):
        mean_1 = self._get_mean_genie(override=True)
        mean_2 = self._get_mean_genie()
        self.assertEqual(mean_1.code, mean_2.code)
