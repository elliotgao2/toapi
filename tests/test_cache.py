#!/usr/bin/env python
from toapi.cache import MemoryCache, CacheSetting, JsonSerializer, PickleSerializer, cached
from toapi.settings import Settings


def test_memory_cache():
    memory_cache = MemoryCache()
    memory_cache.set('name', 'toapi')
    cache_ins = CacheSetting()
    assert cache_ins.get('name') == 'toapi'


def test_cached():
    cache_ins = CacheSetting(Settings)

    @cached(**Settings.cache)
    def hello_cache(name, **kwargs):
        return 'hello world'

    name = 'toapi'
    hello_cache(name=name, dynamic_key=name)
    assert cache_ins.get(name) == 'hello world'


def test_serializer():
    test = {
        'name': 'toapi',
        'url': 'https://github.com/gaojiuli/toapi'
    }
    serializer_ins = JsonSerializer()
    pickle_ins = PickleSerializer()
    assert pickle_ins.loads(pickle_ins.dumps(test)) == test
    assert serializer_ins.loads(serializer_ins.dumps(test)) == test
