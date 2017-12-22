#!/usr/bin/env python
"""
Tips for toapi caches: there are several simple caching schemes we provide for you, and you can use the following ways.
    - Use RedisCache class directly
    - Use cached decorator
"""
from toapi.settings import Settings
from toapi.cache import RedisCache, cached, CacheSetting, MemoryCache


class MySettings(Settings):
    """
    Create custom configuration
    """
    cache = {
        'cache_class': RedisCache,
        'cache_config': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'password': None
        },
        'serializer': None
    }


@cached(**MySettings.cache, ttl=10)
def parse(url, params=None, **kwargs):
    return 'value'


if __name__ == '__main__':
    url = '/toapi'
    result = parse(url=url, dynamic_key=url)
    cache_ins = CacheSetting(MySettings)
    print(cache_ins.get(url))
