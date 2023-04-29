__version__ = "0.2.0-dev0"

from typing import Dict, Any

from code_genie._cache import _CacheManager
from code_genie._config import _Config

# initialize global cache
CACHE = _CacheManager(cache_dir=_Config.cache_dir)


def set_options(options: Dict[str, Any]):
    """
    Set global options for the package

    Args:
        options: dictionary containing (name, value) of the options to set. allowed keys: ['cache_code', 'cache_path']
    """
    _Config._set_options(options)

    # if cache path is set, then reload cache
    new_cache_path = options.get("cache_dir")
    if new_cache_path:
        global CACHE
        CACHE = _CacheManager.reload(new_cache_path)
