#!/usr/bin/env python
"""
Tips for toapi caches: we provide you with simple caching scheme, and you can use it as following.
"""
from toapi.settings import Settings
from toapi.cache import RedisCache, MemoryCache, cached


class MySettings(Settings):
    """

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


@cached(cache_class=MySettings.redis_cache['type'], ttl=0, cache_config=MySettings.redis_cache['config'])
def parse(url, params=None, **kwargs):
    return 'value'


if __name__ == '__main__':
    url = '/toapi'
    result = parse(url=url, dynamic_key=url)
    print(result)
