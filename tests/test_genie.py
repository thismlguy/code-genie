import pandas as pd

from code_genie.genie import PandasGenie, Genie


def test_add(client):
    # use genie to get a method to add 2 numbers
    add = Genie(instructions="add num1 and num2",
                inputs={"num1": "int", "num2": "int"},
                allowed_imports=["math"],
                client=client)
    # call the method
    assert add(num1=1, num2=2) == 3
    assert add(6, 12) == 18


def test_pd_mean(client):
    # use genie to get a method to get the mean of a list of numbers
    mean_sum = PandasGenie(instructions="sum of mean of columns x and y",
                           columns=["x", "y"],
                           client=client)
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    # call the method
    assert mean_sum(df=df) == 7
