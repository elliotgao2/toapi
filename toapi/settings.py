import os
from toapi.cache import MemoryCache


class Settings:
    """Global Settings"""
    cache_config = {
        'cache_class': MemoryCache,
        'cache_config': {},
        'serializer': None
    }
    storage_config = {
        "PATH": os.getcwd(),
        "DB_URL": None
    }
    with_ajax = False
