import json
import logging
import os
from hashlib import blake2b
from tempfile import mkdtemp
from typing import Dict, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


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
    DEFAULT_CACHE_DIR = mkdtemp()

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir, self.meta_path = self._check_cache_dir(cache_dir or self.DEFAULT_CACHE_DIR)
        self._cache_meta = self._load_meta()
        if len(self._cache_meta) > 0:
            logger.info(f"Loaded {len(self._cache_meta)} items from cache file {self.cache_dir}")

    @classmethod
    def _set_cache_dir(cls, cache_dir: str):
        cls.DEFAULT_CACHE_DIR = cache_dir

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

    def _load_meta(self) -> Dict[str, _MetaValue]:
        if not os.path.exists(self.meta_path):
            return {}
        with open(self.meta_path, "r") as f:
            meta_data: Dict[str, _MetaValue] = json.load(f, object_hook=self._json_decoder(_MetaValue))
        return meta_data

    def _load_code(self, filename: str) -> str:
        with open(os.path.join(self.cache_dir, filename), "r") as f:
            return f.read()

    @classmethod
    def _consistent_hash(cls, value: str) -> str:
        h = blake2b()
        h.update(bytes(value, "utf-8"))
        return h.hexdigest()

    def update(self, key: str, value: _CacheValue):
        key_hash = self._consistent_hash(key)
        self._cache_meta[key_hash] = value
        # write to code file
        with open(os.path.join(self.cache_dir, value.filename), "w") as f:
            f.write(value.code)
        # update metadata
        with open(self.meta_path, "w") as f:
            json.dump(self._cache_meta, f, indent=4, default=self._json_encoder)

    def get(self, key: str) -> Optional[_CacheValue]:
        meta = self._cache_meta.get(self._consistent_hash(key), None)
        if meta is not None:
            code = self._load_code(meta.filename)
            return _CacheValue(code=code, filename=meta.filename, fn_name=meta.fn_name)
        return None

    def num_items(self):
        return len(self._cache_meta)
