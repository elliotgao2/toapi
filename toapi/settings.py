from toapi.cache import MemoryCache


class Settings:
    """Global Settings"""
    cache_config = {
        'cache_class': MemoryCache,
        'cache_config': {},
        'serializer': None
    }
    with_ajax = False
