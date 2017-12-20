from toapi import Settings


def test_api_with_ajax():
    from toapi import XPath, Item, Api
    class MySettings(Settings):
        web = {
            "with_ajax": False
        }

    api = Api('https://news.ycombinator.com/', settings=MySettings)

    class Post(Item):
        url = XPath('//a[@class="storylink"][1]/@href')
        title = XPath('//a[@class="storylink"][1]/text()')

        class Meta:
            source = XPath('//tr[@class="athing"]')
            route = {'/all?page=:page': '/news?p=:page'}

    class Page(Item):
        next_page = XPath('//a[@class="morelink"]/@href')

        class Meta:
            source = None
            route = {'/all?page=:page': '/news?p=:page'}

        def clean_next_page(self, next_page):
            return "http://127.0.0.1:5000/" + str(next_page)

    api.register(Post)
    api.register(Page)

    api.parse('/news?p=1')
