# Toapi

Make existing web sites available with APIs.

## Feature

- Convert static html to api.
- Easy to use.

## Usage

```python
from pprint import pprint

from toapi import XPath, Item, Api

api = Api('https://news.ycombinator.com/')

class Post(Item):
    url = XPath('//a[@class="storylink"][1]/@href')
    title = XPath('//a[@class="storylink"][1]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'

api.register(Post)

pprint(api.parse('/'))

```

## Contribute

Open issue.
Pull Request.

## License

Apache-2.0