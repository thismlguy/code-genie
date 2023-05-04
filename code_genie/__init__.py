__version__ = "0.3.0-dev0"

from code_genie._cache import _CacheManager
from code_genie.genie import Genie


def set_cache_dir(path: str):
    """
    Set global options for the package

    Args:
        path: path to the cache dir
    """
    _CacheManager._set_cache_dir(path)
