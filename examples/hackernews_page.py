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


api.register(Post)
api.register(Page)

api.serve()

# Visit http://127.0.0.1:5000/news?p=1
