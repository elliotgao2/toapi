#!/usr/bin/env python
from toapi.cache.memory_cache import MemoryCache


class CacheSetting:
    """
    Cache setting configuration
    cache_config provides the basic configuration of the cache
        - cache_class: such as MemoryCache RedisCache etc.
        - cache_config: your basic configuration, just like redis's host port db password etc.
        - serializer: such as JsonSerializer PickleSerializer.
    """
    cache_config = {
        'cache_class': MemoryCache,
        'cache_config': {},
        'serializer': None
    }
