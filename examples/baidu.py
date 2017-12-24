from toapi import XPath, Item, Api

api = Api('https://www.baidu.com')


class Baidu(Item):
    url = XPath('//a/@href')
    title = XPath('//a/text()')

    class Meta:
        source = XPath('//div[@class="result"]')
        route = {'/:wd': '/s?wd=:wd'}


class Bing(Item):
    __base_url__ = 'https://www.bing.com'
    url = XPath('//a/@href')
    title = XPath('//a/text()')

    class Meta:
        source = XPath('//h2')
        route = {'/:wd': '/search?q=:wd'}


api.register(Baidu)
api.register(Bing)

api.serve()

# Visit http://127.0.0.1:5000/news?p=1
