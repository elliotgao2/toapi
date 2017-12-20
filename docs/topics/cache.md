When you are writing a service, maybe you need to be able to save a piece of JSON data to your system's memory.

There are three ways to create a cache, which are MemoryCache, RedisCache or MemcachedCache.

What is the difference between these three ways?

- [MemoryCache](https://github.com/gaojiuli/toapi/blob/master/toapi/cache/memory_cache.py): easy to configure, but it automatically destroys when the server is stopped.
- [RedisCache](https://github.com/gaojiuli/toapi/blob/master/toapi/cache/redis_cache.py): stable but you have to install Redis.
- [MemcachedCache](https://github.com/gaojiuli/toapi/blob/master/toapi/cache/memcached_cache.py): stable but you have to install Memcached.

There are two serialization schemes we provide for you:

- [JsonSerializer](https://github.com/gaojiuli/toapi/blob/master/toapi/cache/serializer.py)
- [PickleSerializer](https://github.com/gaojiuli/toapi/blob/master/toapi/cache/serializer.py)

## Core arguments

`RedisCache` and `MemcachedCache` class constructor must takes these arguments. Some Field classes take additional, field-specific arguments, but the following should always be accepted:

- host
- port

!!! Note
    `MemoryCache` can be instantiated directly

## Methods

### .set(self, key, value, ttl=None, **kwargs)
Set the value at key ``key`` to ``value``

### .get(self, key, default=None, **kwargs)
Return the value at key ``name``, or None if the key doesn't exist

### .delete(self, key, **kwargs)
Delete one or more keys specified by ``keys``

### .exists(self, key, **kwargs)
Returns a boolean indicating whether key ``name`` exists

### .incr(self, key, **kwargs)
Increments the value of ``key``

### .api_cached(self, ttl=None, **kwargs)
This decorator provides a caching mechanism for the data

- param cache_class: such as RedisCache MemcachedCache MemoryCache
- param ttl: int seconds to store the data
- param serializer: serialize the value

## Usage

These methods can be used with very convenient, first of all, you just need to add one new class which inheritance the [`Toapi.Settings`](https://github.com/gaojiuli/toapi/blob/master/toapi/settings.py).

Let's take a look at a quick example of using MemoryCache.Start off by adding the following to your `settings.py`:

``` python
from toapi.cache import MemoryCache, RedisCache


class MyMemorySettings(Settings):
    """
    Create custom configuration
    """
    cache = {
        # If you want to use other classes, just replace it
        'cache_class': MemoryCache,
        'cache_config': {},
        # Default value is JsonSerializer
        'serializer': None,
        'ttl': None
    }

class MyRedisSettings(Settings):
    """
    If you want to use Redis, you can create your configuration like this
    """
    cache = {
        # If you want to use other classes, just replace it
        'cache_class': RedisCache,
        'cache_config': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'password': None
        },
        'serializer': None,
        'ttl': None
    }

```

Next create `cache_demo.py`:

``` python
from toapi.cache import cached, CacheSetting

from settings import MyMemorySettings

# Create a cache instance
# Or cache_ins = CacheSetting(MyRedisSettings)
cache_ins = CacheSetting(MyMemorySettings)

# Set the value at key, the key will be automatically deleted after 10s
cache_ins.set(key='name', value='toapi', ttl=10)

# Return the value at key ``name``,
value = cache_ins.get(key='name')

# Output
# toapi
```

Once a cache instance has been created, you can use it anywhere to implement data caching.

Now you know some of the basic operations for using cache_ins, but how can you add a cache to your API service?

Add the following to your `app.py`:

``` python

from toapi import Api

from settings import MyMemorySettings

api = Api('https://www.github.com', settings=MyMemorySettings)

```

## How It Works?

The [`Api`](https://github.com/gaojiuli/toapi/blob/master/toapi/api.py) class will initialize the `cache` attribute based on the value of settings.

!!! Note
    Api class can accept a parameter named settings, if settings is None, the default configuration will take effect
    
    You can read the basic configuration from [`toapi/settings.py`](https://github.com/gaojiuli/toapi/blob/master/toapi/settings.py)