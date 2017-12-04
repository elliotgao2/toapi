from toapi import XPath, Item, Api

api = Api('http://gaoqing.la/', with_ajax=True)


class Movie(Item):
    url = XPath('//a[@class="zoom"]/@href')
    title = XPath('//a[@class="zoom"]/@title')

    class Meta:
        source = XPath('//*[@id="post_container"]/li')
        route = '/'


api.register(Movie)

api.serve()
