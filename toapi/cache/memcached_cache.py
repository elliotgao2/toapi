#!/usr/bin/env python
from pymemcache.client.base import Client

from toapi.cache.base_cache import BaseCache
from toapi.cache.decorator import dec_connector
from toapi.cache.serializer import PickleSerializer


class MemcachedCache(BaseCache):
    _cache_conn = None

    def __init__(self, host="127.0.0.1", port=11211, connect_timeout=20, timeout=15, serializer=None,
                 **kwargs):
        if serializer is None:
            serializer = PickleSerializer
        super().__init__(serializer=serializer, **kwargs)
        self.host = host
        self.port = port
        self.connect_timeout = connect_timeout
        self.timeout = timeout
        self.kwargs = kwargs

    @dec_connector
    def set(self, key, value, ttl=None, **kwargs):
        ttl = ttl or 0
        result = self._cache_conn.set(key, self.serializer.dumps(value), expire=ttl)
        return result

    @dec_connector
    def get(self, key, default=None, **kwargs):
        result = self._cache_conn.get(key)
        if result and not isinstance(self.serializer, PickleSerializer):
            if isinstance(result, bytes):
                result = bytes.decode(result)
        return self.serializer.loads(result) if result is not None else default

    @dec_connector
    def delete(self, key, **kwargs):
        result = self._cache_conn.delete(key)
        return result

    @dec_connector
    def exists(self, key, **kwargs):
        result = self._cache_conn.get(key)
        return result is not None

    @dec_connector
    def incr(self, key, value=1, **kwargs):
        if not self.exists(key):
            result = value
            self.set(key, result)
        else:
            result = self._cache_conn.incr(key, value=value)
        return result

    def _cache_client(self):
        client = Client((self.host, self.port), self.kwargs)
        return client

    def _connector(self):
        return self._cache_client()
