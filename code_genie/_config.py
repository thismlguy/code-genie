

class _Config:

    # set default values
    cache_code: bool = True

    @classmethod
    def _all_options(cls):
        return [x for x in dir(cls) if not x.startswith("__")]

    @classmethod
    def set_options(cls, option, value):
        # if attribute not present, raise error
        if not hasattr(cls, option):
            raise AttributeError(f"No option found: {option}; allowed options: {cls._all_options()}")
        setattr(cls, option, value)


def set_options(option, value):
    """
    Set global options for the package

    Args:
        option: name of the option to set. allowed values: ['cache_code']
        value: value of the option
    """
    _Config.set_options(option, value)
