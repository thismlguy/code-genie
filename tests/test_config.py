from unittest import TestCase

from code_genie._config import _Config


class Test(TestCase):

    def test_set_options(self):
        config = _Config
        self.assertTrue(config.cache_code)
        config.set_options("cache_code", False)
        self.assertFalse(config.cache_code)
