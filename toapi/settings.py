import os

from toapi.cache import MemoryCache, StrSerializer


class Settings:
    """Global Settings"""
    cache = {
        'cache_class': MemoryCache,
        'cache_config': {},
        'serializer': StrSerializer,
        'ttl': None
    }
    storage = {
        "PATH": os.getcwd(),
        "DB_URL": None
    }
    web = {
        "with_ajax": False,
        "request_config": {},
        "headers": None
    }
