#!/usr/bin/env python
import redis

from toapi.cache.base_cache import BaseCache
from toapi.cache.decorator import dec_connector
from toapi.cache.serializer import PickleSerializer


class RedisCache(BaseCache):
    _db = {}
    _cache_conn = None

    def __init__(self, host="127.0.0.1", port=6379, db=0, password=None, decode_responses=True,
                 serializer=None, **kwargs):
        if serializer is None:
            serializer = PickleSerializer
        super().__init__(serializer=serializer, **kwargs)
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses

    @dec_connector
    def set(self, key, value, ttl=None, **kwargs):
        result = self._cache_conn.set(key, self.serializer.dumps(value), ex=ttl)
        return result

    @dec_connector
    def get(self, key, default=None, **kwargs):
        result = self._cache_conn.get(key)
        return self.serializer.loads(result) if result is not None else default

    @dec_connector
    def delete(self, *keys, **kwargs):
        result = self._cache_conn.delete(*keys)
        return result

    @dec_connector
    def exists(self, key, **kwargs):
        result = self._cache_conn.exists(key)
        return result

    @dec_connector
    def incr(self, key, **kwargs):
        result = self._cache_conn.incr(key)
        return result

    def _cache_client(self, db=None):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=db, password=self.password,
                                    decode_responses=self.decode_responses)
        return redis.StrictRedis(connection_pool=pool)

    def _connector(self, db=None):
        if db is None:
            db = self.db
        if db not in self._db:
            self._db[db] = self._cache_client(db)
        return self._db[db]
