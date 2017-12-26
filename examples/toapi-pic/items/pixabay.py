from toapi import Item, XPath


class Pixabay(Item):
    __base_url__ = 'https://pixabay.com/'
    img = XPath('//a//img/@src')

    class Meta:
        source = XPath('//div[@class="item"]')
        route = {'/pic/?q=:key': '/zh/photos/?q=:key'}
