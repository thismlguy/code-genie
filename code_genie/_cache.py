import json
import logging
import os
from hashlib import blake2b
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


class _MetaValue(BaseModel):
    filename: str
    fn_name: str

    class Config:
        frozen = True

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class _CacheValue(_MetaValue):
    code: str


class _CacheManager:

    DEFAULT_NAME = "_genie_cache.json"
    META_NAME = "_meta.json"

    def __init__(self, cache_dir: str):
        self.cache_dir, self.meta_path = self._check_cache_dir(cache_dir)
        self._cache = self._load()
        if len(self._cache) > 0:
            logger.info(f"Loaded {len(self._cache)} items from cache file {self.cache_dir}")

    @classmethod
    def reload(cls, filepath: str):
        return cls(filepath)

    def _check_cache_dir(self, name: str):
        # if dir doesn't exist, create it
        if not os.path.exists(name):
            os.makedirs(name)
        return name, os.path.join(name, self.META_NAME)

    @staticmethod
    def _json_decoder(schema):
        def decoder(obj):
            try:
                return schema.parse_obj(obj)
            except:
                return obj
        return decoder

    @staticmethod
    def _json_encoder(obj):
        try:
            return obj.dict()
        except:
            return obj

    def _load(self) -> Dict[str, _CacheValue]:
        if not os.path.exists(self.meta_path):
            return {}
        with open(self.meta_path, "r") as f:
            meta_data: Dict[str, _MetaValue] = json.load(f, object_hook=self._json_decoder(_MetaValue))
        # read all files in meta and create cache values
        cache = {}
        for key, item in meta_data.items():
            with open(os.path.join(self.cache_dir, item.filename), "r") as f:
                code = f.read()
            cache[self._consistent_hash(key)] = _CacheValue(code=code, **item.dict())
        return cache

    @classmethod
    def _consistent_hash(cls, value: str) -> str:
        h = blake2b()
        h.update(bytes(value, 'utf-8'))
        return h.hexdigest()

    @property
    def _cache_meta(self):
        return {key: _MetaValue(filename=value.filename, fn_name=value.fn_name) for key, value in self._cache.items()}

    def update(self, key: str, value: _CacheValue):
        key_hash = self._consistent_hash(key)
        self._cache[key_hash] = value
        # write to code file
        with open(os.path.join(self.cache_dir, value.filename), "w") as f:
            f.write(value.code)
        # update metadata
        with open(self.meta_path, "w") as f:
            json.dump(self._cache_meta, f, indent=4, default=self._json_encoder)

    def get(self, key: str) -> Optional[_CacheValue]:
        return self._cache.get(self._consistent_hash(key), None)

    def num_items(self):
        return len(self._cache)
