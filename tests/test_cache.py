from code_genie import _CacheManager
from code_genie.genie import Genie, PandasGenie


def _get_add_genie(client, cache_dir, override=False):
    return Genie(instructions="add num1 and num2",
                 inputs={"num1": "int", "num2": "int"},
                 allowed_imports=["math"],
                 override=override,
                 client=client,
                 cache_dir=cache_dir)


def _get_mean_genie(client, cache_dir, override=False):
    # use genie to get a method to get the mean of a list of numbers
    return PandasGenie(instructions="sum of mean of columns x and y",
                           columns=["x", "y"],
                       override=override,
                       client=client,
                       cache_dir=cache_dir)


def test_genie(client, cache_dir):
    # use genie to get a method to add 2 numbers
    add_1 = _get_add_genie(client, cache_dir, override=True)
    add_2 = _get_add_genie(client, cache_dir)
    assert add_1.code == add_2.code

    cache = _CacheManager(cache_dir)
    cache_data = cache.get(add_1._get_hash_str())
    assert cache_data.filename == add_1._filename
    assert cache_data.fn_name == add_1._fn_name


def test_pd_genie(client, cache_dir):
    mean_1 = _get_mean_genie(client, cache_dir, override=True)
    mean_2 = _get_mean_genie(client, cache_dir)
    assert mean_1.code == mean_2.code

    cache = _CacheManager(cache_dir)
    cache_data = cache.get(mean_1._get_hash_str())
    assert cache_data.filename == mean_1._filename
    assert cache_data.fn_name == mean_1._fn_name
