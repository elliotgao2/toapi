#!/usr/bin/env python
import abc


class BaseCache(metaclass=abc.ABCMeta):
    """
    The class defines some functions that is necessary provided by RedisCache MemoryCache MemcachedCache
    """

    def __init__(self, namespace=None):
        self.namespace = namespace

    @abc.abstractmethod
    def set(self, key, value, ttl=None):
        pass

    @abc.abstractmethod
    def get(self, key, default=None):
        pass

    @abc.abstractmethod
    def exists(self, key):
        pass


class BaseSerializer(metaclass=abc.ABCMeta):
    """
    The class defines some functions that is necessary provided by JsonSerializer PickleSerializer
    """

    @abc.abstractmethod
    def dumps(self, value):
        pass

    @abc.abstractmethod
    def loads(self, value):
        pass
