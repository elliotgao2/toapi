from toapi import Item, XPath


class Page(Item):
    next_page = XPath('//a[@class="morelink"]/@href')

    class Meta:
        source = None
        route = '/news\?p=\d+'
