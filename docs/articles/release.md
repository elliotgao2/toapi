## Toapi released! You will never lack of data sources!

#### Brief Introduction

Toapi is a framework for converting a website to an api service.

Whenever I want to start an app or website, I always have a problem with no data sources.
No APi, no database. But I often found the data I need on the website. I need the data.

So I write [Toapi](https://github.com/gaojiuli/toapi) for converting website to api service.
The [Toapi](https://github.com/gaojiuli/toapi) could help me fetch any data I want.

- Project: [https://github.com/gaojiuli/toapi](https://github.com/gaojiuli/toapi)
- Organization (welcome to join us): [https://github.com/toapi](https://github.com/toapi)
- Document: [http://www.toapi.org/](http://www.toapi.org/)

What the result looks like?

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

#### How

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

As you can see. The only thing you should to is writing very little code that is necessary.
Then you finish the APIs of [hackernews](https://news.ycombinator.com).

There are some templates:

- [toapi-search](https://github.com/toapi/toapi-search): Baidu, Bing, Google, Sogou aggregation API
- [toapi-one](https://github.com/toapi/toapi-one) API service of One app <http://wufazhuce.com/>
- [toapi-ebooks](https://github.com/toapi/toapi-ebooks): API service of IT e-book source
- [toapi-instagram](https://github.com/toapi/toapi-instagram): API service of Instagram <https://www.instagram.com/>
- [toapi-pic](https://github.com/toapi/toapi-pic): API service of HD photos website
- etc.

### What else

Toapi development team([@gaojiuli](https://github.com/gaojiuli/), [@howie6879](https://github.com/howie6879/), [@wuqiangroy](https://github.com/wuqiangroy/))