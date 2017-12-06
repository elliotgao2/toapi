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

        def clean_next_page(self, next_page):
            return "http://127.0.0.1:5000/" + next_page

    api.register(Post)
    api.register(Page)

    print(api.parse('/news?p=1'))
