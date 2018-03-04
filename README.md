# Toapi

Every web site provides APIs.

[![Build](https://travis-ci.org/gaojiuli/toapi.svg?branch=master)](https://travis-ci.org/gaojiuli/toapi)
[![Python](https://img.shields.io/pypi/pyversions/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![Version](https://img.shields.io/pypi/v/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![License](https://img.shields.io/pypi/l/toapi.svg)](https://pypi.python.org/pypi/toapi/)


![Toapi](logo.png)

## Overview

Toapi v2.0.0.

Completely rewrote. 

More beautiful.

- v1.0.0 Documentation: [http://www.toapi.org](http://www.toapi.org)
- Awesome: [https://github.com/toapi/awesome-toapi](https://github.com/toapi/awesome-toapi)
- Organization: [https://github.com/toapi](https://github.com/toapi)


## Get Started

### Installation

```text
$ pip install toapi
$ toapi -v
toapi, version 2.0.0
```

### Usage

```python
from htmlparsing import Attr, Text

from toapi import Api, Item

api = Api()


@api.site('https://news.ycombinator.com/')
@api.list('.athing')
@api.route('/posts?page={page}', '/news?p={page}')
@api.route('/posts', '/news?p=1')
class Post(Item):
    url = Attr('.storylink', 'href')
    title = Text('.storylink')


@api.site('https://news.ycombinator.com/')
@api.route('/posts?page={page}', '/news?p={page}')
@api.route('/posts', '/news?p=1')
class Page(Item):
    next_page = Attr('.morelink', 'href')


api.run(debug=True, host='0.0.0.0', port=5000)
```


