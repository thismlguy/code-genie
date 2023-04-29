import os

import pytest
from dotenv import load_dotenv

from code_genie.client import Client


@pytest.fixture(scope="module")
def client():
    # path to 2 directories above current file
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(path)
    return Client()


@pytest.fixture(scope="module")
def cache_dir():
    # path to _cache dir in same directory as this file
    return os.path.join(os.path.dirname(__file__), "_cache")
