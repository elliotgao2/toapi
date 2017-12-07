from toapi.cache import MemoryCache


class Settings:
    """Global Settings"""
    cache_config = {
        'cache_class': MemoryCache,
        'cache_config': {}
    }
    with_ajax = False
