#!/usr/bin/env python
from functools import wraps


def dec_connector(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._cache_conn is None:
            self._cache_conn = self._connector()
            return func(self, *args, **kwargs)

        return func(self, *args, **kwargs)

    return wrapper


def cached(cache_class=None, key=None, ttl=None, serializer=None, cache_config=None, **kwargs):
    """
    This decorator provides a caching mechanism for the data
    :param cache_class: such as RedisCache MemcachedCache MemoryCache
    :param key: key or dynamic_key
    :param ttl: int seconds to store the data
    :param serializer: serialize the value
    :param kwargs:
    :return:
    """

    def cached_dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(cache_config, dict):
                kwargs.update(cache_config)
            cache_ins = cache_class(serializer=serializer, **kwargs)
            dynamic_key = kwargs.get('dynamic_key')
            cache_key = key or dynamic_key
            try:
                if cache_ins.exists(cache_key):
                    return cache_ins.get(cache_key)
            except Exception:
                # TODO
                pass
            result = func(*args, **kwargs)
            if result:
                try:
                    cache_ins.set(cache_key, result, ttl=ttl)
                except Exception as e:
                    # TODO
                    pass

            return result

        return wrapper

    return cached_dec
