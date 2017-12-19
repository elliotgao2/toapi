Global settings.

```python
import os
from toapi import Api, Settings
from toapi.cache import MemoryCache

class MySettings(Settings):
    """
    Create custom configuration
    """
    storage = {
        "PATH": os.getcwd(),
        "DB_URL": None
    }
    cache = {
        # If you want to use other classes, just replace it
        'cache_class': MemoryCache,
        'cache_config': {},
        # Default value is JsonSerializer
        'serializer': None,
        'ttl': None
    }
    web = {
        "with_ajax": True,
        "request_config": {},
        "headers": None
    }

api = Api('https://www.github.com', settings=MySettings)
```

## Attributes

### cache

Config how the app perform [cache](cache). 

### storage

Config how the app perform [storage](storage). 

### web

Config how the app perform request. 



