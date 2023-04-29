__version__ = "0.2.0"

from code_genie._cache import _CacheManager


def set_cache_dir(path: str):
    """
    Set global options for the package

    Args:
        path: path to the cache dir
    """
    _CacheManager._set_cache_dir(path)
