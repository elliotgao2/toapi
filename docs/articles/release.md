## Toapi released! You will never lack of data source!

#### Brief Introduction

Do you have such a demand, have a good idea,
but do not have a good source of data,
it is not easy to find a relevant data sources website,
but found no API (yes but there may be fees),

What it looks like?

```json
// http://127.0.0.1:5000/pic/?q=coffee

{
    "Pixabay": [
        {
            "img": "https://cdn.pixabay.com/photo/2017/06/21/05/28/coffee-2426110__340.png"
        },
        {
            "img": "/static/img/blank.gif"
        }
    ],
    "Pexels": [
        {
            "img": "https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg?h=350&auto=compress&cs=tinysrgb"
        },
        {
            "img": "https://images.pexels.com/photos/34085/pexels-photo.jpg?h=350&auto=compress&cs=tinysrgb"
        }
    ]
}
```


Now I can tell you, [Toapi](https://github.com/gaojiuli/toapi) provides a good solution for this.
It can:

- Short development cycle: a website can be built into your own API service with a small amount of code
- Robust Service Support: You only have to build and use it quickly, and the rest is peace of mind to [Toapi](https://github.com/gaojiuli/toapi)
  - Automatic **data cache**, provides `MemoryCache RedisCache MemcachedCache` three caching solutions
  - Local persistence of source files, providing local and database support
  - Incremental update
  - Custom routing
  - Custom multi-station assembly API
- A variety of template: every [Toapi](https://github.com/gaojiuli/toapi) service can be installed by other users, you do not need to write code, 

you can install other services, and then combined into their own services. 
Official maintenance of a template list - [awesome-toapi] (https://github.com/toapi/awesome-toapi)

[Toapi](https://github.com/gaojiuli/toapi) is an open source project written by `python`, 
you can customize if you hava special functional requirements.
We provide complete ecology for you:

- project website: [https://github.com/gaojiuli/toapi](https://github.com/gaojiuli/toapi)
- project organization (welcome to join us):
[https://github.com/toapi](https://github.com/toapi)
- doc website:
[http://www.toapi.org/](http://www.toapi.org/)

#### Use Toapi

Take a look at a simple example  below - just a demo 
target website is [hackernews](https://news.ycombinator.com)：
``` python
from toapi import XPath, Item, Api, Settings


class MySettings(Settings):
    web = {
        "with_ajax": True,
        "request_config": {},
        "headers": None
    }

api = Api('https://news.ycombinator.com', settings=MySettings)

class Post(Item):
    url = XPath('//a[@class="storylink"]/@href')
    title = XPath('//a[@class="storylink"]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = {'/news?p=:page': '/news?p=:page'}

class Page(Item):
    next_page = XPath('//a[@class="morelink"]/@href')

    class Meta:
        source = None
        route = {'/news?p=:page': '/news?p=:page'}

    def clean_next_page(self, next_page):
        return "http://127.0.0.1:5000/" + next_page

api.register(Page)
api.register(Post)

api.serve()
# Visit http://127.0.0.1:5000/news?p=1
```

Less than forty lines of code,
you have aleady have API service of [hackernews](https://news.ycombinator.com).
Introduce current templates provided by official:

- [toapi-search](https://github.com/toapi/toapi-search): Baidu, Bing, Google, Sogou aggregation API
- [toapi-one](https://github.com/toapi/toapi-one) API of One app <http://wufazhuce.com/>
- [toapi-ebooks](https://github.com/toapi/toapi-ebooks): API of IT e-book source
- [toapi-instagram](https://github.com/toapi/toapi-instagram): API of Instagram <https://www.instagram.com/>
- [toapi-pic](https://github.com/toapi/toapi-pic): API of HD photos website collection
- e.g.

### At last

[Toapi](https://github.com/gaojiuli/toapi) will not stop making progress. 
From the primitive version of the first edition to the fully functional version now, 
we have nearly 400 commits in a month, of which hard work is unnecessary to say.

We sincerely hope developer use [Toapi](https://github.com/gaojiuli/toapi) to build server, 
and feedback your valuable opinion. 

Getting started [Toapi](https://github.com/gaojiuli/toapi) is a trivial matter and we would 
like to see [Toapi](https://github.com/gaojiuli/toapi) make a contribution 
to open source community, for you to reduce the trouble of building an API.

Toapi development team([@gaojiuli](https://github.com/gaojiuli/), [@howie6879](https://github.com/howie6879/), [@wuqiangroy](https://github.com/wuqiangroy/))