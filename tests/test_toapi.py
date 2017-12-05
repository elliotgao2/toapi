def test_api():
    from toapi import XPath, Item, Api

    api = Api('https://news.ycombinator.com/')

    class Post(Item):
        url = XPath('//a[@class="storylink"][1]/@href')
        title = XPath('//a[@class="storylink"][1]/text()')

        class Meta:
            source = XPath('//tr[@class="athing"]')
            route = '/'

    api.register(Post)

    print(api.parse('/'))


def test_api_with_ajax():
    from toapi import XPath, Item, Api

    api = Api('https://news.ycombinator.com/', with_ajax=True)

    class Post(Item):
        url = XPath('//a[@class="storylink"][1]/@href')
        title = XPath('//a[@class="storylink"][1]/text()')

        class Meta:
            source = XPath('//tr[@class="athing"]')
            route = '/news\?p=\d+'

    class Page(Item):
        next_page = XPath('//a[@class="morelink"]/@href')

        class Meta:
            source = None
            route = '/news\?p=\d+'

    api.parse('/news?p=1')
