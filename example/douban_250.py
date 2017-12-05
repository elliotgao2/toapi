#!/usr/bin/env python
from pprint import pprint

from toapi import Css, Item, Api

api = Api('https://movie.douban.com/top250')


class Post(Item):
    url = Css('div.hd>a', attr='href')
    title = Css('span.title')

    class Meta:
        source = Css('div.item', attr='target')
        route = '/'


api.register(Post)

if __name__ == '__main__':
    headers = {
        'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"
    }
    pprint(api.parse('/', headers=headers))
    api.serve()
