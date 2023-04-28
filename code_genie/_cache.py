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

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._cache = self._load()
        logger.info(f"Loaded {len(self._cache)} items from cache")

    def _load(self) -> Dict[int, Dict[str, str]]:
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, "r") as f:
            return json.load(f)

    def update(self, key: _CacheKey, value: _CacheValue):
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
