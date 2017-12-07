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
        'type': MemoryCache,
        'config': {}
    }
    redis_cache = {
        'type': RedisCache,
        'config': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'password': None
        }
    }


@cached(cache_class=MySettings.redis_cache['type'], ttl=5, cache_config=MySettings.redis_cache['config'])
def parse(url, params=None, **kwargs):
    return 'value'


if __name__ == '__main__':
    url = '/toapi'
    result = parse(url=url, dynamic_key=url)
    print(result)
