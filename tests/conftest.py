import os

import pytest
from dotenv import load_dotenv

from code_genie import _Config, set_options
from code_genie.client import Client


@pytest.fixture(scope="module")
def client():
    # path to 2 directories above current file
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(path)
    return Client()


@pytest.fixture(scope="module")
def default_config():
    return _Config


@pytest.fixture(scope="module")
def cache_dir():
    # path to _cache dir in same directory as this file
    return os.path.join(os.path.dirname(__file__), "_cache")


@pytest.fixture(scope="module", autouse=True)
def set_cache_dir(cache_dir):
    # clear cache_dir
    if os.path.exists(cache_dir):
        for file in os.listdir(cache_dir):
            os.remove(os.path.join(cache_dir, file))
    set_options({"cache_dir": cache_dir})
