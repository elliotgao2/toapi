import os

from toapi.cache import MemoryCache


class Settings:
    """Global Settings"""
    cache_dict = {
        'cache_class': MemoryCache,
        'cache_config': {},
        'serializer': None,
        'ttl': None
    }
    storage_config = {
        "PATH": os.getcwd(),
        "DB_URL": None
    }
    web_config = {
        "with_ajax": False,
        "request_config": {},
        "headers": None
    }
