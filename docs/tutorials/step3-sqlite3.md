## Prepare Sqlite3

```text
$ sqlite3 --version                     
3.11.0 2016-02-15 17:29:24 3d862f207e3adc00f78066799ac5a8c282430a5f
```

If you don't have sqlite3, you need to install it.

## Setting

Edit the `settings.py`, change it to:

```python
import os

from toapi.cache import RedisCache
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

```

Try to run command `toapi run`. If it works, you do good job. 
In the root directory there should be a `data.sqlite` file.
If something wrong, please check the sqlite3 and the sqlite3 library for python.