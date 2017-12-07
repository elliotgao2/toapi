#!/usr/bin/env python
from toapi.cache import MemoryCache


def test_memory_cache():
    memory_cache = MemoryCache()
    memory_cache.set('name', 'toapi')
    assert memory_cache.get('name') == 'toapi'
