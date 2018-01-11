## Focus on the item directory

`pexels.py`:

```python
from toapi import Item, XPath


class Pexels(Item):
    __base_url__ = 'https://www.pexels.com'
    img = XPath('//a//img/@src')

    class Meta:
        source = XPath('//article[@class="photo-item"]')
        route = {'/pic/?q=:key': '/search/:key/'}
```

`pixabay.py`:

```python
from toapi import Item, XPath


class Pixabay(Item):
    __base_url__ = 'https://pixabay.com/'
    img = XPath('//a//img/@src')

    class Meta:
        source = XPath('//div[@class="item"]')
        route = {'/pic/?q=:key': '/zh/photos/?q=:key'}

```

Pretty simple.

1. Define the section you want to parse. (Meta.source)
2. Define the fileds relative to section.
3. Define the map of expose route of our api server and the routes of source website.


## Register

When you defined your items, you have to register theme to app. So that the app
could know how to work.

In the file `app.py`:

```python
from toapi import Api

from items.pexels import Pexels
from items.pixabay import Pixabay
from settings import MySettings

api = Api(settings=MySettings)
api.register(Pixabay)
api.register(Pexels)

if __name__ == '__main__':
    api.serve()
```