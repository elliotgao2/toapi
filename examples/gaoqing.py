from toapi import XPath, Item, Api, Settings


class MySettings(Settings):
    web = {
        "with_ajax": False,
        "request_config": {},
        "headers": None
    }


api = Api('http://gaoqing.la/', settings=MySettings)


class Movie(Item):
    url = XPath('//a[@class="zoom"]/@href')
    title = XPath('//a[@class="zoom"]/@title')

    class Meta:
        source = XPath('//*[@id="post_container"]/li')
        route = {'/gaoqing/': '/'}


api.register(Movie)

api.serve()
