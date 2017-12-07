#!/usr/bin/env python
from toapi.cache.serializer import JsonSerializer
from toapi.cache.base_cache import BaseCache


class MemoryCache(BaseCache):
    _cache = {}

    def __init__(self, serializer=None, **kwargs):
        if serializer is None:
            serializer = JsonSerializer
        super().__init__(serializer=serializer, **kwargs)

    def set(self, key, value, ttl=None):
        self._cache[key] = self.serializer.dumps(value)
        if ttl:
            # TODO
            pass
        return True

    def get(self, key, default=None):
        result = self._cache.get(key)
        return self.serializer.loads(result) or default

    def delete(self, *keys):
        res = []
        for key in keys:
            res.append(self._delete(key))
        return res

    def exists(self, key):
        return key in self._cache

    def _delete(self, key):
        return self._cache.pop(key, 0)
