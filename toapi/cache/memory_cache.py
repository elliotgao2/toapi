#!/usr/bin/env python
from toapi.cache.serializer import JsonSerializer
from toapi.cache.base_cache import BaseCache


class MemoryCache(BaseCache):
    _cache = {}

    def __init__(self, serializer=JsonSerializer, **kwargs):
        super().__init__(serializer=serializer, **kwargs)

    def set(self, key, value, ttl=None):
        self._cache[key] = value
        if ttl:
            # TODO
            pass
        return True

    def get(self, key, default=None):
        result = self._cache.get(key, default)
        return result

    def delete(self, *keys):
        res = []
        for key in keys:
            res.append(self._delete(key))
        return res

    def exists(self, key):
        return key in self._cache

    def _delete(self, key):
        print(key)
        return self._cache.pop(key, 0)
