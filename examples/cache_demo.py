#!/usr/bin/env python
"""
Tips for toapi caches: there are several simple caching scheme we provide for you, and you can use the following ways.
    - Use RedisCache class directly
    - Use cached decorator
"""
from toapi.settings import Settings
from toapi.cache import RedisCache, MemoryCache, cached


class MySettings(Settings):
    """
    Create custom configuration
    """
    cache = {
        'cache_class': MemoryCache,
        'cache_config': {}
    }
    redis_cache = {
        'cache_class': RedisCache,
        'cache_config': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'password': None
        }
    }


@cached(**MySettings.redis_cache, ttl=5)
def parse(url, params=None, **kwargs):
    return 'value'


if __name__ == '__main__':
    url = '/toapi'
    result = parse(url=url, dynamic_key=url)
    print(result)
