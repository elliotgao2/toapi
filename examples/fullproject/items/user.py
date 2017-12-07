from toapi import Item, XPath


class User(Item):
    url = XPath('//a[@class="hnuser"][1]/@href')
    name = XPath('//a[@class="hnuser"][1]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/news\?p=\d+'
