from toapi import XPath, Item, Api

api = Api('http://www.dy2018.com')


class Movie(Item):
    url = XPath('//b//a[@class="ulink"]/@href')
    title = XPath('//b//a[@class="ulink"]/text()')

    class Meta:
        source = XPath('//table[@class="tbspan"]')
        route = '/html/gndy/dyzz/index_\d+.html'


class Post(Item):
    __base_url__ = 'https://news.ycombinator.com/'
    url = XPath('//a[@class="storylink"]/@href')
    title = XPath('//a[@class="storylink"]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/news\?p=\d+'


class Page(Item):
    __base_url__ = 'https://news.ycombinator.com/'
    next_page = XPath('//a[@class="morelink"]/@href')

    class Meta:
        source = None
        route = '/news\?p=\d+'

    def clean_next_page(self, next_page):
        return "http://127.0.0.1:5000/" + next_page


api.register(Movie)
api.register(Post)
api.register(Page)

api.serve()
