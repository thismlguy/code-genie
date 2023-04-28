from unittest import TestCase

from code_genie._config import _Config, set_options


class Test(TestCase):

    def setUp(self) -> None:
        self.config = _Config

    def test_set_options_cache_code(self):
        self.assertTrue(self.config.cache_code)
        set_options({"cache_code": False})
        self.assertFalse(self.config.cache_code)

    def test_set_options_cache_path(self):
        config = _Config
        self.assertEqual(self.config.cache_path, config.cache_path)

        set_options({"cache_path": "tests"})
        self.assertEqual(self.config.cache_path, "tests")
