from toapi import XPath, Item, Api, Settings


class MySettings(Settings):
    with_ajax = False


api = Api('http://gaoqing.la/', settings=MySettings)


class Movie(Item):
    url = XPath('//a[@class="zoom"]/@href')
    title = XPath('//a[@class="zoom"]/@title')

    class Meta:
        source = XPath('//*[@id="post_container"]/li')
        route = '/'


api.register(Movie)

api.serve()
