# Toapi

Every web site provides APIs.

[![Build](https://travis-ci.org/gaojiuli/toapi.svg?branch=master)](https://travis-ci.org/gaojiuli/toapi)
[![Python](https://img.shields.io/pypi/pyversions/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![Version](https://img.shields.io/pypi/v/toapi.svg)](https://pypi.python.org/pypi/toapi/)
[![License](https://img.shields.io/pypi/l/toapi.svg)](https://pypi.python.org/pypi/toapi/)


![Toapi](logo.png)

## Overview

Toapi v2.0.0. New usage, more simple.

- Documentation: [http://www.toapi.org](http://www.toapi.org)
- Awesome: [https://github.com/toapi/awesome-toapi](https://github.com/toapi/awesome-toapi)
- Organization: [https://github.com/toapi](https://github.com/toapi)


## Get Started

### Installation

```text
$ pip install toapi
$ toapi -v
toapi, version 0.1.12
```

### Usage

```python
from htmlparsing import Attr, Text

from toapi import Api, Item

api = Api('https://news.ycombinator.com/')


@api.list('tr.athing')
@api.route(['/post?p={page}', '/news?p={page}'])
class Post(Item):
    url = Attr('.storylink', 'href')
    title = Text('storylink')


@api.route(['/post?p={page}', '/news?p={page}'])
class Page(Item):
    next_page = Attr('.morelink', 'href')


api.app.run(debug=True, host='0.0.0.0', port=5000)
```


