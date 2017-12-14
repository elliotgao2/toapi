#!/usr/bin/env python
import abc


class BaseCache(metaclass=abc.ABCMeta):
    """
    The class defines some functions that is necessary provided by RedisCache MemoryCache MemcachedCache
    """

    def __init__(self, serializer, namespace=None, **kwargs):
        self.namespace = namespace
        self.serializer = serializer()

    @abc.abstractmethod
    def set(self, key, value, ttl=None, **kwargs):
        """
        Set the value at key ``key`` to ``value``
        """
        pass

    @abc.abstractmethod
    def get(self, key, default=None, **kwargs):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        pass

    @abc.abstractmethod
    def delete(self, *keys, **kwargs):
        """
        Delete one or more keys specified by ``keys``
        """
        pass

    @abc.abstractmethod
    def exists(self, key, **kwargs):
        """
        Returns a boolean indicating whether key ``name`` exists
        """
        pass

    @abc.abstractmethod
    def incr(self, key, **kwargs):
        """
        Increments the value of ``key``.
        """
        pass


class BaseSerializer(metaclass=abc.ABCMeta):
    """
    The class defines some functions that is necessary provided by JsonSerializer PickleSerializer
    """

    @abc.abstractmethod
    def dumps(self, value, **kwargs):
        pass

    @abc.abstractmethod
    def loads(self, value, **kwargs):
        pass
