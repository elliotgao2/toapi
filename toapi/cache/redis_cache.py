#!/usr/bin/env python
import redis

from toapi.cache.serializer import JsonSerializer
from toapi.cache.base_cache import BaseCache
from toapi.cache.decorator import dec_connector


class RedisCache(BaseCache):
    _db = {}

    def __init__(self, host="127.0.0.1", port=6379, db=0, password=None, decode_responses=True,
                 serializer=JsonSerializer, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.serializer = serializer

    @dec_connector
    def set(self, key, value, ttl=None, connector=None):
        result = connector.set(key, value, ex=ttl)
        return result

    @dec_connector
    def get(self, key, default=None, connector=None):
        result = connector.get(key)
        return result or default

    @dec_connector
    def exists(self, key, connector=None):
        result = connector.exists(key)
        return result

    def _cache_client(self, db=None):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password,
                                    decode_responses=self.decode_responses)
        return redis.StrictRedis(connection_pool=pool)

    def _connector(self, db=None):
        if db is None:
            db = self.db
        if db not in self._db:
            self._db[db] = self._cache_client(db)
        return self._db[self.db]
