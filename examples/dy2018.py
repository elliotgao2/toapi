from toapi import XPath, Item, Api

api = Api('http://www.dy2018.com/')


class Movies(Item):
    url = XPath('//b//a[@class="ulink"]/@href')
    title = XPath('//b//a[@class="ulink"]/text()')

    class Meta:
        source = XPath('//table[@class="tbspan"]')
        route = '/html/gndy/dyzz/index_\d+.html'


api.register(Movies)

api.serve()
