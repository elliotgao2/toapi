#!/usr/bin/env python
from toapi.cache.memory_cache import MemoryCache


class CacheSetting:
    cache_config = {
        'cache_class': MemoryCache,
        'cache_config': {}
    }
