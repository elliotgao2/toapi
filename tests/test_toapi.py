from toapi import Settings
from toapi import XPath, Item, Api


def test_api():
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


def test_cache():
    api = Api()
    assert api.get_cache('a') is None
    api.set_cache('a', '1')
    assert api.get_cache('a') == '1'


def test_storage():
    api = Api()
    api.set_storage('a', '1')
    assert api.get_storage('a') == '1'


def test_status():
    api = Api()
    assert api.get_status('a') == 1
    api.update_status('a')
    assert api.get_status('a') == 2
