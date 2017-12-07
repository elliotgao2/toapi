from toapi import XPath, Item, Api, Settings


class MySettings(Settings):
    with_ajax = True


api = Api('https://www.baidu.com/', settings=MySettings)


class Post(Item):
    url = XPath('//a/@href')
    title = XPath('//a/text()')

    class Meta:
        source = XPath('//div[@class="result"]')
        route = 's\?wd=.+'


class Page(Item):
    next_page = XPath('//div[@id="page"]//a/@href')

    class Meta:
        source = None
        route = 's\?wd=.+'

    def clean_next_page(self, next_page):
        return "http://127.0.0.1:5000/" + next_page


api.register(Post)
api.register(Page)

api.serve()

# Visit http://127.0.0.1:5000/news?p=1
