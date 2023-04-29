import json
import logging
import os
from typing import Dict, Tuple, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class _CacheKey(BaseModel):
    key: str
    instructions: str
    inputs: Tuple[Tuple[str, str], ...]
    allowed_imports: Tuple[str, ...]

    class Config:
        frozen = True


class _CacheValue(BaseModel):
    code: str
    fn_name: str

    class Config:
        frozen = True


class _CacheManager:

    DEFAULT_NAME = "_genie_cache.json"

    def __init__(self, filepath: str):
        self.filepath = self._get_filename(filepath)
        self._cache = self._load()
        if len(self._cache) > 0:
            logger.info(f"Loaded {len(self._cache)} items from cache file {self.filepath}")

    @classmethod
    def reload(cls, filepath: str):
        return cls(filepath)

    def _get_filename(self, name: Optional[str] = None):
        # if this is directory, append default name
        if os.path.isdir(name):
            return os.path.join(name, self.DEFAULT_NAME)
        return name

    def _load(self) -> Dict[int, Dict[str, str]]:
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, "r") as f:
            return json.load(f)

    def update(self, key: str, value: _CacheValue):
        self._cache[key.__hash__()] = value.dict()
        with open(self.filepath, "w") as f:
            json.dump(self._cache, f, indent=4)

    def get(self, key: _CacheKey) -> Optional[_CacheValue]:
        value = self._cache.get(key.__hash__(), None)
        if value is not None:
            return _CacheValue.parse_obj(value)
        return None

    def num_items(self):
        return len(self._cache)
