from unittest import TestCase

from code_genie import Genie
from code_genie.client import Client


class Test(TestCase):

    def test_add(self):
        # use genie to get a method to add 2 numbers
        add = Genie(instructions="add num1 and num2",
                    inputs={"num1": "int", "num2": "int"},
                    allowed_imports=["math"],
                    client=Client())
        # call the method
        self.assertEqual(add(num1=1, num2=2), 3)
        self.assertEqual(add(num1=6, num2=12), 18)
