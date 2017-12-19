Api is the whole program entrance which connects items, cache, storage, 
handles the request from user and fetches html from source sites. For 
example:

```python
from toapi import XPath, Item, Api

api = Api(base_url='https://news.ycombinator.com')


class Post(Item):
    url = XPath('//a[@class="storylink"]/@href')
    title = XPath('//a[@class="storylink"]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'


api.register(Post)
api.serve()
```

## Arguments

### `base_url`

The argument `base_url` is hostname of source web site. `default = None`

### `settings`

The argument `settings` is the global configuration of the whole app. `default = None` means use default settings.

---

## Methods

### .register(self, item)

Register an item so that we could parse it.


### .serve(self, ip='127.0.0.1', port=5000, **options)

Start to serve.


### .parse(self, path, params=None, **kwargs)

Parse items if the path is defined in registered items.


### .fetch_page_source(self, url, item, params=None, **kwargs)

Fetch html from an url.


### .get_browser(self, settings, item_with_ajax=False)

Init a PhantomJS instance to the Api instance.

### .update_status(self, key)

Update status of Api instance.

### .get_status(self, key)

Get status of Api instance.

### .set_cache(self, key, value)

Set cache. In Api instance, the value usually in type of `dict`.

### .get_cache(self, key)

Get cache.

### .set_storage(self, key, value)

Set storage.In Api instance, the value is usually a HTML.

### .get_storage(self, key)

Get storage.

### .parse_item(self,  html, item)

Parse items from HTML.


