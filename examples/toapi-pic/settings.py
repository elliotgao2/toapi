import os

from toapi.cache import RedisCache, JsonSerializer
from toapi.settings import Settings


class MySettings(Settings):
    """
    Create custom configuration
    http://www.toapi.org/topics/settings/
    """

    cache = {
        'cache_class': RedisCache,
        'cache_config': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0
        },
        'serializer': JsonSerializer,
        'ttl': 10000
    }
    storage = {
        "PATH": os.getcwd(),
        "DB_URL": 'sqlite:///data.sqlite'
    }
    web = {
        "with_ajax": False,
        "request_config": {},
        "headers": None
    }
