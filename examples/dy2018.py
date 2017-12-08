from toapi import XPath, Item, Api

api = Api()


class Movie(Item):
    __base_url__ = 'http://www.dy2018.com'

    url = XPath('//b//a[@class="ulink"]/@href')
    title = XPath('//b//a[@class="ulink"]/text()')

    class Meta:
        source = XPath('//table[@class="tbspan"]')
        route = '/'


class Post(Item):
    __base_url__ = 'https://news.ycombinator.com/'
    url = XPath('//a[@class="storylink"]/@href')
    title = XPath('//a[@class="storylink"]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'


class Page(Item):
    __base_url__ = 'https://news.ycombinator.com/'
    next_page = XPath('//a[@class="morelink"]/@href')

    class Meta:
        source = None
        route = '/'


api.register(Movie)
api.register(Post)
api.register(Page)

api.serve()
