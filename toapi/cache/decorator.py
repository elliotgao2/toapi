#!/usr/bin/env python
from functools import wraps

from colorama import Fore

from toapi.log import logger


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
            cache_key = key or kwargs.pop('dynamic_key', None)
            if isinstance(cache_config, dict):
                kwargs.update(cache_config)
            cache_ins = cache_class(serializer=serializer, **kwargs)
            try:
                if cache_ins.exists(cache_key):
                    logger.info(Fore.YELLOW, 'Cache', 'Get<%s>' % cache_key)
                    return cache_ins.get(cache_key, **kwargs)
            except Exception:
                logger.exception('Cache', 'Get<%s>' % cache_key)
            result = func(*args, **kwargs)
            if result and cache_key:
                try:
                    if cache_ins.set(cache_key, result, ttl=ttl, **kwargs):
                        logger.info(Fore.YELLOW, 'Cache', 'Set<%s>' % cache_key)
                except Exception:
                    logger.exception('Cache', 'Set<%s>' % cache_key)

            return result

        return wrapper

    return cached_dec
