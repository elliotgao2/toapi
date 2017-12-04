# Toapi

[![Build](https://travis-ci.org/gaojiuli/toapi.svg?branch=master)](https://travis-ci.org/gaojiuli/toapi)
[![Python](https://img.shields.io/pypi/pyversions/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![Version](https://img.shields.io/pypi/v/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![License](https://img.shields.io/pypi/l/toapi.svg)](https://pypi.python.org/pypi/toapi/)

Make existing web sites available with APIs. You can have your own APIs of your web.
You can create your owen APIs from other's web. And Then, you can do something interesting with those APIs.

## Feature

- Convert static html to api.
- Easy to use.

## Installaton

- `pip install toapi`
- `pip install git+https://github.com/gaojiuli/toapi/`

## Usage

### Static Site:

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

print(api.parse('/'))

api.serve()
```

### Site with Ajax:

- `Phantomjs` is required. Run `phantomjs -v` to check.
- If you use Ubuntu. Run `sudo apt install phantomjs` to install.
- If you use MacOS. Run `brew install phantomjs` to install.

```python
from toapi import XPath, Item, Api

api = Api('https://news.ycombinator.com/', with_ajax=True) # This meas use selenium to load the page source.

class Post(Item):
    url = XPath('//a[@class="storylink"][1]/@href')
    title = XPath('//a[@class="storylink"][1]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'

api.register(Post)

print(api.parse('/'))

api.serve()
```


Then, You get your api server. Powered by flask.

## Contribute

- Open issue.
- Pull Request.

## License

Apache-2.0