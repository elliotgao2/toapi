import os

from toapi.cache import MemoryCache


class Settings:
    """Global Settings"""
    cache = {
        'cache_class': MemoryCache,
        'cache_config': {},
        'serializer': None,
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
