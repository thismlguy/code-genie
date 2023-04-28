from tempfile import NamedTemporaryFile
from typing import Any, Dict


class _Config:

    # set default values
    cache_code: bool = True
    cache_path: str = NamedTemporaryFile().name

    @classmethod
    def _all_options(cls):
        return [x for x in dir(cls) if not x.startswith("__")]

    @classmethod
    def _set_option(cls, option: str, value: Any):
        # if attribute not present, raise error
        if not hasattr(cls, option):
            raise AttributeError(f"No option found: {option}; allowed options: {cls._all_options()}")
        setattr(cls, option, value)

    @classmethod
    def _set_options(cls, options: Dict[str, Any]):
        # if attribute not present, raise error
        for option, value in options.items():
            cls._set_option(option, value)


def set_options(options: Dict[str, Any]):
    """
    Set global options for the package

    Args:
        options: dictionary containing (name, value) of the options to set. allowed keys: ['cache_code', 'cache_path']
    """
    _Config._set_options(options)
