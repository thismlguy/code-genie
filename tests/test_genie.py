from unittest import TestCase

import pandas as pd

from code_genie import Genie
from code_genie.genie import PandasGenie


class Test(TestCase):

    def test_add(self):
        # use genie to get a method to add 2 numbers
        add = Genie(instructions="add num1 and num2",
                    inputs={"num1": "int", "num2": "int"},
                    allowed_imports=["math"])
        # call the method
        self.assertEqual(add(num1=1, num2=2), 3)
        self.assertEqual(add(6, 12), 18)

    def test_pd_mean(self):
        # use genie to get a method to get the mean of a list of numbers
        mean_sum = PandasGenie(instructions="sum of mean of columns x and y",
                               columns=["x", "y"])
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        # call the method
        self.assertEqual(mean_sum(df=df), 7)
