#!/usr/bin/env python
from functools import wraps

from colorama import Fore
from urllib.parse import urlparse

from flask import jsonify

from toapi.cache.memory_cache import MemoryCache
from toapi.log import logger


class CacheSetting:
    """
    Cache setting configuration
    cache_dict provides the basic configuration of the cache
        - cache_class: such as MemoryCache RedisCache etc.
        - cache_config: your basic configuration, just like redis's host port db password etc.
        - serializer: such as JsonSerializer PickleSerializer.
    """
    cache_dict = {
        'cache_class': MemoryCache,
        'cache_config': {},
        'serializer': None
    }

    def __init__(self, settings=None):
        self.cache = getattr(settings, 'cache', self.cache_dict)
        if not isinstance(self.cache.get('cache_config'), dict):
            raise ValueError("Key cache_config must be a dict")
        serializer = self.cache.get('serializer')
        self.ttl = self.cache.get('ttl')
        self.instance = self.cache['cache_class'](serializer=serializer, **self.cache['cache_config'])

    def set(self, key, value, ttl=None, **kwargs):
        ttl = ttl or self.ttl
        return self.instance.set(key, value, ttl=ttl, **kwargs)

    def get(self, key, default=None, **kwargs):
        return self.instance.get(key, default=default, **kwargs)

    def exists(self, key, **kwargs):
        return self.instance.exists(key, **kwargs)

    def incr(self, key, **kwargs):
        return self.instance.incr(key, **kwargs)

    def api_cached(self, ttl=None, **kwargs):
        """
        This decorator provides a caching mechanism for the data
        :param cache_class: such as RedisCache MemcachedCache MemoryCache
        :param ttl: int seconds to store the data
        :param serializer: serialize the value
        :param kwargs:
        :return:
        """

        def cached_dec(func):
            @wraps(func)
            def wrapper(error=None, ttl=ttl, *args, **kwargs):
                if error:
                    from flask import request
                    parse_result = urlparse(request.url)
                    if parse_result.query != '':
                        key = '{}?{}'.format(
                            parse_result.path,
                            parse_result.query
                        )
                    else:
                        key = request.path
                else:
                    # TODO
                    key = None
                cache_key = key
                ttl = ttl or self.ttl
                try:
                    if self.exists(cache_key):
                        logger.info(Fore.YELLOW, 'Cache', 'Get<%s>' % cache_key)
                        return jsonify(self.get(cache_key, **kwargs))
                except Exception:
                    logger.exception('Cache', 'Get<%s>' % cache_key)
                result = func(error, url=key, *args, **kwargs)
                if result and cache_key:
                    try:
                        if self.set(cache_key, result, ttl=ttl, **kwargs):
                            logger.info(Fore.YELLOW, 'Cache', 'Set<%s>' % cache_key)
                    except Exception:
                        logger.exception('Cache', 'Set<%s>' % cache_key)

                return jsonify(result)

            return wrapper

        return cached_dec
