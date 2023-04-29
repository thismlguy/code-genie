from code_genie import set_options


def test_set_options_cache_code(default_config):
    assert default_config.cache_code
    set_options({"cache_code": False})
    assert not default_config.cache_code


def test_set_options_cache_path(default_config, cache_dir):
    assert default_config.cache_dir == default_config.cache_dir

    set_options({"cache_dir": cache_dir})
    assert default_config.cache_dir == cache_dir
