from toapi import XPath, Item, Api

api = Api('https://news.ycombinator.com/')


class Post(Item):
    url = XPath('//a[@class="storylink"][1]/@href')
    title = XPath('//a[@class="storylink"][1]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'


api.register(Post)

api.serve()

# Visit http://127.0.0.1:5000/
