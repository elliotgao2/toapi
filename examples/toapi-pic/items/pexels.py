from toapi import Item, XPath


class Pexels(Item):
    __base_url__ = 'https://www.pexels.com'
    img = XPath('//a//img/@src')

    class Meta:
        source = XPath('//article[@class="photo-item"]')
        route = {'/pic/?q=:key': '/search/:key/'}
