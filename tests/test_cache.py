from code_genie.genie import Genie, PandasGenie


def _get_add_genie(client, override=False):
    return Genie(instructions="add num1 and num2",
                 inputs={"num1": "int", "num2": "int"},
                 allowed_imports=["math"],
                 override=override,
                 client=client)


def _get_mean_genie(client, override=False):
    # use genie to get a method to get the mean of a list of numbers
    return PandasGenie(instructions="sum of mean of columns x and y",
                           columns=["x", "y"],
                       override=override,
                       client=client)


def test_genie(client):
    # use genie to get a method to add 2 numbers
    add_1 = _get_add_genie(client, override=True)
    add_2 = _get_add_genie(client)
    assert add_1.code == add_2.code


def test_pd_genie(client):
    mean_1 = _get_mean_genie(client, override=True)
    mean_2 = _get_mean_genie(client)
    assert mean_1.code == mean_2.code
