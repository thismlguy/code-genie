import pandas as pd

from code_genie import Genie


def test_add(client):
    # use genie to get a method to add 2 numbers
    genie = Genie(inputs={"num1": 4, "num2": 2}, client=client)

    # call the method
    assert genie.plz(instructions="add num1 and num2") == 6
    assert genie.plz(instructions="multiply num1 and num2") == 8


def test_pd_mean(client):
    df = pd.DataFrame({"x": [1, 2, 3, 1, 2, 3], "y": [4, 5, 6, 4, 5, 6]})
    genie = Genie(inputs={"df": df}, client=client)

    # call the method
    assert genie.plz(instructions="sum of mean of x and y") == 7
    assert set(genie.plz(instructions="distinct values of x")) == {1, 2, 3}


def test_cache(client):
    # use genie to get a method to add 2 numbers
    genie = Genie(inputs={"num1": 4, "num2": 2}, client=client)

    # call the method
    assert genie.plz(instructions="add num1 and num2") == 6
    last_run_id_1 = genie.last_run_id

    assert genie.plz(instructions="add num1 and num2") == 6
    last_run_id_2 = genie.last_run_id
    assert last_run_id_1 == last_run_id_2

    assert genie.plz(instructions="add num1 and num2", override=True) == 6
    assert last_run_id_2 != genie.last_run_id
