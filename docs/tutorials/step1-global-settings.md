## Settings

Settings allow you config cache, storage, request. In our toapi-pic project.
You could see the code:

```python
import os

from toapi.cache import MemoryCache
from toapi.settings import Settings

class MySettings(Settings):
    """
    Create custom configuration
    http://www.toapi.org/topics/settings/
    """

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
```

- cache: config what kind of cache you use. Default is memory cache
- storage: config what kind of storage you use. Default is local file storage.
- web: config the request headers and if using ajax. Default without ajax.

You can find more detail describe for theme in [topics](/topics/settings)