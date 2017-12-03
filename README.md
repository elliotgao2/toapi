# Toapi

Make existing web sites available with APIs.
[![Build](https://travis-ci.org/gaojiuli/toapi.svg?branch=master)](https://travis-ci.org/gaojiuli/toapi)
[![Python](https://img.shields.io/pypi/pyversions/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![Version](https://img.shields.io/pypi/v/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![License](https://img.shields.io/pypi/l/toapi.svg)](https://pypi.python.org/pypi/toapi/)

## Feature

- Convert static html to api.
- Easy to use.

## Installaton

`pip install toapi

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