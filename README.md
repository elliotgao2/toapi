# Toapi

[![Build](https://travis-ci.org/gaojiuli/toapi.svg?branch=master)](https://travis-ci.org/gaojiuli/toapi)
[![Python](https://img.shields.io/pypi/pyversions/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![Version](https://img.shields.io/pypi/v/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![License](https://img.shields.io/pypi/l/toapi.svg)](https://pypi.python.org/pypi/toapi/)

A library letting any web site provide APIs.
In the past, we crawl data and storage them and create api service to share them maybe we should also update them regularly.
This library make things easy.
The only thing you should do is defining your data, they would be shared as api service automatically.

## Diagram

![Toapi](diagram.png)

## Installation

- `pip install toapi`
- `pip install git+https://github.com/gaojiuli/toapi/`

## Usage

### Static site:

```python
from toapi import XPath, Item, Api

api = Api('https://news.ycombinator.com/')


class Post(Item):
    url = XPath('//a[@class="storylink"][1]/@href')
    title = XPath('//a[@class="storylink"][1]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'


api.register(Post)

api.serve()

# Visit http://127.0.0.1:5000/
```

- Item.Meta.route: A regex statement. Define the path of your api service. Which means when the request path match the route regex statement, the Item would be parsed. Most of the time, the route is the same as ths path of source site.
- Item.Meta.source: The section part of html that contains a single item.
- api.serve(): Run a server, provide api service.
- api.parse(): Parse a path. If the path is not defined in Item.Meta.route, this method returns nothing.

### Site with ajax:

- `Phantomjs` is required. Run `phantomjs -v` to check.
- If you use Ubuntu. Run `sudo apt install phantomjs` to install.
- If you use MacOS. Run `brew install phantomjs` to install.

```python
from toapi import XPath, Item, Api, Settings


class MySettings(Settings):
    web = {
        "with_ajax": False
    }


api = Api('https://news.ycombinator.com/', settings=MySettings)


class Post(Item):
    url = XPath('//a[@class="storylink"]/@href')
    title = XPath('//a[@class="storylink"]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/news\?p=\d+'


class Page(Item):
    next_page = XPath('//a[@class="morelink"]/@href')

    class Meta:
        source = None
        route = '/news\?p=\d+'

    def clean_next_page(self, next_page):
        return "http://127.0.0.1:5000/" + next_page


api.register(Post)
api.register(Page)

api.serve(ip='127.0.0.1',port=5000)

# Visit http://127.0.0.1:5000/news?p=1
```

## Contribution

- Open Issue.
- Pull Request.

## License

Apache-2.0
